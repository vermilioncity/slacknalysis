FROM python:3.7

WORKDIR slack

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./slack_scraper/migrations/db-migrate.sh

CMD tail -f /dev/null