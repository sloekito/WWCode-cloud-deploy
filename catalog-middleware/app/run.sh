export MYSQL_DATABASE_DB="catalog"
export MYSQL_DATABASE_HOST="localhost"
export MYSQL_DATABASE_USER="readonly"
export MYSQL_DATABASE_PASSWORD="readonly%%%%%%%"

cd /Users/sloekito/WWCode/WWCode-cloud-deploy/catalog-middleware/app
gunicorn app:app -b 0.0.0.0:8099
