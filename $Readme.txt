Steps to launch flask server:
-Ensure your folder contains two files:
-the web launch batch file (.bat)
-virtual folder with script file (containing activate and acitivate.bat)

For web launch batch file:
cd "C:\Program Files\MySQL\MySQL Workbench 8.0 CE"   ------> Enter your equivalent path that contains your workbench
start MySQLWorkbench.exe    ---> starts your workbench automatically on starting the server 
cd C:\my_flask\virtual\Scripts     -----> Enter the path only until your scripts folder 
call C:\my_flask\virtual\scripts\activate  ------> Enter the path in which your activate file is present (ensure all files are in the same directory)

cd C:\my_flask   -----> Enter the root path where your web launch batch file is present 

set FLASK_ENV=development
set FLASK_APP=app.py    ---> set your flask app to the respective app.py file
flask run
pause

Additional steps:

Activate file:
-Set Virtual Environment variable to respective path where virtual folder is present 
 Eg: VIRTUAL_ENV="C:\my_flask\virtual

Activate.bat file:
-Set Virtual Environment variable to respective path where virtual folder is present 
Eg: set VIRTUAL_ENV=C:\my_flask\virtual

After completing, launch the web launch.bat file to start the flask server 

Pyvenvconf:
- in virtual folder, find file called pyvenv.conf
-set the configuration to the path where your python 3.9 resides 
eg: home = C:\Users\varsh\AppData\Local\Programs\Python\Python39

Database Setup:
-Download Dbeaver.io
-Establish your mySQL connection
-Create Database with schema name as financeapp
-Create tables using the DDL given in the root folder 
Database_Definition_DDL.sql