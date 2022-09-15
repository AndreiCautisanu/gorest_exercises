from venv import create
import pytest
import toml_methods
import backend_functions as bf
import vars
import toml

created_objects = []

@pytest.fixture()
def objects(scope='module'):

    # SETUP
    file_path = r'objects\objects_to_post.toml'

    with open('objs_log.txt', 'w') as f:
        f.write('')
    
    yield file_path


    #CLEANUP
    with open('objs_log.txt', 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]

        for line in lines:
            bf.DELETE(line, vars.headers)


def test_post_toml(objects):
    content = toml.load(objects)
    for key in ['user', 'post', 'comment', 'todo']:
        if key in content:
            for _key in content[key]:
                toml_methods.post_with_children(vars.type_url[key], content[key][_key], key)

    with open('response_code_log.txt', 'r') as f:
        responses = f.readlines()
        responses = [line.rstrip() for line in responses]

        assert responses == ['201'] * len(responses)