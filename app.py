from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "1234"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100))
    email = db.Column(db.String(60))
    telefone = db.Column(db.String(30))
    cargo = db.Column(db.String(20))


    def __init__(self, nome, email, telefone, cargo):

        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.cargo = cargo





#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", funcionarios = all_data)



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cargo = request.form['cargo']


        my_data = Data(nome, email, telefone, cargo)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))

        my_data.nome = request.form['nome']
        my_data.email = request.form['email']
        my_data.telefone = request.form['telefone']
        my_data.cargo = request.form['cargo']


        db.session.commit()
        flash("Funcionário editado com sucesso!")

        return redirect(url_for('Index'))




#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Funcionário deletado com sucesso!")

    return redirect(url_for('Index'))






if __name__ == "__main__":
    app.run(debug=True)