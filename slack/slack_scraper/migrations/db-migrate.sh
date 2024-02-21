cd slack_scraper/migrations
alembic upgrade head
cd ../..
python -m slack_scraper.populate_db