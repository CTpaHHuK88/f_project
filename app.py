from flask import Flask
from flask import render_template, session, request
import logging
from models import UserBase
from sqlalchemy.orm import Session
from session import engine

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
        if request.method == 'POST':
            login = request.form.get('login')
            password = request.form.get('password')
            return f"{login} \n {password}"
        return render_template('login.html')
        

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
  
except NameError as err:
    logging.error(err,exc_info=True)
finally:
    #if __name__ == 'main':
    app.run(debug=True)

