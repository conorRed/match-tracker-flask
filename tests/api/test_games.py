from flask import jsonify
from flask import json
from flask import request
from conftest import make_headers

class TestGames:
    def test_create_game(self, client, get_token, add_verified_user):
        request = client.post('/api/games', headers=make_headers(get_token),
                json = {"name" : "game 1"})
        assert request.status_code == 201
        assert request.get_json() == ""

    def test_get_games(self, client, get_token, add_verified_user):
        request = client.get('/api/games', headers=make_headers(get_token))
        assert request.status_code == 200
