import requests


class RemoteObject:
    def __init__(self, id=-1):
        self.id = id


    # do a GET request for remote object by its specific id, grab the correct URL from the child class attribute
    def get_by_id(self, id):
        print(f'requesting at https://gorest.co.in/public/v2{self.url}{id}')
        response = requests.get(f'https://gorest.co.in/public/v2{self.url}{id}')

        if response.status_code == 200:
            response_json = response.json()
            for key in response_json:
                setattr(self, key, response_json[key])
    

    # child classes should call this to return a list of all remote objects of their type
    def get_all(self):
        print(f'requesting at https://gorest.co.in/public/v2{self.url}')
        response = requests.get(f'https://gorest.co.in/public/v2{self.url}')

        obj_list = []

        if response.status_code == 200:
            for obj in response.json():
                obj_list.append(self.__class__(**obj))

        return obj_list



    def post(self):
        headers = {
            'Authorization': 'Bearer a81345463eb65f45373d18174a0bf2750c85c6bbc2f4d4f687981c426ce0d47d'
        }

        url = 'https://gorest.co.in/public/v2' + self.url
        response = requests.post(url, headers=headers, data=self.__dict__)

        return response 


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

    
    # can be called with a user id parameter to get posts of user
    def get_all(self, user_id=-1):
        if user_id == -1:
            return super().get_all()
        else:
            response = requests.get(f'https://gorest.co.in/public/v2/users/{user_id}/posts')
            obj_list = []

            if response.status_code == 200:
                for obj in response.json():
                    obj_list.append(self.__class__(**obj))

            return obj_list
        

        


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

        # can be called with a user id parameter to get posts of user
    def get_all(self, post_id=-1):
        if post_id == -1:
            return super().get_all()
        else:
            response = requests.get(f'https://gorest.co.in/public/v2/users/{post_id}/posts')
            obj_list = []

            if response.status_code == 200:
                for obj in response.json():
                    obj_list.append(self.__class__(**obj))

            return obj_list


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

        # can be called with a user id parameter to get posts of user
    def get_all(self, user_id=-1):
        if user_id == -1:
            return super().get_all()
        else:
            response = requests.get(f'https://gorest.co.in/public/v2/users/{user_id}/posts')
            obj_list = []

            if response.status_code == 200:
                for obj in response.json():
                    obj_list.append(self.__class__(**obj))

            return obj_list
