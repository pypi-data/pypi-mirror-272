from typing import Union
import httpx
import io
import json
import logging
import os 
import tarfile 
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.responses import RedirectResponse, StreamingResponse

from bincrafters_conan_remote.helpers import conf, make_request, make_request_async_multiple


app = FastAPI()
logger = logging.getLogger("bincrafters-conan-remote")

cached_headers = {}

def create_tarfile(file_paths: [str] = ["requirements.txt",]):
    # Create an in-memory file
    data = io.BytesIO()

    # Create a tarfile in the in-memory file
    with tarfile.open(fileobj=data, mode='w:gz') as tar:
        for file_path in file_paths:
            tar.add(file_path)
        info = tarfile.TarInfo(name='test.txt')
        info.size = len('This is a test file')
        tar.addfile(info, io.BytesIO('This is a test file'.encode()))
    data.seek(0)
    return data


@app.get("/")
def read_root(request: Request):
    user_agent = request.headers.get('user-agent')
    return {"Hello": "World", "User-Agent": user_agent, "pwd": os.getcwd()}


def v1_ping(remote_http_url, user_agent):
    if remote_http_url in cached_headers:
        headers = cached_headers[remote_http_url]
    else:
        r = make_request(f"{remote_http_url}{conf['filename_server_conan_headers']}", user_agent)
        if r.status_code == 404:
            headers = conf["headers_default"]
        else:
            headers = json.loads(r.content)
        cached_headers[remote_http_url] = headers
    return Response(headers=headers)

def get_latest_revision(remote_http_url_revisions, user_agent):
    r = make_request(f"{remote_http_url_revisions}", user_agent)
    revisions = r.json()
    # https://github.com/conan-io/conan/blob/80fee05d5811608511bbb30a965afd66bdc13311/conans/server/revision_list.py#L40
    return revisions["revisions"][-1]

@app.get("/{url_path:path}")
async def get_external_site(request: Request, url_path: str):
    # User Agent Manipulation
    user_agent = request.headers.get('user-agent')
    if not user_agent.startswith("Conan"):
        user_agent = conf["user_agent_default"]

    # Remote Source Selection
    # example /r/github+bincrafters_remote+testing_v-998+inexorgame/
    remote_type = conf["remote_default_type"]
    remote_types_allowed = ["local", "github", "conancenter"]
    remote_source = conf["remote_default_source"] # this is not allowed to have underscores
    remote_checkout = conf["remote_default_checkout"] # this is not allowed to have underscores
    remote_selection = conf["remote_default_selection"]
    remote_config = f"{remote_type}+{remote_source}+{remote_checkout}+{remote_selection}"
    if url_path.startswith("r/"):
        remote_config = url_path.split('/')[1]
        # remote_type, remote_source, remote_checkout = remote_config.split("+")
        remote_type, *remote_confs = remote_config.split("+")
        if remote_type in ["local", "github"]:
            remote_source = remote_confs[0].replace("_", "/")
            remote_checkout = remote_confs[1].replace("_", "/")
            if remote_confs[2]:
                remote_selection = remote_confs[2]
        url_path = "/".join(url_path.split('/')[2:])   
    remote_http_suffix = ""
    remote_http_url = f"https://raw.githubusercontent.com/{remote_source}/{remote_checkout}/r/{remote_selection}/"
    if remote_type == "conancenter":
        remote_http_url = "https://center.conan.io/"
        remote_config = "conancenter"
    elif remote_type == "github":
        remote_http_url = f"https://raw.githubusercontent.com/{remote_source}/{remote_checkout}/r/{remote_selection}/"

    cache_url_path = os.path.join("r", remote_config, url_path)

    logger.info(f"Remote Type: {remote_type}, Remote Source: {remote_source}, Remote Checkout: {remote_checkout}, Remote Selection: {remote_selection}, Remote HTTP URL: {remote_http_url}, Remote HTTP Suffix: {remote_http_suffix}")
    logger.info(f"url_path: {url_path}, cache_url_path: {cache_url_path}")

    default_response_type = "application/json"

    if url_path == "v1/ping":
        return v1_ping(remote_http_url=remote_http_url, user_agent=user_agent)

    if not remote_http_url in cached_headers:
        _ = v1_ping(remote_http_url=remote_http_url, user_agent=user_agent)

    if url_path.endswith("latest"):
        tmp_path = "/".join(url_path.split("/")[:-1])
        revisions_url = f"{remote_http_url}{tmp_path}/revisions.json"
        latest_revision = get_latest_revision(remote_http_url_revisions=revisions_url, user_agent=user_agent)
        logger.info(f"Latest Revision: {latest_revision}")
        return Response(content=json.dumps(latest_revision).encode(), media_type="application/json", headers=cached_headers[remote_http_url])

    # Special handling of binary files
    if url_path.endswith(".tgz"):
        # data = create_tarfile()
        filename = url_path.split('/')[-1]
        remote_http_suffix = ".json"

        # Create an in-memory file
        data = io.BytesIO()

        # Create a tarfile in the in-memory file
        with tarfile.open(fileobj=data, mode='w:gz') as tar:
            #for file_path in file_paths:
            #    tar.add(file_path)

            file_list_r = make_request(f"{remote_http_url}{url_path}{remote_http_suffix}", user_agent)
            logger.info(f"File List url: {remote_http_url}{url_path}{remote_http_suffix}")
            file_list = file_list_r.json()
            logger.info(f"File List: {file_list}")
            request_urls = []
            for tar_file in file_list["files"]:
                url_path_dir = "/".join(url_path.split('/')[:-1])
                request_urls.append(f"{remote_http_url}{url_path_dir}/{tar_file}")
                
            request_responses = await make_request_async_multiple(request_urls, user_agent)
            for file_content_r in request_responses:
                file_content = file_content_r.content
                tar_filename = "/".join(tar_file.split('/')[1:])
                info = tarfile.TarInfo(name=tar_file)
                info.size = len(file_content)
                tar.addfile(info, io.BytesIO(file_content))
        data.seek(0)

        # Create a StreamingResponse to return the tarfile
        response = StreamingResponse(data, media_type='application/gzip')
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    elif url_path.endswith(".txt") or url_path.endswith(".py"):
        default_response_type = "text/plain"
    else:
        if remote_type in ["local", "github"]:
            remote_http_suffix = ".json"

    getting_url = f"{remote_http_url}{url_path}{remote_http_suffix}"
    r = make_request(getting_url, user_agent)

    # logger.info(f"Headers: {r.headers}")
    content_type = r.headers.get('Content-Type', 'application/json')
    if remote_http_suffix == ".json":
        content_type = "application/json"

    # Create caches, mostly for debugging
    cache_path = os.path.join("cache", *cache_url_path.split('/'))
    os.makedirs(cache_path, exist_ok=True)
    with open(os.path.join(cache_path, "response.txt"), 'wb') as f:
        f.write(user_agent.encode())
        f.write(json.dumps(dict(r.headers)).encode())
        f.write("\n".encode())
        f.write("\n".encode())
        f.write(r.content)

    return Response(content=r.content, media_type=content_type, headers=cached_headers[remote_http_url])



def run_remote(args):
    uvicorn.run(app, host="0.0.0.0", port=args.port)
