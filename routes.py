import os
import uuid
from datetime import datetime
from sqlite3 import IntegrityError
from flask import (
    current_app,
    jsonify,
    request,
    send_from_directory,
    Blueprint,
    send_file,
    render_template,
    redirect
)
from extensions import bcrypt


from model import Users, Request
from flask_login import login_user, logout_user, current_user

routes_bp = Blueprint("routes", __name__)


reciprocal=0

@routes_bp.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect("/login")
    

    return render_template("index.html", current_user=current_user,reciprocal=reciprocal)

@routes_bp.route('/profile')
def profile():
    from app import db
    from model import Users,Request
    if not current_user.is_authenticated:
        return redirect("/login")
    

    matchlist = []

    user_queries = Request.query.filter_by(Created_by=current_user.User_ID).all()

    for i in user_queries:
        requested_user = Users.query.filter_by(Phone=i.Phone).first()
        if requested_user:
            if Request.query.filter_by(Phone=current_user.Phone, Created_by=requested_user.User_ID):
                matchlist.append(i)

    for i in matchlist:
        print(Users.query.filter_by(Phone=i.Phone).first().Name)


    return render_template("profile.html", current_user=current_user, matchlist=matchlist, Users=Users)

@routes_bp.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    user = Users.query.filter_by(Phone=request.form['username']).first()
    if user and bcrypt.check_password_hash(user.Password, request.form['password']):
        login_user(user)
        return redirect('/')
    return
    


@routes_bp.route('/register', methods=['GET','POST'])
def signup():

    if request.method == "GET":
        return render_template("register.html")

    from app import db, bcrypt
    
    name = request.form['name']
    mobile = request.form['username']
    password = request.form['password']


    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    if name and mobile and password:
        

        new_user = Users(
        Name=name,
        Phone=mobile,
        Password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except IntegrityError:
            db.session.rollback()
            return

    else:
        return

@routes_bp.route('/logout' )
def logout():
    if not current_user.is_authenticated:
        return redirect('/login')
    logout_user()
    return redirect('/login')



@routes_bp.route('/request', methods=['POST'])
def create_request():
    from app import db, bcrypt
    global reciprocal
    
    mobile = request.form['username']

    if mobile:
        

        new_request = Request(
        Phone=mobile,
        Created_by=current_user.User_ID)

        try:
            db.session.add(new_request)
            db.session.commit()

            check = Users.query.filter_by(Phone=mobile).first()
            if check:
                reciprocal_match = Request.query.filter_by(Phone=current_user.Phone, Created_by=check.User_ID).first()
                if reciprocal_match:
                    reciprocal=1
                else:
                    reciprocal=0
            else:
                reciprocal=0

            return redirect('/')
        except IntegrityError:
            db.session.rollback()
            return

    else:
        return
