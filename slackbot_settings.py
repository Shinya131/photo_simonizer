import os

API_TOKEN_ENV = "SLACKBOT_API_TOKEN"
API_TOKEN_FILE = './api_token.txt'


def read_api_token():
    # 環境変数から取得を試みる
    api_token = os.getenv(API_TOKEN_ENV, None)

    if api_token is not None:
        return api_token

    # ファイルから読み込みを試みる
    if os.path.exists(API_TOKEN_FILE):
        with open(API_TOKEN_FILE, 'r') as f:
            api_token = f.read().replace('\n', '')

        return api_token

    # どっちにも無かった
    mes = '{}にapi_tokenを書いたテキストファイルを置くか、'\
          '環境変数{}にapi_tokenをセットしてください'

    raise RuntimeError(mes.format(API_TOKEN_FILE, API_TOKEN_ENV))


# slack-botのAPI-TOKEN
API_TOKEN = read_api_token()

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "?"
