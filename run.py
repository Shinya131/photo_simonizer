"""Channelに投稿された画像にｼﾓーﾈが写っているか判定するBot
"""

import tempfile
import shutil
import numpy
import requests
import face_recognition
import slackbot_settings
from slackbot.bot import listen_to
from slackbot.bot import Bot

IMAGE_FILE_TYPES = ['gif', 'png', 'jpg', 'jpeg']
ENCODED_SIMONE_PATH = './encoded_simone.csv'

# 起動時の通知
POST_START_MESSAGE = False
START_MESSAGE_POST_CHANNEL = 'trans_m4'
START_MESSAGE = 'ﾋﾟｺｯ(起動音)'


@listen_to('(.*)')  # 全投稿をリッスン
def detect_simone(message, _):
    # 画像付いてなかったら何もしない
    if not __has_image(message):
        return

    image = __download_image(message)
    faces = face_recognition.face_encodings(image)

    # 顔写ってなかったら何もしない
    if len(faces) <= 0:
        return

    # 顔写ってたら判定
    encoded_simone = __load_encoded_simone()
    for face in faces:
        distance = face_recognition.face_distance([encoded_simone], face)[0]
        simo_score = 1 - distance

        if simo_score >= 0.7:
            message.reply('ｼﾓーﾈ!')
        elif simo_score >= 0.6:
            message.reply('ｼﾓーﾈ...?')
        else:
            message.reply('非ﾓーﾈ...')

        message.send('ｼﾓさ{}%'.format(round(simo_score*100, 0)))


def __load_encoded_simone():
    try:
        return numpy.loadtxt(ENCODED_SIMONE_PATH, delimiter=',')
    except IOError:
        mes = 'ｼﾓーﾈの特徴量ファイル{}が読み込めなかった'
        mes = mes.format(ENCODED_SIMONE_PATH)
        raise IOError(mes)


def __has_image(message):
    """messageに画像が付いてるか判定
    """
    if 'file' in message.body:
        return message.body['file']['filetype'] in IMAGE_FILE_TYPES


def __download_image(message):
    """messageについてる画像をダウンロードしてnumpy.ndarray化
    """
    def request_image():
        """画像ダウンロード
        """
        url = message.body['file']['url_private']
        header = {'Authorization': 'Bearer %s' % slackbot_settings.API_TOKEN}

        res = requests.get(url, headers=header, stream=True)

        if not res.status_code == 200:
            raise RuntimeError('なんか画像ダウンロード出来なかった')

        return res

    def generate_tempfile():
        """ダウンロードした画像の一時保存先pathを生成
        """
        filetype = message.body['file']['filetype']
        return tempfile.NamedTemporaryFile(suffix='.'+filetype).name

    def save_to_tempfile(_tempoutput):
        """添付ファイルに保存
        """
        f = open(tempoutput, 'wb')
        try:
            shutil.copyfileobj(response.raw, f)
        finally:
            f.close()

    response = request_image()
    tempoutput = generate_tempfile()
    save_to_tempfile(tempoutput)

    image = face_recognition.load_image_file(tempoutput)

    assert isinstance(image, numpy.ndarray), "何かに失敗"
    return image


def __post_start_message(_bot):
    """所定のチャンネルに起動時メッセージを投稿する
    """
    _bot._client.send_message(START_MESSAGE_POST_CHANNEL, START_MESSAGE)


if __name__ == "__main__":
    print('start slackbot')
    bot = Bot()

    if POST_START_MESSAGE:
        __post_start_message(bot)

    bot.run()
