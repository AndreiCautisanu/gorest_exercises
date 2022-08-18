import requests
import json
from remote_objects import User, Post, Comment, Todo


base_url = 'https://gorest.co.in/public/v2/'


# easier way to choose which constructor to use in the get functions
url_to_class_map = {
    'users': User,
    'posts': Post,
    'comments': Comment,
    'todos': Todo
}


# gets all remote objects, pass relevant part of url as argument (e.g. get_all('users'))
# or nested (get_all('users', 3705, 'posts'))
def get_all(to_get, id=None, to_get_nested=None):
    if id is not None:
        response = requests.get(base_url + to_get + f'/{id}' + f'/{to_get_nested}')
    else:
        response = requests.get(base_url + to_get)

    obj_list = []  # list to return

    if response.status_code == 200:
        for obj in response.json():
            obj_list.append(url_to_class_map[to_get_nested or to_get](**obj)) # create the correct class passing the dictionary values
            # could also do this with a base object and inheritance but couldn't figure out a way to relate them and have it be
            # as easy as this where they're all independent classes, will change if needed

            # gets the nested resource type if argument was provided, otherwise uses the root

    return obj_list


# get one object by its id
def get_by_id(to_get, id):
    response = requests.get(base_url + to_get + f'/{id}')

    if response.status_code == 200:
        print(response.json())
        return url_to_class_map[to_get](**response.json())
    else:
        return None



def post(res_type, content):
    headers = {
        'Authorization': 'Bearer 00acd34b1e776abaf94fba24b268c3d2c9168fdcb51649abc85e3cef2ff30111'
    }
    url = base_url + res_type

    response = requests.post(url, headers=headers, data=content)

    return response



for obj in get_all('users'):
    print(obj)

print(get_by_id('users', 1))

print(get_by_id('users', 3705))

for obj in get_all('users', 3705, 'posts'):
    print(obj)


new_user = {"id":99998,"name":"Test User","email":"john_delaney_4pres_2@gmail.com","gender":"male","status":"active"}
print(post('users', new_user).json())


#print(get_by_id('users', 99998))