from flask import jsonify
from flask import json
from flask import request
from datetime import date

class TestEvents:
    mock_event = {
        "name" : "Kick"
    }

    mock_game = {
        "name" : "Game",
        "timestamp" : date.today()
    }

    def test_get_event_outcomes(self, client, add_outcome):
        o = add_outcome(TestEvents.mock_event["name"], "testOutcome")
        response = client.get('/api/events/'+str(o.id)+'/outcomes').get_json()
        assert len(response["items"]) == 1
        assert "testOutcome" == response["items"][0]["name"]

    def test_create_event(self, client, add_game):
        g = add_game(TestEvents.mock_game["name"], TestEvents.mock_game["timestamp"])
        TestEvents.mock_event["game_id"] = g.id
        response = client.post('/api/events', data=json.dumps(TestEvents.mock_event), mimetype='application/json')
        assert response.status_code == 201
