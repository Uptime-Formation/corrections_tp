from monster_icon import *

def test_render():
    template = '''
    <html>
    <h1>{title}<h1>
    visites: {visits}
    </html>
    '''
    values = {
        'title': 'Pytest!',
        'visits': 32

    }
    result = render(template, values)

    assert result
    assert str(values['visits']) in result
    assert values['title'] in result

    assert str(values['visits']+1) not in result

def test_hash_name():
    name = "Jacques"
    salt = "lesel"
    salt2 = "leselbis"
    result = hash_name(name, salt)
    result2 = hash_name(name, salt2)

    print(len(result))
    print(result)

    assert result
    assert result != result2
    # assert result == 