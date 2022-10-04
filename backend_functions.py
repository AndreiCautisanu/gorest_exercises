import requests
import vars


def GET(url: str):
    print(f'Sending GET request at {vars.base_url}{url}\n')
    response = requests.get(vars.base_url + url, headers=vars.headers)
    print(f'Request sent, received response {response.status_code}')

    return (response.status_code, response.json())



def POST(url: str, headers: dict, data: dict):
    print(f'Sending POST request to {vars.base_url}{url}')
    print(f'Trying to send payload {data}')
    response = requests.post(vars.base_url + url, headers=headers, data=data)
    print(f'POST request sent, received response {response.status_code}')

    if response.status_code == 422:
        print(response.json())

    return (response.status_code, response.json())


def PATCH(url: str, headers: dict, data: dict):
    print(f'Sending PATCH request to {vars.base_url}{url}')
    response = requests.patch(vars.base_url + url + str(id), headers=headers, data=data)
    print(f'PATCH request sent, received response {response.status_code}')

    if response.status_code == 422:
        print(response.json())

    return (response.status_code, response.json())


def DELETE(url: str, headers: dict):
    print(f'Sending DELETE request for {vars.base_url}{url}')
    response = requests.delete(vars.base_url + url, headers=headers)
    print(f'DELETE request sent, received response {response.status_code}')

    if response.status_code == 204:
        print('Remote object successfully deleted')
    else:
        print(f'DELETE error, got status code {response.status_code}')

    return response.status_code