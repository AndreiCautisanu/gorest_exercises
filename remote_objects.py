import requests

class RemoteObject:

    def __init__(self, id=-1):
        self.id = id


    def get_by_id(self, id):
        print(f'requesting at https://gorest.co.in/public/v2{self.url}{id}')
        response = requests.get(f'https://gorest.co.in/public/v2{self.url}{id}')
        
        if response.status_code == 200:
            response_json = response.json()
            for key in response_json:
                setattr(self, key, response_json[key])

    def post(self):
        pass


class User(RemoteObject):
    url = '/users/'

    def __init__(self, id=-1, name='', email='', gender='', status=''):
        super().__init__(id)
        self.name = name
        self.email = email
        self.gender = gender
        self.status = status

    def __str__(self):
        return f'[id: {self.id}, name: {self.name}, email: {self.email}, gender: {self.gender}, status: {self.status}]\n'



class Post(RemoteObject):
    url = '/posts/'
    
    def __init__(self, id=-1, user_id='', title='', body=''):
        super().__init__(id)
        self.user_id = user_id
        self.title = title
        self.body = body

    def __str__(self):
        return f'[id: {self.id}, user_id: {self.user_id}, title: {self.title}, body: {self.body}]\n'


class Comment(RemoteObject):
    url = '/comments/'

    def __init__(self, id=-1, post_id=-1, name='', email='', body=''):
        super().__init__(id)
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

    def __str__(self):
        return f'[id: {self.id}, post_id: {self.post_id}, name: {self.name}, email: {self.email}, body: {self.body}]\n'

class Todo(RemoteObject):
    url = '/todos/'

    def __init__(self, id=-1, user_id=-1, title='', due_on='', status=''):
        super().__init__(id)
        self.user_id = user_id
        self.title = title
        self.due_on = due_on
        self.status = status
    
    def __str__(self):
        return f'[id: {self.id}, user_id: {self.user_id}, title: {self.title}, due_on: {self.due_on}, status: {self.status}]\n'