import os
import requests
import configparser

RC_FILE = os.path.expanduser("~/.docmeshrc")


class TermColor:
    blue = "\033[94m"
    green = "\033[92m"
    red = "\033[96m"
    end = "\033[0m"


def client():
    # setup docmesh server
    url = input("docmesh server: ")

    # setup docmesh token
    parser = configparser.ConfigParser()
    if not os.path.exists(RC_FILE):
        access_token = input(f"You have not setup {RC_FILE}, please enter your access_token: ")

        parser["docmesh"] = {}
        parser["docmesh"]["access_token"] = access_token

        with open(RC_FILE, "w", encoding="utf-8") as f:
            parser.write(f)
            print(f"Write your access_token to {RC_FILE}.")
    else:
        parser.read(RC_FILE)
        access_token = parser["docmesh"]["access_token"]

    # setup headers
    headers = {"Authorization": f"Bearer {access_token}"}

    # retreive entity_name and session_id
    rsp = requests.post(url=f"{url}/login", headers=headers)
    if rsp.status_code == 200:
        data = rsp.json()["data"]
        entity_name = data["entity_name"]
        session_id = data["session_id"]
        print(f"{TermColor.green}You are logined in as: {entity_name}{TermColor.end}")
    if rsp.status_code == 401:
        detail = rsp.json()["detail"]
        print(f"{TermColor.red}{detail}{TermColor.end}")
        rsp.raise_for_status()
    else:
        rsp.raise_for_status()

    # send query
    while True:
        query = input(f"{TermColor.blue}query: {TermColor.end}")
        data = {"session_id": session_id, "query": query}
        rsp = requests.post(url=f"{url}/agent", headers=headers, json=data)

        output = rsp.json()["data"]["output"]
        if rsp.status_code == 200:
            print(f"{TermColor.green}{output}{TermColor.end}")
        else:
            print(f"{TermColor.red}{output}{TermColor.end}")
