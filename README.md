# Implementing a skills python app using Postgres and Flask

# Step one: Install the requirements
To implement this app, I have used Python3. 
1. Install PostgreSQL in Linux

`sudo apt-get install postgresql postgresql-contrib`

I create a superuser (here called yosr) for PostgreSQL, create a database yosr_db and grant all previliges to my user.

`
$ sudo -u postgres psql
`\
`postgres=# CREATE ROLE yosr_user WITH SUPERUSER CREATEDB CREATEROLE LOGIN ENCRYPTED PASSWORD 'mypass';
`\
`
postgres=# CREATE DATABASE yosr_db;
`\
`
postgres=# GRANT ALL PRIVILEGES ON DATABASE yosr_db TO yosr_user;
`\
`
postgres=# \c yosr_db;
`\
`
postgres=# create schema agorize;
`\
`
postgres=# ALTER SCHEMA agorize OWNER TO yosr_user;
`

2. Make sure you install Flask and flask_sqlalchemy.

# step two: Create the test data
1. First things first, you need to create the tables if they do not exist. For this, I have written a python script that you can run in your terminal as follow:
`
$ python3 create_tables.py
`
To check it worked, you can go back to your postgres shell and type the command below to show the created tables of our schema.
`
yosr_db=# \dt+ agorize.*
`

2. Now we can fill our tables with some test data.
`$python3 insert_testdata.py`

# step three: Run the app
1. We have used flask REST API.
`$ python3 app.py`
You should see a msg stating that the app is running on http://127.0.0.1:5000/ 
2. Use your fav browser to go to Running on http://127.0.0.1:5000/
3. At this stage, you can only add a new user by adding his points (the Id will be generated automatically) or add a new skill or associate a skill to one or multiple users. 

#step four: Run the unit tests:
I didn't cover all the possible test cases. I implemented two tests with unittest python library: the first one to verify the creation of the tables and the second one to test that each child skill is not a parent.   
(Other test scenarios: test the types of the input, test the output of the query) 


