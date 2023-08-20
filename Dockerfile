FROM --platform=linux/amd64 python:3.9-buster

# 必要なツールのインストール
RUN apt-get update && apt-get install -y \
  wget \
  unzip \
  gnupg \
  curl \
  libgconf-2-4 \
  libnss3 \
  libxi6 \
  libgdk-pixbuf2.0-0 \
  libasound2 

# Google ChromeとChromeDriverのインストール
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/115.0.5790.170/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip -d /usr/bin && \
    rm chromedriver-linux64.zip

# ソースコードをコンテナにコピー
COPY . /app

# 作業ディレクトリを設定
WORKDIR /app

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r ./requirements.txt

# 実行時のデフォルトコマンドを指定
CMD ["/bin/bash"]