import requests

TERM_BLUE = "\033[94m"
TERM_GREEN = "\033[92m"
TERM_RED = "\033[96m"
TERM_END = "\033[0m"


def client():
    url = input("PaperAgent server: ")
    entity_name = input("login user: ")

    rsp = requests.post(url=f"{url}/login", json={"entity_name": entity_name})
    rsp.raise_for_status()

    session_id = rsp.json()["data"]["session_id"]

    while True:
        query = input(f"{TERM_BLUE}query: {TERM_END}")
        data = {"entity_name": entity_name, "session_id": session_id, "query": query}
        rsp = requests.post(url=f"{url}/agent", json=data)

        output = rsp.json()["data"]["output"]
        if rsp.status_code == 200:
            print(f"{TERM_GREEN}{output}{TERM_END}")
        else:
            print(f"{TERM_RED}{output}{TERM_END}")
