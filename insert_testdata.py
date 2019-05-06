#!/usr/bin/python

import psycopg2


def insert():
    """ insert test data into the tables in the PostgreSQL database"""
    commands = (
    
        """ 	
        INSERT INTO agorize.users (points )
    	SELECT * FROM (VALUES (100), (200), (100), (50), (10)) foo
    	WHERE NOT EXISTS (SELECT 1 FROM agorize.users);
        """,
        
       """ 	
        INSERT INTO agorize.skills (name, parent_id)
    	SELECT * FROM (VALUES ('Football', NULL), ('Basketball',NULL), ('Foot',1), ('Basket',2), ('Soccer',1)) foo
    	WHERE NOT EXISTS (SELECT 1 FROM agorize.skills);
        """,
        
        """ 	
        INSERT INTO agorize.skills_users (skill_id, user_id)
    	SELECT * FROM (VALUES (1,1), (1,2), (3,3), (2,4), (5,5)) foo
    	WHERE NOT EXISTS (SELECT 1 FROM agorize.skills_users);
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
    insert()
    
