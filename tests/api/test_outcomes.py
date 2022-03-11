from flask import jsonify
from flask import json
from flask import request
from datetime import date

class TestOutcomes:
    mock_outcome = {
        "name" : "Turnover"
    }
    mock_event = {
        "name" : "Pass"
    }

    def test_get_outcome_by_id(self, client, add_outcome):
        o = add_outcome(TestOutcomes.mock_event["name"], TestOutcomes.mock_outcome["name"])
        response = client.get('/api/outcome/'+str(o.id))
        assert o.name == response.get_json()['name']
        assert response.status_code == 200

    def test_create_outcome(self, client, add_event):
        e = add_event(TestOutcomes.mock_event["name"])
        TestOutcomes.mock_outcome["event_id"] =  e.id
        response = client.post('/api/outcomes', data=json.dumps(TestOutcomes.mock_outcome), mimetype='application/json')
        assert response.status_code == 201
