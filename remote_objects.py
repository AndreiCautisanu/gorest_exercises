from email.mime import base
import requests
import backend_functions as bf
import vars

class RemoteObject:

    def __init__(self, id=None):
        self.id = id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass
    #     if not any([exc_type, exc_value, tb]):
    #         bf.DELETE(self.url + str(self.id), vars.headers)

    #     else:
    #         print(exc_value)


    # do a GET request for remote object by its specific id, grab the correct URL from the child class attribute
    def get_by_id(self, id):
        print(str(id))
        status_code, payload =  bf.GET(self.url + str(id))
        if status_code == 200:
            for key in payload:
                setattr(self, key, payload[key])

        else:
            print(f'GET error, got response status code {status_code}')

        return status_code, payload

    

    # child classes should call this to return a list of all remote objects of their type
    @staticmethod
    def get_all(type=None, parent_id=None):

        if parent_id is None:
            url = f'/{type}'
        else:
            if type == 'posts' or type == 'todos':
                url = '/users/' + f'{parent_id}/' + type
            elif type == 'comments':
                url = '/posts/' + f'{parent_id}/' + type
            else:
                print('INVALID')
                return []

        status_code, payload = bf.GET(url)
        obj_list = []

        if status_code == 200:
            for obj in payload:
                obj_list.append(obj)

        else:
            print(f'GET error, got response status code {status_code}')

        return status_code, obj_list


    def post(self):
        url = 'https://gorest.co.in/public/v2' + self.url
        status_code, payload = bf.POST(self.url, vars.headers, self.__dict__)

        if status_code == 201:
            print(f'Remote object successfully created with id {payload["id"]}')
            self.id = payload['id']

        else:
            print(f'POST error, got response status code {status_code}')

        return status_code, payload


    def delete(self):
        status_code = bf.DELETE(f'{self.url}{str(self.id)}', headers=vars.headers)
        
        if status_code == 204:
            print(f'Remote object with id {self.id} successfully deleted')
            self.id = None

        else:
            print(f'DELETE error, got response status cude {status_code}')

        return status_code

class User(RemoteObject):
    url = '/users/'

    def __init__(self, id=None, name=None, email=None, gender=None, status=None):
        super().__init__(id)
        self.name = name
        self.email = email
        self.gender = gender
        self.status = status

    def __str__(self):
        return f'[id: {self.id}, name: {self.name}, email: {self.email}, gender: {self.gender}, status: {self.status}]\n'



class Post(RemoteObject):
    url = '/posts/'
    
    def __init__(self, id=None, user_id=None, title=None, body=None):
        super().__init__(id)
        self.user_id = user_id
        self.title = title
        self.body = body

    def __str__(self):
        return f'[id: {self.id}, user_id: {self.user_id}, title: {self.title}, body: {self.body}]\n'
        


class Comment(RemoteObject):
    url = '/comments/'

    def __init__(self, id=None, post_id=None, name=None, email=None, body=None):
        super().__init__(id)
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

    def __str__(self):
        return f'[id: {self.id}, post_id: {self.post_id}, name: {self.name}, email: {self.email}, body: {self.body}]\n'


class Todo(RemoteObject):
    url = '/todos/'

    def __init__(self, id=None, user_id=None, title=None, due_on=None, status=None):
        super().__init__(id)
        self.user_id = user_id
        self.title = title
        self.due_on = due_on
        self.status = status
    
    def __str__(self):
        return f'[id: {self.id}, user_id: {self.user_id}, title: {self.title}, due_on: {self.due_on}, status: {self.status}]\n'
