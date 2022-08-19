from remote_objects import RemoteObject, User, Post, Comment, Todo
import requests

base_url = 'https://gorest.co.in/public/v2/'
user = User()
user.get_by_id(2783)
print(user.name)

print(user.get_all())


post = Post()
print(Post.get_all(user_id=3566))
print(post)
