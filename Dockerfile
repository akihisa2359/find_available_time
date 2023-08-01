# ベースイメージとしてPython 3.9とGoogle Chromeを含むDebian Busterイメージを使用
FROM python:3.9-slim-buster

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y wget unzip

# Chromeの依存ライブラリをインストール
RUN apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

# Chromeをダウンロードしてインストール
RUN wget -q -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i /tmp/google-chrome.deb || apt-get -fy install && \
    rm -f /tmp/google-chrome.deb

# ChromeDriverをダウンロードしてインストール
RUN wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/101.0.4951.41/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# ソースコードをコンテナにコピー
COPY . /app

# 作業ディレクトリを設定
WORKDIR /app

# RUN pip install --no-cache-dir -r  requirements.txt
RUN pip install -r ./requirements.txt

CMD ["/bin/bash"]
