from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yosr_user:mypass@localhost:5432/yosr_db'
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema":"agorize"}
    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)

    def __init__(self, points):
        self.points = points
        #self.id = id


    def __repr__(self):
        return self.points
        
class Skill(db.Model):
    __tablename__ = "skills"
    __table_args__ = {"schema":"agorize"}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique=True)
    parent_id = db.Column(db.Integer)
    


    def __init__(self, name, parent_id):
        self.name = name
        self.parent_id = parent_id


    def __repr__(self):
        return self.name
        
class UserSkill(db.Model):
    __tablename__ = "skills_users"
    __table_args__ = {"schema":"agorize"}
    id = db.Column(db.Integer, primary_key=True)
    skill_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    


    def __init__(self, skill_id, user_id):
        self.skill_id = skill_id
        self.user_id = user_id


    def __repr__(self):
        return self.skill_id

# Set "homepage" to index.html
@app.route('/')
def index():

	user = User(None)
	skill = Skill(None, None)
	users_ids= user.query.all()
	parent_names = skill.query.filter_by(parent_id=None).all()
	skills_names = skill.query.all()
	return render_template('index.html',
				parent_names= parent_names, 
				skills_names=skills_names,
				users_ids= users_ids)

#returns the result of the sum /count query
@app.route('/sqlQuery', methods=['GET'])
def getQuery():
	results = db.engine.execute("with names as ( SELECT *, CASE WHEN parent_id is null THEN name ELSE ( select name from agorize.skills as s1 where s1.id = s2.parent_id) END as init_names FROM agorize.skills as s2), pc as (SELECT *, CASE 	WHEN parent_id is null THEN id ELSE parent_id END as init_id FROM agorize.skills) select 	pc.init_id as ID , names.init_names as NAME , sum(u.points) as POINTS, count(su.user_id) as USERS_COUNT from agorize.skills_users as su left join pc  on pc.id = su.skill_id left join names on names.id  = pc.id left join agorize.users as u on su.user_id = u.id group by (pc.init_id, names.init_names) Order by pc.init_id;")
	data= []
	for res in results:
		line= []
		for l in res:
			line.append(l)
		data.append(line)
	return render_template('query.html', data=data)

# Save user to database
@app.route('/user', methods=['POST'])
def addUser():
    points = 0
    if request.method == 'POST':
       points = request.form['points']
       #id = request.form['id']
       user = User(points)

       db.session.add(user)
       db.session.commit()
       return render_template('success.html')
    return render_template('index.html')

# Save user to database
@app.route('/skills', methods=['POST'])
def addSkill():
	name = ""	
	parent_id = None
	if request.method == 'POST':
	       Skill_name = request.form['Skill_name']
	       parent_name = request.form['parent_name']
	       if (parent_name == 'Aucun'):
	       		parent_id= None
	       else:
	       		parent_id = skill.query.filter_by(name= parent_name).first().parent_id
	       skill = Skill(Skill_name, parent_id)
		
	       db.session.add(skill)
	       db.session.commit()
	       return render_template('success.html')
	return render_template('index.html')

@app.route('/userskills', methods=['POST'])
def addUserSkill():
	user_ids = None	
	skill_id = None
	skill = Skill(None, None)
	if request.method == 'POST':
	       Skill_name = request.form['all_skills_names']
	       skill_id = skill.query.filter_by(name= Skill_name).first().id
	       user_ids = request.form.getlist('user_ids')
	       print (user_ids)
	       
	       for user_id in user_ids:
	       	       	user_skill = UserSkill(skill_id, user_id)
	       	       	db.session.add(user_skill)
	       	       	db.session.commit()
	       return render_template('success.html')
	return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
