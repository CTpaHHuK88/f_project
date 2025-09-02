from flask import Flask
from flask import render_template, session, request, redirect, url_for
import logging
from models import UserBase, AuthBase
from sqlalchemy.orm import Session
from session import engine
from utils import hash_password
from uuid import uuid4

logging.basicConfig(
    level=logging.INFO, 
    filename="py_log.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s")
logging.info("Запуск программы")

try:
    app = Flask(__name__)

    @app.route('/')
    def index_pa():
        return 'Index page'

    @app.route('/login', methods=['GET', 'POST'])
    def signin():
        if session:
            return redirect('/panel')
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            h_pasword = hash_password(password)
            with Session(autoflush=False, bind=engine) as db:
                query_login = db.query(AuthBase).filter(AuthBase.login==login).first()
            if query_login and h_pasword == query_login.password:
                session['access'] = 1
                session['username'] = login
                logging.info(f"Удачная попытка входа {login}")
                return redirect('/panel')
            else: 
                logging.warning(f"Неудачная попытка входа {login}")
                return 'Логин или пароль введён неправильно!!!'
        return render_template('login.html')
    
    @app.route('/logout')
    def logout_panel():
        logging.info(f"Пользователь {session['username']} вышел из системы.")
        session.pop('access', None)
        session.pop('username', None)        
        return redirect(('/login'))
    
    @app.route('/panel')
    def panel_admin():
        data = {'title': 'Панель администратора',
                'username':session['username']
                }
        if 'access' in session and session['access']==1:            
            return render_template('panel.html',data=data)
        else: return redirect('/login')
        
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            email = request.form.get('email')

            with Session(autoflush=False, bind=engine) as db:
                values = AuthBase(
                    login=login,
                    password=hash_password(password),
                    mail=email,
                    status=1
                    )
                db.add(values)     # добавляем в бд
                db.commit()     # сохраняем изменения
                return redirect('/login')
        return render_template('signup.html')

    @app.route('/about/<name>')
    def about(name):
        if isinstance(name, str):
            with Session(autoflush=False, bind=engine) as db:
                ss = db.query(UserBase).filter(UserBase.name==name).first()
            data = {
                'username': ss,
                'title': 'Home page',
                'text': 'This is Flask app!!!',
                'age': name
                }
        return render_template('index.html', data=data)
  
    @app.route('/settings')
    def settings():
        data = {'title': 'Настройки',
        'username':session['username']
        }
        if 'access' in session and session['access']==1:    
            return render_template('/settings/set.html', data=data)
        
        if request.method == 'POST':
            return 
    
    
    @app.route('/users')
    def users():
        with Session(autoflush=False, bind=engine) as db:
            query_login = db.query(AuthBase).all()
        data = {'title': 'Управление пользователями',
        'username':session['username'],
        'list':query_login
        }
        if 'access' in session and session['access']==1:    
            return render_template('/users/users.html', data=data)
        
        if request.method == 'POST':
            return 

except NameError as err:
    logging.error(err,exc_info=True)
finally:
    app.secret_key = b"\xb0f\xe4+z,\xbd'\xd0\x89i\x92\xffF\xb9\x9d]\x1eP\x10\x986#\xfe"
    app.run(debug=True)


