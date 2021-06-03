from flask import jsonify
from flask import json
from flask import request
class TestPlayers:
    mock_team = {
        "name" : "Galway",
        "colour" : "maroon"
    }
    mock_player = {
        "name" : "Player A",
        "number" : 1
    }
    def test_get_player(self, client, add_team, add_player):
        t = add_team(TestPlayers.mock_team["name"], TestPlayers.mock_team["colour"])
        p = add_player(t.id, TestPlayers.mock_player["name"], TestPlayers.mock_player["number"])
        response = client.get('/api/teams/'+str(t.id)+'/players')
        response_obj = response.get_json()
        assert response.status_code == 200
        assert len(response_obj["items"]) == 1
        assert TestPlayers.mock_player["name"] == response_obj["items"][0]["name"]
        assert TestPlayers.mock_player["number"] == response_obj["items"][0]["number"]


    def test_create_player(self, client, add_team):
        t = add_team(TestPlayers.mock_team["name"], TestPlayers.mock_team["colour"])
        TestPlayers.mock_player["team_id"] = t.id
        response = client.post('/api/player', data=json.dumps(TestPlayers.mock_player), mimetype='application/json')
        assert response.status_code == 201

    def test_create_players(self, client, add_team):
        players = []
        t = add_team(TestPlayers.mock_team["name"], TestPlayers.mock_team["colour"])
        players = []
        for i in range(0, 10):
            players.append({"name" : "Player A", "number" : i, "team_id": t.id})
        response = client.post('/api/players', data=json.dumps(players), mimetype='application/json')
        assert response.status_code == 201