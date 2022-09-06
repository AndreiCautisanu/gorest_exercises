import toml
import sys
import remote_objects
import backend_functions as bf
from vars import base_url, type_url, headers


def post_from_toml(file_path: str):
    content = toml.load(file_path)
    for key in ['user', 'post', 'comment', 'todo']:
        if key in content:
            for _key in content[key]:
                status_code, payload = bf.POST(type_url[key], headers, content[key][_key])


if __name__ == '__main__':

    post_from_toml(r'objects\objects_to_post.toml')