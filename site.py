import os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import db

# DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = os.environ.get('secret_key')

app = Flask(__name__)
app.config.from_object(__name__)
#app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))

login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
# login_manager.login_message_category = "success"


# @login_manager.user_loader
# def load_user(user_id):
#     print("load_user")
#     return UserLogin().fromDB(user_id)





@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')



@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['email']) > 0 and len(request.form['psw']) > 0 \
            and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            db.addUser(request.form['name'], request.form['email'], hash, 21)
            flash("Зарегался, родной", 'success')
            return redirect(url_for('login'))
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html", title="Регистрация")




if __name__ == "__main__":
    app.run(debug=True)
