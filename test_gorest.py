import pytest
import toml_methods
import backend_functions as bf
import vars
import toml
from remote_objects import User, Post, Comment, Todo
import conftest
import re
from copy import deepcopy



class TestClass1:

    def test_user_post(self, operations_log):
        user1 = User(
            name = "Abe Lincoln",
            email = "Abez_Lingz_16@us.gov",
            gender = "male",
            status = "inactive"
        )

        status_code, payload = user1.post()
        with open('objs_log.txt', 'a') as f:
            f.write(f'/users/{user1.id}\n')
        print(payload)

        conftest.ValueStorage.cached_objs = [user1.__dict__]

        assert status_code == 201




    def test_user_get(self, operations_log):
        user1 = User()
        with open('objs_log.txt', 'r') as f:
            obj = f.read()

        status_code, payload = user1.get_by_id((int(obj.split('/')[-1])))
        
        assert ((status_code == 200), (conftest.ValueStorage.cached_objs[0] == user1.__dict__)) == (True, True)




    def test_user_patch(self, operations_log):
        id = conftest.ValueStorage.cached_objs[0]['id']
        status_code, payload = bf.PATCH(f'/users/{id}', headers = vars.headers, data = {"name": "Jack Wilshere"})

        user1 = User()
        user1.get_by_id(id)

        assert (status_code == 200, user1.name == "Jack Wilshere") == (True, True)




    def test_user_delete(self, operations_log):
        user1 = User(**conftest.ValueStorage.cached_objs[0])
        status_code_del = user1.delete()
        status_code_get, payload = user1.get_by_id(conftest.ValueStorage.cached_objs[0]['id'])

        assert ((status_code_del == 204), (status_code_get == 404)) == (True, True)




class TestClass2:
    def test_get_all_users(self, operations_log):
        users = []
        status_code, users = User.get_all(type='users')
        assert ((status_code == 200), (len(users) > 0)) == (True, True)


    def test_get_all_posts_of_user(self, operations_log):
        posts = []
        status_code, posts = Post.get_all(type='posts', parent_id=2409)
        correct_parent = all(post['user_id'] == 2409 for post in posts)

        assert ((status_code == 200), correct_parent) == (True, True)


    def test_delete_user_deletes_children(self, operations_log):
        user1 = User(
            name = "Roy Jones Jr",
            email = "rjj@punches.com",
            gender = "male",
            status = "active"
        )

        status_code, payload = user1.post()

        if status_code != 201:
            pytest.xfail("failed to post parent object")

        post1 = Post(
            user_id = user1.id,
            title = "Hi I used to punch people",
            body = "Made tons of money"
        )

        post2 = Post(
            user_id = user1.id,
            title = "TEst Post AAAA",
            body = "123abc123cvbv"
        )
        _, _ = post1.post()
        _, _ = post2.post()

        status_code = user1.delete()
        if status_code != 204:
            pytest.xfail('failed to delete')

        sc1, payload = post1.get_by_id(post1.id)
        sc2, payload = post2.get_by_id(post2.id)

        assert ((sc1 == 404), (sc2 == 404)) == (True, True)



class TestClass3:
    def test_user_get_invalid_id(self, operations_log):
        user1 = User()
        status_code, payload = user1.get_by_id(1365231246)
        assert status_code == 404

    
    def test_user_post_invalid_gender_value(self, operations_log):
        user1 = User(
            name = "Mr T",
            email = "mrt4@TTTinc.com",
            gender = "male",
            status = "active"
        )

        _, _ = user1.post()
        conftest.ValueStorage.cached_objs = [deepcopy(user1)]

        user1.gender = "NOT A POLITICAL STATEMENT"
        status_code, payload = user1.post()

        assert ((status_code == 422), ("can be male of female" in payload[0]['message'])) == (True, True)

    
    def test_user_post_invalid_status_value(self, operations_log):
        user1 = deepcopy(conftest.ValueStorage.cached_objs[0])
        user1.status = "FAR AWAY"
        status_code, payload = user1.post()
        assert ((status_code == 422), ("can't be blank" in payload[0]['message'])) == (True, True)


    def test_user_post_duplicate_email(self, operations_log):
        user1 = deepcopy(conftest.ValueStorage.cached_objs[0])
        user1.email = 'mrt4@TTTinc.com'
        status_code, payload = user1.post()
        
        assert ((status_code == 422), ("has already been taken" in payload[0]['message'])) == (True, True)


    def test_post_invalid_parent_user(self, operations_log):
        post1 = Post(
            user_id = 99999999,
            title = 'Testing testing',
            body = 'aaaaaaaaaaaaaaaaaaaaaaa'
        )

        status_code, payload = post1.post()

        assert ((status_code == 422), ("must exist" in payload[0]['message'])) == (True, True)


    def test_user_delete_invalid_ID(self, operations_log):
        user1 = User(id = 999999999)
        status_code = user1.delete()
        assert status_code == 404


    def test_user_post_to_invalid_url(self, operations_log):
        user1 = deepcopy(conftest.ValueStorage.cached_objs[0])
        status_code, payload = bf.POST('/posts/', vars.headers, user1.__dict__)

        assert ((status_code == 422), (len(payload) == 4)) == (True, True)

    
    def test_user_post_invalid_bearer(self, operations_log):
        user1 = deepcopy(conftest.ValueStorage.cached_objs[0])
        status_code, payload = bf.POST('/users/', {'Authorization': 'AAAAAAAAAAAAAAA'}, user1.__dict__)

        assert status_code == 401


    
    