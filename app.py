from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy  import SQLAlchemy
from datetime import datetime

app = Flask(__name__)                                            #reference file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'      #set connection to database
db = SQLAlchemy(app)                                             #This creates the SQLAlchemy object that connects Flask ↔ your database

class ToDo(db.Model):                                           
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):                                          #representation
        return '<Task %r>' % self.id                             #return string when we add a new task, Show the task object as <Task id> instead of a raw memory address.   

# with app.app_context():                                          #create the database
#     db.create_all()
    
@app.route('/', methods=['POST', 'GET'])                                                  # routes points to endpoint/url
def index():  
    if request.method == 'POST':                              
        task_content = request.form['content']                  # unod ka form, name=content
        new_task = ToDo(content=task_content)                   # create a new task object
        
        try:
            db.session.add(new_task)                            # add the new task to the database session
            db.session.commit()                                 # commit the changes to the database
            return redirect('/')                                # redirect to the home page
        except:
            return 'There was an issue adding your task'        # error handling
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()        # retrieve all tasks from the database, ordered by date created
        return render_template('index.html', tasks=tasks)                         # render_template to render html file, no need to specify templates folder
    
    
@app.route('/delete/<int:id>')                                #accept an int na parang parameter para ma delete ang amo to nga id
def delete(id):
        task_to_delete = ToDo.query.get_or_404(id)            # get the task by id or return 404 if not found
        
        try:
            db.session.delete(task_to_delete)                 
            db.session.commit()                                
            return redirect('/')                              
        except:
            return 'There was a problem deleting that task'    
        
        
@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
                            
if __name__ == "__main__":
    app.run(debug=True)