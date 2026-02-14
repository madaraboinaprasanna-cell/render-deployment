@echo off
echo Starting AstraLearn Platform...

echo Installing required packages...
pip install Pillow

echo Applying database migrations...
python manage.py makemigrations accounts groups collaborate learning
python manage.py migrate

echo Creating superuser (if not exists - manual step usually, skipping automatic creation)...
echo To create superuser run: python manage.py createsuperuser

echo Starting server...
start http://127.0.0.1:8000/
python manage.py runserver
pause
