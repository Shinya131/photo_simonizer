FROM python:3.6
ENV PYTHONUNBUFFERED 1

# workdir作成
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# aptせざるを得ないライブラリ群
RUN apt-get update -y
RUN apt-get install cmake -y

# pip install
ADD requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

# source codeを仮想マシンに追加
ADD . /usr/src/app/
