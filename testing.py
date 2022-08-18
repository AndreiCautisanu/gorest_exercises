from remote_objects import RemoteObject, User, Post, Comment, Todo
import requests

base_url = 'https://gorest.co.in/public/v2/'
user = User()
user.get_by_id(2783)
print(user.name)


post = Post()
post.get_by_id(1373)
print(post.__dict__)