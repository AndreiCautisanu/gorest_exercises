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