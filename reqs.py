import requests
import json


base_url = 'https://gorest.co.in/public/v2/'



class User:
    def __init__(self, id, name, email, gender, status):
        self.id = id
        self.name = name
        self.email = email
        self.gender = gender
        self.status = status
        self.posts = []
        self.todos = []

    def __str__(self):
        return f'[id: {self.id}, name: {self.name}, email: {self.email}, gender: {self.gender}, status: {self.status}]\n'


class Post:
    def __init__(self, id, user_id, title, body):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.body = body

    def __str__(self):
        return f'[id: {self.id}, user_id: {self.user_id}, title: {self.title}, body: {self.body}]\n'


class Comment:
    def __init__(self, id, post_id, name, email, body):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

    def __str__(self):
        return f'[id: {self.id}, post_id: {self.post_id}, name: {self.name}, email: {self.email}, body: {self.body}]\n'


class Todo:
    def __init__(self, id, user_id, title, due_on, status):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.due_on = due_on
        self.status = status
    
    def __str__(self):
        return f'[id: {self.id}, user_id: {self.user_id}, title: {self.title}, due_on: {self.due_on}, status: {self.status}]\n'



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
print(post('users', new_user).status_code)


print(get_by_id('users', 99998))