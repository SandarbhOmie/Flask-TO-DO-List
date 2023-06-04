from flask import Flask,render_template, request, redirect 

# render_template help us to seperate information of presentation (like html codes) from application logic ( like python app code of flask)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# initializing the aplication name as 'app'
app = Flask(__name__)

# "SQLALCHEMY" is used to create database in Flask
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
db = SQLAlchemy(app)

# creating Database class to Specify layout of database and creating table to save the entries.
class Todo(db.Model):

    # serial No is our primary key which will help us to diffrentiate the entries in ToDo list
    sno = db.Column(db.Integer,primary_key =True )

    # title of the task 
    title = db.Column(db.String(100),nullable = False )

    # description of the task
    desc = db.Column(db.String(300),nullable = False )

    # Creating a Time column to show the time when the task was added tot he list
    date_created = db.Column(db.DateTime , default = datetime.utcnow )
    
    # Providind concise representation of object's attribute by returning string object.
    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"




@app.route('/',methods=['GET','POST']) 


def home_page():                # creating basic entry in the application : this will hel us to show the first page when we enter the website.
    
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()   # used to execute

    allTodo = Todo.query.all()

    return render_template('index.html',allTodo=allTodo)


# Update method : to update the entries in the list.
@app.route('/update/<int:sno>',methods=['GET','POST'])  # uisng this we can create multiple viewpoints
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc= request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()   # used to execute
        return redirect("/")


    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

    
   

# Deletion method : to delete the entries
@app.route('/delete/<int:sno>')  # uisng this we can create multiple viewpoint
def delete(sno):

    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect("/")




# Calling the app to run
if __name__ =="__main__":
    
    app.run(debug=True,port = 8000)  