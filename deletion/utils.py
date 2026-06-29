import requests

def login_and_get_token(email, password):
    url = 'https://zahraa.cloider.com/api/accounts/login/'
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json().get("token")
