#---------------------------------------------------------
# Superset specific config
#---------------------------------------------------------
ROW_LIMIT = 50000

SUPERSET_WEBSERVER_PORT = 8088
#---------------------------------------------------------

#---------------------------------------------------------
# Flask App Builder configuration
#---------------------------------------------------------
# secret key

import os

SECRET_KEY = '\2\1badthingshappened\1\2\e\y\y\h'

# The SQLAlchemy connection string to your database backend
# This connection defines the path to the database that stores your
# superset metadata (slices, connections, tables, dashboards, ...).

base_url = 'postgresql+psycopg2://{username}:{password}@{service}:{port}/{name}'
SQLALCHEMY_DATABASE_URI = base_url.format(username=os.getenv('POSTGRES_USER'),
                                          password=os.getenv('POSTGRES_PASSWORD'),
                                          service=os.getenv('POSTGRES_SERVICE'),
                                          port=os.getenv('POSTGRES_PORT'),
                                          name=os.getenv('POSTGRES_DB'))

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set this API key to enable Mapbox visualizations
MAPBOX_API_KEY = ''

FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
    'ALLOW_ADHOC_SUBQUERY':True,
    "DASHBOARD_NATIVE_FILTERS": True
}