from flask import jsonify
from flask import json
from flask import request
class TestEvents:
    mock_event = {
        "name" : "Kick"
    }

    def test_get_event_by_id(self, client, add_event):
        e = add_event(TestEvents.mock_event["name"])
        response = client.get('/api/events/'+str(e.id))
        assert "Kick" in response.get_json()['name']
        assert response.status_code == 200

    def test_get_event_outcomes(self, client, add_outcome):
        o = add_outcome(TestEvents.mock_event["name"], "testOutcome")
        response = client.get('/api/events/'+str(o.id)+'/outcomes').get_json()
        assert len(response["items"]) == 1
        assert "testOutcome" == response["items"][0]["name"]

    def test_create_event(self, client):
        response = client.post('/api/events', data=json.dumps(TestEvents.mock_event), mimetype='application/json')
        assert response.status_code == 201