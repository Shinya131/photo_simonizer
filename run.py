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
ENCODED_SIMONE = numpy.array([
    -0.03471003,  0.06048969,  0.03898831, -0.019677  , -0.07857664,
    -0.04628677, -0.0752786 , -0.11614025,  0.10900166, -0.1734724 ,
     0.18551701, -0.07012792, -0.18840286, -0.09499765, -0.05221178,
     0.16973352, -0.1383561 , -0.12198617, -0.07420506, -0.07455432,
     0.06258397,  0.0318348 ,  0.0201092 , -0.00498826, -0.06842905,
    -0.34316722, -0.10041932,  0.00213636,  0.07845978, -0.05689343,
    -0.09637161,  0.00214384, -0.17204411, -0.06912521,  0.04731423,
     0.08808891, -0.06334342, -0.06012471,  0.15263849, -0.02998366,
    -0.16980806, -0.00400486,  0.03599128,  0.26414692,  0.20936845,
     0.08622115, -0.01685071, -0.14988577,  0.11687909, -0.12133989,
     0.04622792,  0.12775181,  0.06242732,  0.08406319,  0.01616399,
    -0.06402029,  0.05347097,  0.12134917, -0.0868063 , -0.01145105,
     0.10900611, -0.10295628, -0.00222771, -0.05255459,  0.24936853,
    -0.01910188, -0.08370158, -0.18100081,  0.15640345, -0.1555246 ,
    -0.05046125,  0.01917581, -0.09858083, -0.11878498, -0.26430994,
     0.01231405,  0.40443799,  0.11519814, -0.16168135,  0.03131885,
    -0.0417447 , -0.01101109,  0.19580272,  0.08999944, -0.04993463,
    -0.02036044, -0.12787941,  0.01711101,  0.24577083, -0.07755674,
    -0.04943966,  0.16108698,  0.0133337 ,  0.0580669 ,  0.06547343,
     0.01180343, -0.12288905,  0.08547792, -0.13815592, -0.0302924 ,
     0.11390147, -0.06797438,  0.02413653,  0.15240298, -0.09359212,
     0.17448479, -0.00893746,  0.06307185,  0.09587732,  0.01418718,
    -0.15366966, -0.12663612,  0.11951894, -0.18301611,  0.15891542,
     0.16315365,  0.10963488,  0.10929712,  0.11771469,  0.13423193,
    -0.01301533, -0.00191968, -0.21294612, -0.03423879,  0.07071996,
    -0.00141306,  0.1125031 ,  0.02380354
])

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
    for face in faces:
        distance = face_recognition.face_distance([ENCODED_SIMONE], face)[0]
        simo_score = 1 - distance

        if simo_score >= 0.7:
            message.reply('ｼﾓーﾈ!')
        elif simo_score >= 0.6:
            message.reply('ｼﾓーﾈ...?')
        else:
            message.reply('非ﾓーﾈ...')

        message.send('ｼﾓさ{}%'.format(round(simo_score*100, 0)))


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
