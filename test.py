import sys
import unittest
import psycopg2


from create_tables import create_tables 



class MyTests(unittest.TestCase):
	#test that the three tables exist
	def test_create_table(self):
		con = None
		try:
	    		con = psycopg2.connect(host="localhost",database="yosr_db", user="yosr_user", password="mypass")
	    		cur = con.cursor()
	    		for table_name in ['skills', 'users', 'skills_users']:
	    			cur.execute('SELECT EXISTS( SELECT 1 from agorize.{})'.format(table_name))
	    			ver = cur.fetchone()[0]
	    			self.assertEqual(ver, True)
		except psycopg2.DatabaseError as e:
	    		print (e)
	    		sys.exit(1)
		finally:
	    		con.close()
	
	#test that each child is not a parent    		
	def test_parent_child(self):
		con = None
		try:
	    		con = psycopg2.connect(host="localhost",database="yosr_db", user="yosr_user", password="mypass")
	    		cur = con.cursor()
	    		cur.execute('SELECT id from agorize.skills where parent_id is not null;')
	    		children = cur.fetchall()
	    		for  child in children: 
	    			cur.execute('SELECT 1 WHERE NOT EXISTS (SELECT id  from agorize.skills where parent_id= {});'.format(
	    															str(child[0])))
	    			ver = cur.fetchone()[0]
	    			self.assertEqual(ver, True)
	    			
		except psycopg2.DatabaseError as e:
	    		print (e)
	    		sys.exit(1)
		finally:
	    		con.close()
	    		
	
	    		
	
if __name__ == '__main__':
    unittest.main()
