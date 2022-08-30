from remote_objects.remote_objects import RemoteObject, User, Post, Comment, Todo
import requests

base_url = 'https://gorest.co.in/public/v2/'

print(RemoteObject.get_all(type='users'))

# with User() as user, Post() as post1:
#     user.get_by_id(2600)
#     print(str(user))
#     user.email = 'real_person_i_2waa2ear2@live.com'
#     user.name = 'Real Man Personn'
#     user.status = 'inactive'
#     response = user.post()

#     print(str(user))


    # post1.get_by_id(1442)
    # print(str(post1))
    # post1.title = 'How to do things'
    # post1.body = 'aaaaaaaaaaa'
    # response = post1.post()

    # if response.status_code == 422:
    #     raise Exception('POST Data validation error')
    # if response.status_code == 401:
    #     raise Exception('POST Authentication failed')

    # print(response.json())
    # print(str(post1))

user = User()
user.get_by_id(4002)
print(user.name)