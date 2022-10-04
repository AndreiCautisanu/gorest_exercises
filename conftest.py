import pytest
import backend_functions as bf
import vars


class ValueStorage:
    cached_obj1 = None


def post_from_toml_nested(url, parent_obj, parent_obj_type):
    status_code, payload = bf.POST(url, vars.headers, parent_obj)
    print(payload)

    with open('response_code_log.txt', 'w') as f:
        f.write(str(status_code) + '\n')
    
    if status_code == 201:
        id = payload['id']

        with open('objs_log.txt', 'a') as f:
            f.write(f'/{parent_obj_type}s/{id}\n')

        for key in ['user', 'post', 'comment', 'todo']:
            if key in parent_obj:
                for _key in parent_obj[key]:
                    parent_obj[key][_key][f'{parent_obj_type}_id'] = id
                    post_from_toml_nested(vars.type_url[key], parent_obj[key][_key], key)
    
    else:
        print(f'ERROR STATUS CODE {status_code}')



@pytest.fixture(scope='class')
def operations_log():
    print('-----------')
    with open('objs_log.txt', 'w') as f:
        f.write('')
    with open('response_code_log.txt', 'w') as f:
        f.write('')

    yield

    with open('objs_log.txt', 'r') as f:
        lines = f.readlines()
        lines = [line.rstrip() for line in lines]

        for line in lines:
            bf.DELETE(line, vars.headers)