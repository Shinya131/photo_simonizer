import getpass

API_TOKEN = getpass.getpass('slackbot aip-token: ')

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "?"
