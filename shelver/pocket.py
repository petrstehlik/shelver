import requests
import flask

POCKET_API_URL = "https://getpocket.com/v3"
POCKET_API_CONSUMER_KEY = "99253-17812c14bf2e3773ac0793bb"

app = flask.Flask(__name__)


def retrieve(pocket_code: str):
    endpoint = f"{POCKET_API_URL}/get"

    response = requests.get(endpoint, params={
        "consumer_key": POCKET_API_CONSUMER_KEY,
        "access_token": pocket_code,
        "count": 10,
        "detailType": "complete",
    })

    return response.text


def authorize():
    endpoint = f"{POCKET_API_URL}/oauth/request"

    response = requests.post(endpoint, json={
        "consumer_key": POCKET_API_CONSUMER_KEY,
        "redirect_uri": "foobar"
    },
                             headers={
                                 "Content-Type": "application/json; charset=UTF-8",
                                 "X-Accept": "application/json",
                             }
    )

    response.raise_for_status()

    body = response.json()

    return body.get("code")


def do_authorize(pocket_code):
    endpoint = f"{POCKET_API_URL}/oauth/authorize"

    response = requests.post(endpoint, json={
        "consumer_key": POCKET_API_CONSUMER_KEY,
        "code": pocket_code,
    },
                             headers={
                                 "X-Accept": "application/json",
                             })

    return response


@app.route('/callback/<auth_code>')
def oauth_callback(auth_code):
    response = do_authorize(auth_code)
    print(response.text)


if __name__ == "__main__":
    code = authorize()

    print(code)
    print(f"https://getpocket.com/auth/authorize?request_token={code}&redirect_uri=http://localhost:5000/callback/{code}")
    results = retrieve(pocket_code='31e70c2c-6c7a-4390-c3c7-6e6780')

    print(results)

    app.run()

