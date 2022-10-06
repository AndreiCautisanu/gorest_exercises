from urllib import response
import backend_functions as bf
import vars
from remote_objects import User, Post, Comment, Todo
import conftest


class TestClass1:

    def test_user_post_get_delete(self, operations_log, valid_objects):
        user1 = User(**valid_objects['user']['danny'])
        status_code, payload = user1.post()
        with open('objs_log.txt', 'a') as f:
            f.write(f'/users/{user1.id}\n')

        assert status_code == 201


        # GET request on the id of the object just posted, check that correct data is returned
        user2 = User()
        status_code, _ = user2.get_by_id(user1.id)

        assert (status_code == 200, all(user1.__dict__[key] == user2.__dict__[key] for key in ['name', 'email', 'gender', 'status'])) == (True, True)


        # DELETE user1, check that 404 is returned when trying to run GET on its ID
        id = user1.id
        status_code_del = user1.delete()
        status_code_get, _ = user1.get_by_id(id)

        assert ((status_code_del == 204), (status_code_get == 404)) == (True, True)



    def test_user_patch(self, operations_log, valid_objects):
        user1 = User(**valid_objects['user']['danny'])
        status_code, _ = user1.post()
        with open('objs_log.txt', 'a') as f:
            f.write(f'/users/{user1.id}\n')
        assert status_code == 201

        status_code, payload = bf.PATCH(f'/users/{user1.id}', headers = vars.headers, data = {"name": "Jack Wilshere"})

        user1.get_by_id(user1.id)

        assert (status_code == 200, user1.name == "Jack Wilshere") == (True, True)




class TestClass2:
    def test_get_all_users(self, operations_log):
        users = []
        status_code, users = User.get_all(type='users')
        assert ((status_code == 200), (len(users) > 0)) == (True, True)


    def test_user_children_posts_get_delete(self, operations_log, user_with_posts):
        for key in user_with_posts['user']:
            conftest.post_from_toml_nested(vars.type_url['user'], user_with_posts['user'][key], 'user')
        
        obj_urls = []
        with open('objs_log.txt', 'r') as f:
            obj_urls = f.readlines()
        

        # parent_id of posted user
        id = int(obj_urls[0].split('/')[2])


        #GET request to /users/<id>/posts, check if all objects are children of parent
        response_code, post_list = Post.get_all(type = 'posts', parent_id = id)
        assert response_code == 200
        assert all(obj['user_id'] == id for obj in post_list)


        #Delete parent object and check that children are deleted too
        user1 = User()
        user1.get_by_id(id)
        user1.delete()

        response_codes = []
        for url in obj_urls[1:]:
            post_id = int(url.split('/')[2])

            post1 = Post()
            status_code, payload = post1.get_by_id(id = post_id)
            response_codes.append(status_code)

        assert all(code == 404 for code in response_codes)

        



class TestClass3:
    def test_user_get_invalid_id(self, operations_log):
        user1 = User()
        status_code, _ = user1.get_by_id(1365231246)
        assert status_code == 404

    
    def test_user_post_invalid_gender_value(self, operations_log, invalid_objects):
        user1 = User(**invalid_objects['user']['invalid_gender'])
        status_code, payload = user1.post()

        assert ((status_code == 422), ("can be male of female" in payload[0]['message'])) == (True, True)

    

    def test_user_post_invalid_status_value(self, operations_log, invalid_objects):
        user1 = User(**invalid_objects['user']['invalid_status'])
        status_code, payload = user1.post()

        assert ((status_code == 422), ("can't be blank" in payload[0]['message'])) == (True, True)



    def test_user_post_duplicate_email(self, operations_log, invalid_objects):
        #Create user with valid email
        user1 = User(**invalid_objects['user']['new_email'])
        status_code, payload = user1.post()
        assert status_code == 201
        with open('objs_log.txt', 'a') as f:
            f.write(f'/users/{user1.id}\n')


        #Create new user with the same email
        user2 = User(**invalid_objects['user']['duplicate_email'])
        status_code, payload = user2.post()
        
        assert ((status_code == 422), ("has already been taken" in payload[0]['message'])) == (True, True)


    def test_post_invalid_parent_user(self, operations_log, invalid_objects):
        post1 = Post(**invalid_objects['post']['invalid_parent'])
        status_code, payload = post1.post()

        assert ((status_code == 422), ("must exist" in payload[0]['message'])) == (True, True)


    def test_user_delete_invalid_ID(self, operations_log):
        user1 = User(id = 999999999)
        status_code = user1.delete()
        assert status_code == 404


    def test_user_post_to_invalid_url(self, operations_log, valid_objects):
        user1 = User(**valid_objects['user']['danny'])
        status_code, payload = bf.POST('/posts/', vars.headers, user1.__dict__)

        assert ((status_code == 422), (len(payload) == 4)) == (True, True)

    
    def test_user_post_invalid_bearer(self, operations_log, valid_objects):
        user1 = User(**valid_objects['user']['danny'])
        status_code, payload = bf.POST('/users/', {'Authorization': 'AAAAAAAAAAAAAAA'}, user1.__dict__)

        assert status_code == 401