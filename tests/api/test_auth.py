from flask import jsonify
from flask import json
from flask import request
from app.models import User
class TestAuth:
    mock_user = {
        "email" : "Galway",
        "password" : "maroon"
    }
    
    def test_create_user(self, client, access_token_for_email):
        response = client.post('/api/signup', data=json.dumps(TestAuth.mock_user), mimetype='application/json')
        assert "" != response.get_json()["access_token"]
        assert response.status_code == 201
        assert User.query.filter_by(email=TestAuth.mock_user["email"]).scalar() != None

    def test_login(self, client, add_user):
        user = add_user(TestAuth.mock_user["email"], TestAuth.mock_user["password"])
        response = client.post('/api/login', data=json.dumps(TestAuth.mock_user), mimetype='application/json')
        assert response.status_code == 201

