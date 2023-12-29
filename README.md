# Flask-Streamlit-MySQL-User-Authentication
I am writing for partly for my project -- achieve user authentication using flask as backend, streamlit front end and MySQL as database.

```python
pip install flask flask-sqlalchemy flask-login pymysql streamlit

```

## Get MySQL 
in the terminal:
- log in mysql
```
mysql -u root -p
```
- type in password, remember to change that in app.py, I name my database "test" by the way.
- handy commands to locate your database and its content
```
SHOW DATABASES;
USE test;
SHOW TABLES;
```
- exit
```
EXIT
```

## Run flask code
```
python3 app.py
```

# Run streamlit code
```
streamlit run streamlit_app.py
```
