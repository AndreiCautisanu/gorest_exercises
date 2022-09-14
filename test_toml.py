import pytest
import toml_methods
import backend_functions as bf
import vars
import toml

created_objects = []

@pytest.fixture()
def objects():
    file_path = r'objects\objects_to_post.toml'
    yield file_path
    for obj in created_objects:
        bf.DELETE(vars.base_url + vars.type_url(obj[0]) + str(obj[1]))


def test_post_toml(objects):
    content = toml.load(objects)
    for key in ['user', 'post', 'comment', 'todo']:
        if key in content:
            for _key in content[key]:
                toml_methods.post_with_children(vars.type_url[key], content[key][_key], key)