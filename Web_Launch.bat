cd "C:\Program Files\MySQL\MySQL Workbench 8.0 CE"
start MySQLWorkbench.exe
cd C:\my_flask\virtual\Scripts
call C:\my_flask\virtual\scripts\activate

cd C:\my_flask

set FLASK_ENV=development
set FLASK_APP=app.py
flask run
pause
