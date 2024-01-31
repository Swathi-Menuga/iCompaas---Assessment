from flask import Flask, request, jsonify
import re
import pytest

app = Flask(__name__)

#API Endpoint Implementation:

def is_sanitized(input_string):
    sql_injection_chars = re.compile(r'(;|--|\'|"|\\)')
    return not bool(sql_injection_chars.search(input_string))

@app.route('/v1/sanitized/input/', methods=['POST'])
def check_sanitization():
    try:
        data = request.get_json()

        if not data or 'input' not in data:
            return jsonify({'error': 'Bad Request'}), 400

        input_string = data['input']

        if is_sanitized(input_string):
            result = {'result': 'sanitized'}
        else:
            result = {'result': 'unsanitized'}

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Unit tests using pytest

@pytest.fixture
def app_instance():
    app.testing = True
    return app.test_client()

# Test case for sanitized input
def test_sanitized_input(app_instance):
    payload = {'input': 'valid input'}
    response = app_instance.post('/v1/sanitized/input/', json=payload)
    assert response.status_code == 200
    assert response.json == {'result': 'sanitized'}

# Test case for unsanitized input
def test_unsanitized_input(app_instance):
    payload = {'input': 'some input with SQL injection --'}
    response = app_instance.post('/v1/sanitized/input/', json=payload)
    assert response.status_code == 200
    assert response.json == {'result': 'unsanitized'}

# Test case for invalid payload
def test_invalid_payload(app_instance):
    response = app_instance.post('/v1/sanitized/input/', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'Bad Request'}



