set -e  

python manage.py check_migrations

python manage.py migrate

python manage.py collectstatic --noinput

