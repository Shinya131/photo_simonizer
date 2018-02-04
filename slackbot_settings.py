import os

API_TOKEN_FILE = './api_token.txt'


def read_api_token():
    assert os.path.exists(API_TOKEN_FILE), \
        'カレントディレクトリにapi_tokenを書いたテキストファイル(api_token.txt)を置いてください'

    with open(API_TOKEN_FILE, 'r') as f:
        api_token = f.read()

    return api_token.replace('\n', '')


API_TOKEN = read_api_token()

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "?"
