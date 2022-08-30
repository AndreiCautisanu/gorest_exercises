import requests
import vars


def GET(url: str, id: int = None):
    print(f'Sending GET request at {url + (str(id) if id is not None else "")}...\n')
    response = requests.get(url + (str(id) if id is not None else ''))
    print(f'Request sent, received response {response.status_code}')

    return (response.status_code, response.json())



def POST(url: str, headers: dict, data: dict):
    print(f'Sending POST request to {base_url}{url}')
    response = requests.post(base_url + url, headers=headers, data=data)
    print(f'POST request sent, received response {response.status_code}')

    if response.status_code == 422:
        print(response.json())

    return (response.status_code, response.json())


def DELETE(url: str, headers: dict):
    print(f'Sending DELETE request for {base_url}{url}')
    response = requests.delete(base_url + url, headers=headers)
    print(f'DELETE request sent, received response {response.status_code}')

    if response.status_code == 204:
        print('Remote object successfully deleted')
    else:
        print(f'DELETE error, got status code {response.status_code}')