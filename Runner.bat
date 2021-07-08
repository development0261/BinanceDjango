@ECHO OFF
start cmd.exe /C "cd venv/Scripts && activate && cd .. && cd .. && python manage.py runserver"
start chrome http://127.0.0.1:8000/
