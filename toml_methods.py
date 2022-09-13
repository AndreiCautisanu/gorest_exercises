import toml
import sys
import remote_objects
import backend_functions as bf
from vars import base_url, type_url, headers


def post_with_children(url, parent_obj, parent_obj_type):
    status_code, payload = bf.POST(url, headers, parent_obj)
    print(payload)
    
    if status_code == 201:
        id = payload['id']
        for key in ['user', 'post', 'comment', 'todo']:
            if key in parent_obj:
                for obj in parent_obj[key]:
                    obj[f'{parent_obj_type}_id'] = id
                    post_with_children(type_url[key], obj, key)
    
    else:
        print(f'ERROR STATUS CODE {status_code}')


def post_from_toml(file_path: str):
    content = toml.load(file_path)
    for key in ['user', 'post', 'comment', 'todo']:
        if key in content:
            for _key in content[key]:
                post_with_children(type_url[key], content[key][_key], key)

if __name__ == '__main__':

    post_from_toml(r'objects\objects_to_post.toml')

    #content = toml.load(r'objects\objects_to_post.toml')
    #print(content['user'])