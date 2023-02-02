import json
from random import sample
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import time
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user #here
from flask_wtf import FlaskForm #here
from wtforms import StringField, PasswordField, SubmitField #here
from wtforms.validators import InputRequired, Length, ValidationError #here
from flask_bcrypt import Bcrypt #here


app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) #here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sprintboard.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #here
app.config['SECRET_KEY'] = 'thisisasecretkey' #here

#here
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#endhere

#here
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')
#endhere

#edited
class Sprinttable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SprintName = db.Column(db.String(200), nullable=False)
    Taskid = db.Column(db.String(200), nullable=True)
    Taskdetail = db.Column(db.String(200), nullable=False)
    Assignee = db.Column(db.String(200), nullable=False)
    Sprintstatus = db.Column(db.String(200), nullable=False)
    EstimatedTime = db.Column(db.Integer, nullable=False)
    StartTime = db.Column(db.String(200), nullable=False)
    EndTime = db.Column(db.String(200), nullable=False)
    Timespent = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #added 13/10/2022
    #tasks = db.relationship('tasksinsprint', backref = 'sprinttable')
   
    
    def __repr__(self):
        return '<SprintTask %r>' % self.id + self.Taskid
#edited

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Type = db.Column(db.String(200), nullable=False)
    Tag = db.Column(db.String(200), nullable=False)
    Story_Point = db.Column(db.String(200), nullable=False)
    Priority = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
 
    def __repr__(self):
        return '<Task %r>' % self.id
#################################################
class tasksinsprint(db.Model):
    uniqueid = db.Column(db.Integer, primary_key=True)
    #sprint_id = db.Column(db.Integer, db.ForeignKey('sprinttable.id'))
    sprint_id = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.String(200), nullable=False)
    Name = db.Column(db.String(200), nullable=False)
    Type = db.Column(db.String(200), nullable=False)
    Tag = db.Column(db.String(200), nullable=False)
    Story_Point = db.Column(db.String(200), nullable=False)
    Priority = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    StartTime = db.Column(db.String(200), nullable=False)
    EndTime = db.Column(db.String(200), nullable=False)
    Timespent = db.Column(db.String(200), nullable=False)
    Storypointforthetask = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return '<SprintTask %r>' % self.id + self.Taskid


class membersinproject(db.Model):
    uniqueid = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
##########

# @app.route('/', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         Nametoadd = request.form["name"]
#         Typetoadd = request.form["Type"]
#         Tagtoadd = request.form["Tag"]
#         Storypointtoadd = request.form["product"]
#         Prioritytoadd = request.form["Prority"]
#         new_task = Todo(Name=Nametoadd, Type=Typetoadd, Tag=Tagtoadd, Story_Point=Storypointtoadd, Priority=Prioritytoadd)
#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect(url_for('dashboard'))  #here
#         except:
#             return "Error"    
#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template("Dashboard.html", tasks=tasks)


#Redirect to add page



@app.route('/')
#here
def home():
    return render_template('home.html')  #newhtml
#endhere
@app.route('/dashboard') #here
def dashboard(): 
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("Dashboard.html", tasks=tasks)

#here
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form) #new login.html

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form) #new register.html

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#endhere

#here 
@app.route('/sprintboard.html/<int:id>', methods=['GET', 'POST'])
def to_sprintboard(id): 
    #13/10/2022
    if request.method == "POST": 
        #edit sprint here
        tasks = Todo.query.order_by(Todo.date_created).all()
        sprintdetail = Sprinttable.query.get_or_404(id)
        taskinsprint =  db.session.query(tasksinsprint).filter(tasksinsprint.sprint_id==id)   
        return render_template("sprintboard.html", tasks=tasks, taskinsprint=taskinsprint, sprintdetail=sprintdetail)
    sprintdetail = Sprinttable.query.get_or_404(id)
    taskinsprint =  db.session.query(tasksinsprint).filter(tasksinsprint.sprint_id==id)  
    return render_template("sprintboard.html", taskinsprint=taskinsprint, sprintdetail=sprintdetail, sprintnumber=id)

#endhere

@app.route("/start_task_in_sprint/<int:id>/<int:sprintid>")
def start_task_in_sprint(id, sprintid):
    task_to_start = tasksinsprint.query.get_or_404(id)
    temp = time.gmtime()
    task_to_start.StartTime = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])+' '+str(temp[3])+':'+str(temp[4])+':'+str(temp[5])
    task_to_start.Status = "In_progress"
    db.session.commit()
    return redirect(url_for('to_sprintboard', id=sprintid)) 

@app.route("/end_task_in_sprint/<int:id>/<int:sprintid>")
def end_task_in_sprint(id, sprintid):
    task_to_end = tasksinsprint.query.get_or_404(id)
    try:
        temp = time.gmtime()
        task_to_end.EndTime = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])+' '+str(temp[3])+':'+str(temp[4])+':'+str(temp[5])
        task_to_end.Status = "Completed"
        dt1 = datetime.strptime(task_to_end.StartTime, "%Y/%m/%d %H:%M:%S")
        dt2 = datetime.strptime(task_to_end.EndTime, "%Y/%m/%d %H:%M:%S")
        delta = dt2 - dt1
        task_to_end.Timespent = f' {delta.days} days {delta.seconds} seconds'
        db.session.commit()
        return redirect(url_for('to_sprintboard', id=sprintid)) 
    except:
        return "problem when ending"




@app.route('/sprintboardTable.html', methods=['GET', 'POST'])
def to_sprintboard_table(): 
    # if request.method == 'POST': 
    #     #adding new sprint
    #     # SprintNametoadd = request.form["sprintname"]
    #     # Starttimetoadd = "-"
    #     # Endtimetoadd = "-"
    #     # Timespenttoadd = "-"
    #     # Taskidtoadd = request.form["Taskid"]
    #     # Taskdetailtoadd = request.form["Taskdetail"]
    #     # Assigneetoadd = request.form["assignee"]
    #     # Sprintstatustoadd = "inactive"
    #     # EstimatedTimetoadd = request.form["Estimatedtime"]

    #     # new_sprint = Sprinttable(SprintName=SprintNametoadd, Taskid=Taskidtoadd, Taskdetail=Taskdetailtoadd, Assignee=Assigneetoadd, Sprintstatus=Sprintstatustoadd, EstimatedTime=EstimatedTimetoadd, StartTime=Starttimetoadd,EndTime=Endtimetoadd, Timespent=Timespenttoadd)

    #     try:
    #         #db.session.add(new_sprint)
    #         #db.session.commit()
    #         tasks = Todo.query.order_by(Todo.date_created).all()
    #         tasks2 = Sprinttable.query.order_by(Sprinttable.id).all()
        
    #         return render_template("sprintboardTable.html", tasks=tasks, tasks2=tasks2)
        
    #     except:
    #         return 'issue adding to sprinboardtable'
    # else:
    tasks = Todo.query.order_by(Todo.date_created).all()
    tasks2 = Sprinttable.query.order_by(Sprinttable.date_created).all()
        
    return render_template("sprintboardTable.html", tasks=tasks, tasks2=tasks2)




@app.route('/add', methods=['GET', 'POST'])
def add_html(): 
    if request.method == 'POST': 
        Nametoadd = request.form["name"]
        Typetoadd = request.form["Type"]
        Tagtoadd = request.form["Tag"]
        Storypointtoadd = request.form["product"]
        Prioritytoadd = request.form["Prority"]
        new_task = Todo(Name=Nametoadd, Type=Typetoadd, Tag=Tagtoadd, Story_Point=Storypointtoadd, Priority=Prioritytoadd)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('dashboard'))  #here
        except:
            return "Error"    
    else:
        return render_template('add.html')

#updated
# @app.route('/sprintboard', methods=['GET', 'POST'])
# def to_sprint(): 
#     if request.method == 'POST': 
#         #adding new sprint
#         SprintNametoadd = request.form["nameofsprint"]
#         Starttimetoadd = request.form["StartDate"]
#         Endtimetoadd = request.form["EndDate"]
#         Timespenttoadd = "-"
#         Taskidtoadd = request.form["Taskid"]
#         Taskdetailtoadd = request.form["Taskdetail"]
#         Assigneetoadd = request.form["assignee"]
#         Sprintstatustoadd = request.form["Status"]
#         EstimatedTimetoadd = '-'

#         new_sprint = Sprinttable(SprintName=SprintNametoadd, Taskid=Taskidtoadd, Taskdetail=Taskdetailtoadd, Assignee=Assigneetoadd, Sprintstatus=Sprintstatustoadd, EstimatedTime=EstimatedTimetoadd, StartTime=Starttimetoadd,EndTime=Endtimetoadd, Timespent=Timespenttoadd)

#         try:
#             db.session.add(new_sprint)
#             db.session.commit()
#             return redirect(url_for('to_sprint'))
        
#         except:
#             return 'issue adding to sprinboard'

#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         tasks2 = Sprinttable.query.order_by(Sprinttable.date_created).all()
#         return render_template("sprintboardTable.html", tasks=tasks, tasks2=tasks2)
#added
@app.route("/delete_sprint/<int:id>")
def delete_sprint(id):
    sprint_to_delete = Sprinttable.query.get_or_404(id)
    #13/10/2022
    alltasksinthatsprint = db.session.query(tasksinsprint).filter(tasksinsprint.sprint_id==id) 
    try:
        db.session.delete(alltasksinthatsprint)
        db.session.delete(sprint_to_delete)
        db.session.commit()
        return redirect('/sprintboardTable.html')
    except:
        return "problem when editing"

#added
@app.route("/start_sprint/<int:id>")
def start_sprint(id):
    sprint_to_start = Sprinttable.query.get_or_404(id)
    try:
        temp = time.gmtime()
        sprint_to_start.StartTime = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])+' '+str(temp[3])+':'+str(temp[4])+':'+str(temp[5])
        sprint_to_start.Sprintstatus = "In progress"
        db.session.commit()
        return redirect('/sprintboardTable.html')
    except:
        return "problem when starting"

#added
@app.route("/end_sprint/<int:id>")
def end_sprint(id):
    sprint_to_end = Sprinttable.query.get_or_404(id)
    try:
        temp = time.gmtime()
        sprint_to_end.EndTime = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])+' '+str(temp[3])+':'+str(temp[4])+':'+str(temp[5])
        sprint_to_end.Sprintstatus = "Completed"
        dt1 = datetime.strptime(sprint_to_end.StartTime, "%Y/%m/%d %H:%M:%S")
        dt2 = datetime.strptime(sprint_to_end.EndTime, "%Y/%m/%d %H:%M:%S")
        delta = dt2 - dt1
        sprint_to_end.Timespent = f'Difference is {delta.days} days {delta.seconds} seconds'
        db.session.commit()
        return redirect('/sprintboardTable.html')
    except:
        return "problem when ending"
#added

######
@app.route('/by_ui_grid', methods=['GET', 'POST'])
def by_ui_grid(): 
    if request.method == 'POST': 
        db.session.query(Todo).filter(Todo.Tag=='UI')
    return render_template("gridview.html", tasks = db.session.query(Todo).filter(Todo.Tag == 'UI'))

@app.route('/by_core_grid', methods=['GET', 'POST'])
def by_core_grid(): 
    if request.method == 'POST': 
        db.session.query(Todo).filter(Todo.Tag=='Core')
    
    return render_template("gridview.html", tasks = db.session.query(Todo).filter(Todo.Tag == 'Core'))

@app.route('/by_testing_grid', methods=['GET', 'POST'])
def by_testing_grid(): 
    if request.method == 'POST': 
        db.session.query(Todo).filter(Todo.Tag=='Testing')
    
    return render_template("gridview.html", tasks = db.session.query(Todo).filter(Todo.Tag == 'Testing'))

@app.route('/by_all_grid', methods=['POST', 'GET'])
def show_all_grid(): 
    if request.method == 'POST': 
        db.session.query(Todo).all()
    return render_template("gridview.html", tasks=db.session.query(Todo).all())

#####


######

@app.route('/show_10only', methods=['GET', 'POST'])
def show_10only(): 
    if request.method == 'POST': 
        db.session.query(Todo).limit(10).all()
    
    return render_template("gridview.html", tasks = db.session.query(Todo).limit(10).all())

@app.route('/show_25only', methods=['GET', 'POST'])
def show_25only(): 
    if request.method == 'POST': 
        db.session.query(Todo).limit(25).all()
    
    return render_template("gridview.html", tasks = db.session.query(Todo).limit(25).all())

@app.route('/show_50only', methods=['GET', 'POST'])
def show_50only(): 
    if request.method == 'POST': 
        db.session.query(Todo).limit(50).all()
    
    return render_template("gridview.html", tasks = db.session.query(Todo).limit(50).all())

@app.route('/show_100only', methods=['GET', 'POST'])
def show_100only(): 
    if request.method == 'POST': 
        db.session.query(Todo).limit(100).all()
    
    return render_template("gridview.html", tasks = db.session.query(Todo).limit(100).all())

#######




@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('dashboard'))   #here
    except:
        return "problem when editing"

@app.route('/gridview', methods=['GET', 'POST'])
def showgrid():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('gridview.html', tasks=tasks)

#AddSprint function
@app.route("/addsprint", methods=['GET', 'POST'])
def to_addsprint():
    if request.method == 'POST': 
        #adding new sprint
        SprintNametoadd = request.form["nameofsprint"]
        Starttimetoadd = request.form["StartDate"]
        Endtimetoadd = request.form["EndDate"]
        Timespenttoadd = "-"
        Taskidtoadd = request.form["Taskid"]
        Taskdetailtoadd = request.form["Taskdetail"]
        Assigneetoadd = request.form["assignee"]
        Sprintstatustoadd = request.form["Status"]
        EstimatedTimetoadd = '-'

        new_sprint = Sprinttable(SprintName=SprintNametoadd, Taskid=Taskidtoadd, Taskdetail=Taskdetailtoadd, Assignee=Assigneetoadd, Sprintstatus=Sprintstatustoadd, EstimatedTime=EstimatedTimetoadd, StartTime=Starttimetoadd,EndTime=Endtimetoadd, Timespent=Timespenttoadd)

        try:
            db.session.add(new_sprint)
            db.session.commit()
            return redirect(url_for('to_sprintboard_table'))
        
        except:
            return 'issue adding to sprinboard'
    else:
        return render_template('addSprint.html')

########### Redirect to all members page ########### 
@app.route('/members', methods=['POST', 'GET'])
def members():
    memberstoload = membersinproject.query.order_by(membersinproject.date_created).all()
    return render_template("members.html", memberstoload=memberstoload)

####################################################

@app.route('/AddMembers', methods=['POST', 'GET'])
def to_addmembers(): 
    if request.method=='POST': 
        Nametoadd = request.form["name"]
        emailtoadd = request.form["email"]
        new_task = membersinproject(Name=Nametoadd, Email=emailtoadd)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('members'))  #here
        except:
            return "Error"  
    else:
        return render_template('addmembers.html')


# @app.route('/members_add', methods=['POST', 'GET'])
# def add_members():
#     if request.method == 'POST': 
#         Nametoadd = request.form["name"]
#         emailtoadd = request.form["email"]
#         new_task = membersinproject(Name=Nametoadd, Email=emailtoadd)
#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect(url_for('members'))  #here
#         except:
#             return "Error"    
#     else:
#         members = membersinproject.query.order_by(membersinproject.date_created).all()
#         return render_template("members.html", members=members)


@app.route("/delete_member/<int:id>")
def delete_member(id):
    members_to_delete = membersinproject.query.get_or_404(id)
    try:
        db.session.delete(members_to_delete)
        db.session.commit()
        return redirect(url_for('members'))   #here
    except:
        return "problem when editing"

@app.route("/burndown_for_member/<int:id>", methods=['GET', 'POST'])
def chartforindividual(id): 
    if request.method == 'POST': 
        return redirect(url_for('dashboard'))
    else:
        member_data = membersinproject.query.get_or_404(id)
        return render_template('graph.html', member_data=member_data)

#####
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.Name = request.form["name"]
        task.Type = request.form["type"]
        task.Tag = request.form["tag"]
        task.Story_Point = request.form["storypoint"]
        task.Priority = request.form["priority"]
        try:
            db.session.commit()
            return redirect(url_for('dashboard'))   #here 
        except:
            return "Error"
    else:
        return render_template("update.html", task=task)  

@app.route('/addtask/<int:id>', methods=['GET', 'POST'])
def addtask(id): 
    if request.method == 'POST': 
        #edit sprint here
    #     task_to_delete = Todo.query.get_or_404(id)
    # try:
    #     db.session.delete(task_to_delete)
    #     db.session.commit()
        #return request.form["taskid"] working

        # tasks = Todo.query.order_by(Todo.date_created).all()
        # sprintdetail = Sprinttable.query.get_or_404(id)
        # taskinsprint =  db.session.query(tasksinsprint).filter(tasksinsprint.sprint_id==id)
        task_tobe_add_into_sprint = request.form["taskid"]
        time_in_seconds = request.form["Storypointforthetask"]
        time_in_seconds = time_in_seconds
        task_transform = Todo.query.get_or_404(task_tobe_add_into_sprint)
        newtaskinsprint = tasksinsprint(Status = "To_Do" , Name = task_transform.Name, Type = task_transform.Type, Tag = task_transform.Tag , Story_Point = task_transform.Story_Point , Priority = task_transform.Priority, sprint_id=id, StartTime = '-', EndTime = '-' ,Timespent ="-", Storypointforthetask= time_in_seconds ) 
        db.session.add(newtaskinsprint)
        db.session.delete(task_transform)
        db.session.commit()
        return redirect(url_for('to_sprintboard', id=id))   
        #return render_template("sprintboard.html", tasks=tasks, taskinsprint=taskinsprint, sprintdetail=sprintdetail)
    else:
        sprintnumber = id 
        tasks = Todo.query.order_by(Todo.date_created).all()  
        return render_template('addtask.html', tasks=tasks, sprintnumber=sprintnumber)


##########BURNDOWN CHART#############################


@app.route("/burndown", methods=['GET', 'POST'])
def chart(): 
    if request.method == 'POST': 
        return redirect(url_for('dashboard'))
    else:
        return render_template('graph.html')

@app.route('/data')
def data(): 
    #query the database for estimated time spent 
    #query the database for actual time spent 
    return jsonify({"actualtime" : [1797, 1456, 1908, 896, 1300, 755], 
                    "estimatedtime" : [1400, 1600, 2700, 400, 1200, 500]})

@app.route('/member_chart', methods=['GET', 'POST'])
def chart_indi(): 
    if request.method == 'POST': 
        time = db.session.query(membersinproject.Email)
    
    return jsonify({"contribution" : [db.session.query(membersinproject.Email)]})


@app.route("/membersChart", methods=['GET', 'POST'])
def to_member_chart(): 
    if request.method == 'POST': 
        return redirect(url_for('dashboard'))
    else:
        return render_template('contributionChart.html')

if __name__ == "__main__":
    app.run(debug=True)