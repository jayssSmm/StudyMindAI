from flask import Blueprint,request,render_template,jsonify,make_response,redirect
from app.extensions import db
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User

bp=Blueprint("auth",__name__)

@bp.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = db.session.execute(
        db.select(user).filter_by(email=email)
    ).scalar_one_or_none()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))

    response=make_response(redirect('/'),200)
    response.set_cookie('access_token_cookie',access_token,httponly=True)

    return response

@bp.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')
    
    new_user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))

    response=make_response(redirect('/'),200)
    response.set_cookie('access_token_cookie',access_token,httponly=True)

    return response