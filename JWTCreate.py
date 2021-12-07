import json
import jwt as pyjwt
import requests
import urllib
from datetime import datetime, timedelta
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
#ログレベルを設定
logger.setLevel(20)
#ログをコンソール出力するための設定
sh = StreamHandler()
logger.addHandler(sh)

# グローバル変数
DOMAIN_ID = "400008279"
API_ID = "jp1XkNduascZS"
SERVER_API_CONSUMER_KEY = "3maZRxwjXuIgtFsGLY84"
SERVER_LIST_ID = "e1764a189ef94e858bc20bf2795c0637"
SERVER_LIST_PRIVATEKEY = "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCvlMUV4NYT4SjRzmAat5malrf4Jd0xFA6PSS/hH9itFMZ/HgImFujn6JzUzck9rC26Dq55AQ0ulzJ9PcdI8DITpvtgqr1g43QY/nRjX0c+YjxqrVoQ954m6fQXtBvoMG1sJDRDqyzh8dJYQEpsSP+MptL2ZYZayGCXakJBUjm2r8ETdWj0J7kbTaYMa6ZWX+ItflbjnBqJdCa+ViYc7BstKD7pBLAnkIeOyKpaETGiA5JpLQNPv4RJFbNpqzB3HUvIlFBnbmlICqkOhktoU4X97W0gPDTJbzWwJOYNhk1xug/tL7uYXshPJLJwQyw/p4L8wQKWQEqcW3xeveXUNF2jAgMBAAECggEAEZKDEwh4hG7RZgYQijv7zIPvD4/Cjmnidyas+wvz5IaiwxAeyO8cCjG2mHmr/VchEHDtt0CKsDIDpJMtQbiAWoUovWj5IRxCf0ngHh3oBG9Sep601+PgWSaq/kBRVrCaEuugq3ETQd2w3pI4oJPBt7LuhChvBODvAdhpnx36lrTfYX4XYt038BQC9zl84/vfk0+6reaQmkjGgPMzp4DXtEcdWlnJ0BT057uBK0/VVI9FvdkfgwpFx4PmbgbXNXE8nmERrLvnfWTiTlzPHeihrTDf0gYMQ2kvNHBdOVxQEpO1R1z07e9UfokrqMKUatXikoduqyfiO0z+ioBgc3ZyGQKBgQD2yLQu7wONCeHkrQNvsuMpiov3RAuQbivJ/ZtgAoRIKE5RRQQ9SlTrbd5nLJq9NowsbcavjqkNyPYVu6Dx1vovj9fijSEIOAfIlW6rIzfsGD3h5fkbL2QMjfDxF7BDkN453LlqV9wlDmidqB2z5xkR7yARlQHWjPu1xYSIDxfXTwKBgQC2I1rQ1cYd43H1oAYMMbkUT8LfvD4MeUrAXnZyeP7nE2qqzXJLNuUAhtip36LYomXIr1+3jGe7KcMJwflV1mk002LuMTNCVYJ6jiAJs7DKkzFvtxYWOiroR6ZeMmPln5vLBBSS8byouOwUtNsmP7ioEeH/TliqqANRru2cOYr/bQKBgG/87CdQN2BNV8EZ8jFCEGvNf26Z5lWIaT6kY1nSSo0kHUYr95yImrirhv1y9FVg54NR3ZPVPUoQI/wAxSx5zda/g8w/FvpP0thnV2058iqlZY+ZeM2pV9GKqAgAI/DFUNMZItrrO+9k9nx0yeXVvT6yMO9JmyftmlwGYfoMP1lpAoGBAJYWuj5++pwkkgL7VCB2VPJ067wczfDPfpbZALhCFqNqb6rCU53BZaIyfJY3cGUeJcvjIHgLXmtv9YWz73gZkGZ0jwCDUJ8oAbZmKeZ0yYmVE9bgQ3YbhsIUUPcshP9ysBnyidWxGGrcv8YsZq61McBlxBrzf8NZYirMgIcNMApdAn8LORr/qdcrgT5kmS1gu7d6WEbEJIGhpb1wSWYBVXyUZJjXPUOteOi27kGk/7ixbRrlHKpZr66foLH+GwycxPHGZRWuvllBWvhqp0DcHqbejzOGTbmPRq59fTaDhUoHhcyB423REMucrssSRzlvB7ejyOZ7xoDkrK/RS3wT0EJe\n-----END PRIVATE KEY-----"
BOT_NO = "2866383"
LINE_ID = "kondo.toyohisa@test-457"

def create_jwt():
    iat = int(datetime.now().timestamp())
    exp = int((datetime.now() + timedelta(minutes=30)).timestamp())
    secret = SERVER_LIST_PRIVATEKEY

    json_claim_set = {
        "iss": SERVER_LIST_ID,
        "iat": iat,
        "exp": exp
    }
    json_header = {"alg": "RS256", "typ": "JWT"}

    jwt = pyjwt.encode(json_claim_set, secret, algorithm="RS256", headers=json_header)

    logger.info({
        "action": "create jwt",
        "status": "success",
        "message": "JWT:" + jwt
    })
    return jwt


def get_server_token(jwt):
    url = 'https://auth.worksmobile.com/b/' + API_ID + '/server/token'
    headers = {
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    form_data = {
        "grant_type" : urllib.parse.quote("urn:ietf:params:oauth:grant-type:jwt-bearer"),
        "assertion" : jwt
    }

    try:
        response = requests.post(url=url, headers=headers, data=form_data)
        access_token = json.loads(response.text)["access_token"]
        logger.info({
            "action": "get access token",
            "status": "success",
            "message": "access_token:" + access_token
        })
        return access_token
    except:
        logger.info({
            "action": "get access token",
            "status": "fail",
            "message": response.text
        })
        return response

def api(url, payload, access_token):
    headers = {
        'Content-Type' : 'application/json; charset=UTF-8',
        'consumerKey': SERVER_API_CONSUMER_KEY,
        'Authorization': 'Bearer ' + access_token,
    }
    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        logger.info({
            "action": "api request",
            "status": "success",
            "message": response.text
        })
    except:
        logger.info({
            "action": "api request",
            "status": "fail",
            "message": response.text
        })

def register_domain(access_token):
    url = 'https://apis.worksmobile.com/r/' + API_ID + '/message/v1/bot/' + BOT_NO + '/domain/' + DOMAIN_ID
    payload = {
        "usePublic": True,
        "usePermission": False,
    }
    api(url, payload, access_token)

def send_message(access_token):
    url = 'https://apis.worksmobile.com/r/' + API_ID + '/message/v1/bot/' + BOT_NO + '/message/push'
    payload = {
        "accountId": LINE_ID,
        "content": {
            "type": "text",
            "text": "aaaaaaaa",
        }
    }
    api(url, payload, access_token)

if __name__ == "__main__":
    jwt = create_jwt()
    access_token = get_server_token(jwt)
    register_domain(access_token)
    send_message(access_token)
