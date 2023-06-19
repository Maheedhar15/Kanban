from email.policy import default
from flask import Flask,jsonify, render_template,session,request,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
import numpy as np
from flask import render_template,jsonify,send_file
import redis
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager,get_jwt
import pandas as pd
from celery import Celery
from celery.schedules import crontab
from os.path import basename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from jinja2 import Environment, PackageLoader

ACCESS_EXPIRES = timedelta(hours=2)


application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)


CORS(application, origins='*')

application.config["JWT_SECRET_KEY"] = "secret"  
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(application)

application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'

celery = Celery(application.name , broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

def deadline_checker(date):
                    CurrDate = str(datetime.now())[:10]


                    if CurrDate > date:
                        return True
                    else:
                        return False

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

class client(db.Model):
    __name__ = "client"
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False)
    uname = db.Column(db.String(80),nullable=False)
    mail = db.Column(db.String(80),nullable=False)
    password = db.Column(db.String(80),nullable=False)
    date_created = db.Column(db.DateTime,nullable=False, default = datetime.utcnow())

class list(db.Model):
    __name__ = "list"
    u_id = db.Column(db.Integer,db.ForeignKey('client.uid'), nullable=False )
    l_id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    l_name = db.Column(db.String(80),nullable=False)
    no_of_tasks = db.Column(db.Integer,default=0)
    no_completed = db.Column(db.Integer,default=0)
    no_crossed_deadline = db.Column(db.Integer,default=0)

class task(db.Model):
    l_id = db.Column(db.Integer, db.ForeignKey('list.l_id'), nullable=False)
    t_id = db.Column(db.Integer, primary_key=True,nullable=False)
    title = db.Column(db.String(80),nullable=False)
    description = db.Column(db.String(80))
    deadline = db.Column(db.String,nullable=False)
    status = db.Column(db.String(80))

@application.route("/login",methods=['GET','POST'])
def login():    
  data = request.json
  print(data['mail'],data['password'])
  encoded_pass = data['password'].encode('utf-8')
  dbdata = client.query.filter_by(mail=data['mail']).first()
  print(dbdata.password)
  print(encoded_pass)
  token = create_access_token(identity={"mail":dbdata.mail})
  if(bcrypt.checkpw(encoded_pass,dbdata.password)):
    return jsonify({'access_token': token, 'name':dbdata.uname,'id':dbdata.uid})

@application.route('/forgotpassword', methods=['GET', 'POST'])
def forgot__password():
    if request.method == 'POST':
        data = request.json
        user_data = client.query.filter_by(mail = data['mail']).first()
        if(user_data):
            pw_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user_data.password = pw_hash
            print(data['password'], pw_hash)
            db.session.add(user_data)
            db.session.commit()
            return jsonify({'message':'password successfully changed'})
        else:
            return jsonify({'message':'email not found',}),404




@application.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        data = request.json
        name = data['name'] 
        mail = data['mail']
        password = data['password']
        pw_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cell = client(uname=name,mail=mail,password=pw_hash)
        db.session.add(cell)
        db.session.commit()
        token = create_access_token(identity={"mail":mail})
        ddata = client.query.filter_by(mail=mail).first()
        return jsonify({'access_token': token, 'name':name,'id':ddata.uid})

@application.route('/dashboard/<int:uid>')
@jwt_required()
def dashboard(uid):
    if(len(list.query.filter_by(u_id=uid).all())==0):
        return jsonify({
            'list': [{'len_list':0}],
            'message': 'no lists'
        }
        )
    else:
        data = list.query.filter_by(u_id=uid).all()
        availableLists = []
        for i in data:
            d = {
                'list_name': i.l_name,
                'list_id' : i.l_id
            }
            availableLists.append(d)
        len_list = len(data)
        l=[]
        for i in data:
            data2 = task.query.filter_by(l_id=i.l_id).all()
            l2 = []
            for j in data2:
                d2 = {
                    'task_id' : j.t_id,
                    'title' : j.title,
                    'desc' : j.description,
                    'deadline': j.deadline,
                    'status' : j.status,
                    'list_id': j.l_id
                }
                l2.append(d2)
            d = {
                'list_id' : i.l_id,
                'len_list' : len_list,
                'list_name': i.l_name,
                'no_of_tasks':i.no_of_tasks,
                'no_completed':i.no_completed,
                'crossed_deadline': i.no_crossed_deadline
            }
            l.append((d,l2))
    return jsonify(
        {
            'list' : l,
            'availableLists': availableLists,
            'message' : 'Success'
        }
    )

@application.route('/createList/<id>', methods=['GET', 'POST'])

def createList(id):
    data = request.json
    l_name = data['l_name']
    present_data = list.query.filter_by(u_id=id).all()
    if(len(present_data)>=5):
        return jsonify({'al': "Maximum Number of Lists Reached","status" : "707"})
    else:
        additive = list(u_id=id,l_name=l_name)
        db.session.add(additive)
        db.session.commit()
        return jsonify({'message':'success','status':'200'})

@application.route('/createTask/<uid>', methods=['GET', 'POST'])

def createTask(uid):
    if request.method == 'GET':
        data = list.query.filter_by(u_id=uid).all()
        l = []
        for i in data:
            d = {
                'list_name': i.l_name,
                'list_id' : i.l_id
            }
            l.append(d)
        return jsonify({
            'availableLists': l,
            'message': 'success'
        })
    else:
        data = request.json
        lname = data['list_name']
        title = data['task_title']
        desc = data['task_desc']

        deadline = data['deadline'][:10]
        status = data['status']
        
        activeListID = list.query.filter_by(l_name = lname).first().l_id
        ldata = list.query.filter_by(l_name = lname).first()
        if(status==1):
            ldata.no_completed+=1
        ldata.no_of_tasks+=1
        additive = task(l_id=activeListID, title=title,description=desc,deadline=deadline,status=status)
        db.session.add(additive)
        db.session.commit()

        return jsonify({'message' : 'success'})

@application.route('/updateList/<int:lid>', methods = ['GET','PUT'])

def updateList(lid):
    data = list.query.filter_by(l_id = lid).first()
    if request.method == 'GET':
        d = { 'list_id': lid, 'list_name' : data.l_name }
        return jsonify({'list':d})
    if request.method == 'PUT':
        change = request.json
        ak = change['l_name']
        data.l_name = ak
        db.session.add(data)
        db.session.commit()
        return jsonify({'message':'Success'})

@application.route('/deleteList/<lid>',methods = ['DELETE'])

def deleteList(lid):
    if request.method == 'DELETE':
        data = list.query.filter_by(l_id=lid).first()
        tasks = task.query.filter_by(l_id=lid).all()
        for i in tasks:
            db.session.delete(i)
        db.session.delete(data)
        db.session.commit()
        return jsonify({'message':'success'})

@application.route('/updateTask/<tid>/<uid>', methods=['GET','PUT'])

def updateTask(tid,uid):
    taskdata = task.query.filter_by(t_id=tid).first()
    if request.method == 'GET':
        list_name = ''
        data = list.query.filter_by(u_id=uid).all()
        l = []
        for i in data:
            if i.l_id == taskdata.l_id:
                list_name = i.l_name
            d1 = {
                'list_name': i.l_name,
                'list_id' : i.l_id
            }
            l.append(d1)
        d = {
            'task_id':taskdata.t_id,
            'task_name': taskdata.title,
            'task_desc': taskdata.description,
            'task_deadline': taskdata.deadline,
            'task_status': taskdata.status,
            'list_name' : list_name
        }
        return jsonify({'list': d, 'availableLists': l })
    if request.method== 'PUT':
        data = request.json
        ldata = list.query.filter_by(l_name=data['list_name']).first()
        l1data = list.query.filter_by(l_id=taskdata.l_id).first()
        if(taskdata.l_id != ldata.l_id):
            l1data.no_of_tasks-=1
            ldata.no_of_tasks+=1 
        taskdata.l_id = ldata.l_id
        taskdata.title = data['task_title']
        taskdata.description = data['task_desc']
        taskdata.deadline = data['deadline']
        taskdata.status = data['status']

        if(data['status']==1):
            ldata.no_completed+=1
        

        db.session.add(taskdata)
        db.session.commit()

        return jsonify({'message':'success'})

@application.route('/deleteTask/<id>', methods=['DELETE'])

def deleteTask(id):
    removable = task.query.filter_by(t_id=id).first()
    ldata= list.query.filter_by(l_id=removable.l_id).first()
    ldata.no_of_tasks-=1
    if(removable.status=='1'):
        print(ldata.no_completed)
        ldata.no_completed-=1
        print(ldata.no_completed)

    db.session.delete(removable)
    db.session.commit()
    return jsonify({'message':'success'})

@application.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")

@application.route('/summary/<int:uid>')
@jwt_required()
def summary(uid):
    if(len(list.query.filter_by(u_id=uid).all())==0):
        return jsonify({
            'list': [{'len_list':0}],
            'message': 'no lists'
        }
        )
    else:
        data = list.query.filter_by(u_id=uid).all()
        availableLists = []
        for i in data:
            
            d = {
                'list_name': i.l_name,
                'list_id' : i.l_id
            }
            availableLists.append(d)
        len_list = len(data)
        l=[]
        
        for i in data:
            i.no_crossed_deadline = 0
            data2 = task.query.filter_by(l_id=i.l_id).all()
            l2 = []
            visited = []
            no_of_tasks_in_month = {}
            no_of_completed_tasks_in_month = {}
            no_of_deadline_crossed_tasks = {}
            for j in data2:
                
                CurrentDate = str(datetime.now())[:10]

                ExpectedDate = j.deadline

                if CurrentDate > ExpectedDate:
                    if(int(j.status)==0):
                        i.no_crossed_deadline+=1
                test_date = datetime(int(j.deadline[:4]),int(j.deadline[5:7]),int(j.deadline[9:11]))

                label = test_date.strftime("%B") +" " + j.deadline[:4]

                if label not in visited:
                    visited.append(label)
                    no_of_tasks_in_month[label] = 1
                    if(j.status=='1'):
                        no_of_completed_tasks_in_month[label] = 1
                    else:
                        no_of_completed_tasks_in_month[label] = 0
                    
                    if(deadline_checker(j.deadline)):
                        if(j.status=='0'):
                            no_of_deadline_crossed_tasks[label] = 1
                    else:
                        no_of_deadline_crossed_tasks[label] = 0
                else:
                    no_of_tasks_in_month[label]+=1
                    if(j.status=='1'):
                        no_of_completed_tasks_in_month[label]+= 1
                    if(deadline_checker(j.deadline)):
                        if j.status == '0':
                            no_of_deadline_crossed_tasks[label]+=1
                    
                        
            no_of_tasks_list,no_completed_tasks_list,no_of_deadline_crossed_tasks_list = [],[],[]
            keys_arr = (no_of_tasks_in_month.keys())
            labels = []
            for m in keys_arr:
                no_of_tasks_list.append(no_of_tasks_in_month[m])
                no_completed_tasks_list.append(no_of_completed_tasks_in_month[m])
                no_of_deadline_crossed_tasks_list.append(no_of_deadline_crossed_tasks[m])
                labels.append(str(m))

            

            d = {
                'list_id' : i.l_id,
                'len_list' : len_list,
                'list_name': i.l_name,
                'no_of_tasks':i.no_of_tasks,
                'no_completed':i.no_completed,
                'no_crossed_deadline': i.no_crossed_deadline,
                'labels' : labels,
                'no_of_tasks_list' : no_of_tasks_list,
                'no_completed_tasks_list': no_completed_tasks_list,
                'no_of_deadline_crossed_tasks_list': no_of_deadline_crossed_tasks_list
            }
            l.append(d)
    return jsonify(
        {
            'list' : l,
            'availableLists': availableLists,
            'message' : 'Success'
        }
    )
@application.route('/export/<int:id>',methods=['GET'])

def export_tracker(id):
    lists = list.query.filter_by(u_id=id).all()
    exportable = []
    for i in lists:
        l=[]
        l.append(i.l_name)
        l.append(i.no_of_tasks)
        l.append(i.no_completed)
        print(i.no_crossed_deadline)


        exportable.append(l)
    
    listed = pd.DataFrame(exportable, columns=['List Name','Number of Tasks','Number of Completed tasks'])
    listed.to_csv('./csv_files/your_lists.csv',index=False)
    return send_file('./csv_files/your_lists.csv')

@application.route('/export_list/<lid>', methods=['GET'])

def export_list(lid):
    tasks = task.query.filter_by(l_id=lid).all()
    exportable = []
    for i in tasks:
        l = []
        l.append(i.title)
        l.append(i.description)
        l.append(i.deadline)
        if(i.status=='1'):
            l.append("Completed")
        else:
            l.append("Not Completed")
        exportable.append(l)
    
    tasks_for_list = pd.DataFrame(exportable, columns=['Task Name','Task Description','Task Deadline','Status of Task'])
    tasks_for_list.to_csv('./csv_files/your_tasks.csv',index=False)
    return send_file('./csv_files/your_tasks.csv')



@celery.task()
def monthly_report():
    with application.app_context():
        file_loader = PackageLoader("application", "templates")
        env = Environment(loader=file_loader)
        # Extracting user
        users = client.query.all()



        for ak in users:
            uid = ak.uid
            udata = ak.query.filter_by(uid=uid).first()
            lists = list.query.filter_by(u_id=uid).all()
            l=[]
            for i in lists:
                tasks = task.query.filter_by(l_id=i.l_id).all()
                for j in tasks:
                    data={}
                    data['task_name'] = j.title
                    data['deadline'] = j.deadline
                    data['list_name'] = i.l_name
                    if(j.status == '1'):
                        data['status'] = 'Completed'
                    else:
                        data['status'] = 'Not Completed'

                    l.append(data)
                
            print(l)
            
            # Creating Monthly Report in Html
            rendered = env.get_template("report.html").render(udata=udata,data=l)
            filename = "report.html"
            with open(f"{filename}", "w") as f:
                    f.write(rendered)

            msg = MIMEMultipart()
            msg["From"] = 'kanbanteam15@gmail.com'
            msg["To"] = ak.mail
            msg["Subject"] = "Monthly Report"
            body = MIMEText("Here is your Monthly Report", "plain")
            msg.attach(body)
            with open(f"{filename}", "r") as f:
                    attachment = MIMEApplication(f.read(), Name=basename(filename))
                    attachment["Content-Disposition"] = 'attachment; filename="{}"'.format(basename(filename))

            msg.attach(attachment)

            with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user='kanbanteam15@gmail.com', password='hxvzsxwdzypbilfm')
                    connection.send_message(
                        msg=msg,
                        from_addr='kanbanteam15@gmail.com',
                        to_addrs=[ak.mail],
                    ) 

        return "Monthly Report Sent"

@celery.task()
def daily_reminder():
    with application.app_context():
        # Extracting user
        users = client.query.all()
        tasks_crossed = []
        for ak in users:
            uid = ak.uid
            udata = ak.query.filter_by(uid=uid).first()
            lists = list.query.filter_by(u_id=uid).all()
            for i in lists:
                tasks = task.query.filter_by(l_id=i.l_id).all()
                for j in tasks:
                    if deadline_checker(j.deadline):
                        if(j.status=='0'):
                            tasks_crossed.append(j.title)

                
                
            
            tc =  str(tasks_crossed)[1:-1].replace("'","")

            msg = MIMEMultipart()
            msg["From"] = 'kanbanteam15@gmail.com'
            msg["To"] = ak.mail
        
            msg["Subject"] = "Daily Reminder"
            if(len(tasks_crossed)==0):
                body = MIMEText(f"There are no tasks that has crossed the deadline!, ", "plain")
            else:
                body = MIMEText(f"These are the tasks that have crossed the deadline: {tc}")
            msg.attach(body)

            with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user='kanbanteam15@gmail.com', password='hxvzsxwdzypbilfm')
                    connection.send_message(
                        msg=msg,
                        from_addr='kanbanteam15@gmail.com',
                        to_addrs=[ak.mail],
                    ) 

        return "Daily Reminder Sent"

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=15),daily_reminder.s(), name = "Daily Reminder")
    sender.add_periodic_task(crontab(hour=11, minute=0, day_of_month=1), monthly_report.s(), name="Monthly Reports")

@application.route('/report')
def daily():
    monthly_report.delay()
    daily_reminder.delay()
    return jsonify({'status':'ok'})

@application.route('/moveTask/<tid>/<lid>', methods=['GET', 'POST'])
def moveTask(tid,lid):
    if request.method == 'POST':
        task_at_hand = task.query.filter_by(t_id=tid).first()
        if(str(lid)== str(task_at_hand.l_id)):
            return jsonify({'message': 'same list'})
        else:
            list1_data = list.query.filter_by(l_id=task_at_hand.l_id).first()
            list1_data.no_of_tasks-=1
            if(task_at_hand.status=='1'):
                list1_data.no_completed-=1
            list2_data = list.query.filter_by(l_id=lid).first()
            list2_data.no_of_tasks+=1
            if(task_at_hand.status=='1'):
                list2_data.no_completed+=1
            task_at_hand.l_id = int(lid)

            db.session.add(task_at_hand)
            db.session.add(list1_data)
            db.session.add(list2_data)
            db.session.commit()

            return jsonify({'message':'success'})

        

if __name__ == "__main__":
    

    application.run(debug=True)