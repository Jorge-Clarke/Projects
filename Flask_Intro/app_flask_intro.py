from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)   # This is for referencing this file (Auto referencing ?)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    # In the previous line: '///' is for relative paths. '////' is for absolute paths. We use 3/ here because we don't want to 
    # specify an exact location.
    # test.db is the database where we are going to store sverything.
db = SQLAlchemy(app)    # Initialising the data base

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) # 'nullable = False' because we don't want this to be left blank 
 #   completed = db.Column(db.Integer, default = 0)  # Ignore this line, the completed column is never used (???)
    date_created = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):     # a function to return a string everytime we create a new element
        return '<Task %r>' % self.id


@app.route('/', methods=['POST' , 'GET'])   # index route, so when we browse to the URL we don't immediatelly just 404.
                    # Flask set-up routes with app route decorator. We are going to pass the URL string of our route
def index():        # Define the function for the previous route
    if request.method == 'POST':
        task_content = request.form['content']  # Try with: return 'hello' 
        new_task = Todo(content = task_content) #

        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding your task'    

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html' , tasks=tasks)


@app.route('/delete/<int:id>')  # This is the "delete" part of the app 
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')   # This send us back to our homepage
    except:
        return 'There was a problem with the task'
    

@app.route('/update/<int:id>' , methods = ['GET' , 'POST'] )  # This is the "delete" page of the app 
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating the task'    
    else:
        return render_template('update.html' , task = task)



if __name__ == '__main__':
    app.run(host = 'localhost', port = 5001, debug=True)     # '= True', so if we have any errors they will pop-up and we can see

