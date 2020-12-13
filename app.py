from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwert@localhost/simplebankingsystem'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ptyrktzegcnkku:e2aa7f41be85c8d1d9248f5e3e33f37033b40254e5bfc35a0b9f6830ffb8e857@ec2-54-157-66-140.compute-1.amazonaws.com:5432/dcc2ophr2g6god'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Customers(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    balance = db.Column(db.Integer)

    def __init__(self, customer, email, balance):
        self.customer = customer
        self.email = email
        self.balance = balance
        

class Transfers(db.Model):
    __tablename__ = 'Transfers'
    id = db.Column(db.Integer, primary_key=True)
    customerfrom = db.Column(db.String(200), unique=False)
    customerto = db.Column(db.String(200))
    amount = db.Column(db.Integer)

    def __init__(self, customerfrom, customerto, amount):
        self.customerfrom = customerfrom
        self.customerto = customerto
        self.amount = amount
        


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers')
def cust():
    if db.session.query(Customers).count() == 0:
        #print("lol")
        cus=["customer1","customer2","customer3","customer4","customer5","customer6","customer7","customer8","customer9","customer10"]
        em=['c1@email.com','c2@email.com','c3@email.com','c4@email.com','c5@email.com','c6@email.com','c7@email.com','c8@email.com','c9@email.com','c10@email.com']
        bal=[3836,7347,9090,7654,9090,122,3245,4322,4567,8766]
        for i in range(10):
            customer=cus[i]
            email=em[i]
            balance=bal[i]
            data = Customers(customer,email,balance)
            db.session.add(data)
            db.session.commit()
    users = db.session.query(Customers).all()   
    return render_template('customers.html',users=users)

@app.route('/transfers')
def transfer():
    tfs = db.session.query(Transfers).all()
    return render_template('transfers.html',tfs=tfs)

@app.route('/customers/<customer_name>')
def profile(customer_name):

    return render_template('customer_name.html',c_name=customer_name)


@app.route('/customers/<customer_name>/submit', methods=['POST'])
def submit(customer_name):
    if request.method == 'POST':
        customerfrom = customer_name
        customerto = request.form['customerto']
        balance = int(request.form['balance'])
        
        # print(customer, dealer, rating, comments)
        if customerfrom == '' or customerto == '':
            return render_template('index.html', message='Please enter required fields')
        user1 = db.session.query(Customers).filter_by(customer = customerfrom).first()
        #print(user1.balance)
        user2 = db.session.query(Customers).filter_by(customer = customerto).first()
        if user1.balance >= balance:
            
            user1.balance = user1.balance - balance
            db.session.commit()
            user2.balance = user2.balance + balance
            db.session.commit()
            #print("done")
            #session.commit()
            #session.commit()
            #user2.balance = user2.balance + balance
            #session.user1.commit()
            
            data = Transfers(customerfrom, customerto, balance)
            db.session.add(data)
            db.session.commit()
            return render_template('index.html', message='funds transferred succesfully')
        else:
            return render_template('index.html', message='Insuffiecient funds')

       # if db.session.query().filter(Feedback.customer == customer).count() == 0:
        #    data = Feedback(customer, dealer, rating, comments)
         #   db.session.add(data)
          #  db.session.commit()
           # send_mail(customer, dealer, rating, comments)
            #return render_template('success.html')
       # return render_template('index.html', message='You have already submitted feedback') ***/


if __name__ == '__main__':
    app.run()
