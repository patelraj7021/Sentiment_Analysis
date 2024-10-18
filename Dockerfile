FROM amd64/python:3.12-bookworm

COPY . /sentiment_analysis

WORKDIR /sentiment_analysis

RUN pip install -r requirements.txt

RUN playwright install

RUN playwright install-deps

CMD ["bash", "scanning.sh"]