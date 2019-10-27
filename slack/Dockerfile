FROM python:3.7

WORKDIR slack

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD tail -f /dev/null