#!/usr/bin/python

import psycopg2

 
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """ CREATE TABLE IF NOT EXISTS agorize.users (
                id SERIAL PRIMARY KEY,
                points int NOT NULL
                )
        """,
        
        """
        CREATE TABLE IF NOT EXISTS agorize.skills (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL, 
            parent_id int 
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS agorize.skills_users (
                id SERIAL PRIMARY KEY,
                skill_id int NOT NULL,
		user_id int NOT NULL,
                FOREIGN KEY (skill_id) REFERENCES agorize.skills (id),
                FOREIGN KEY (user_id)  REFERENCES agorize.users (id)
        )
        """
        )

    conn = None

    try:
        
        # connect to the PostgreSQL server
        conn = psycopg2.connect(host="localhost",database="yosr_db", user="yosr_user", password="mypass")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
 
if __name__ == '__main__':
    create_tables()
    
