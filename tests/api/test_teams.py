from flask import jsonify
from flask import json
from flask import request
class TestTeams:
    mock_team = {
        "name" : "Galway",
        "colour" : "maroon"
    }
    def test_get_teams(self, client, add_team):
        t = add_team(TestTeams.mock_team["name"], TestTeams.mock_team["colour"])
        response = client.get('/api/teams')
        response_obj = response.get_json()
        assert len(response_obj["items"]) == 1
        assert "Galway" == response_obj["items"][0]["name"]
        assert "maroon" == response_obj["items"][0]["colour"]
        assert response.status_code == 200

    def test_get_team_by_id(self, client, add_team):
        t = add_team(TestTeams.mock_team["name"], TestTeams.mock_team["colour"])
        response = client.get('/api/teams/'+str(t.id))
        response_obj = response.get_json()
        assert "Galway" == response_obj["name"]
        assert "maroon" == response_obj["colour"]
        assert response.status_code == 200

    def test_create_teams(self, client):
        response = client.post('/api/teams', data=json.dumps(TestTeams.mock_team), mimetype='application/json')
        assert response.status_code == 201