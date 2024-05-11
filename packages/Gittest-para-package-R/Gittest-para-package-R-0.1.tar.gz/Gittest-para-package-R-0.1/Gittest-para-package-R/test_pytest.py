import requests


def buscar_avatar(usuario):
    url = f'https://api.github.com/users/{usuario}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


def test_answer():
    assert buscar_avatar('RafaRissatto') == 'https://avatars.githubusercontent.com/u/149025114?v=4'
