import os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import db
from user import User

#app config
DEBUG = True
SECRET_KEY = os.environ.get('secret_key')
app = Flask(__name__)
app.config.from_object(__name__)
login_manager = LoginManager(app)

# what to say and to where redirect when unauth person trying to visit somethig special
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(email):
    return User().init_by_email(email)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template('welcome.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
            
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        user_dict = db.get_user_by_email(request.form['email'])
        remember = True if request.form.get('remainme') else False
        print(remember)
        if user_dict and check_password_hash(user_dict['password'], request.form['password']):
            login_user(User().init_by_dict(user_dict), remember=remember)
            return redirect(request.args.get('next') or url_for('profile'))
        else:
            flash('Неверный логин, пароль', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Ты вышел, бра", 'success')
    return redirect(url_for('login'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['email']) > 0 and len(request.form['psw']) > 0 \
            and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            db.add_user(request.form['name'], request.form['email'], hash, 21)
            flash("Зарегался, родной", 'success')
            return redirect(url_for('login'))
        else:
            flash("Неверно заполнены поля", "error")
    return render_template("register.html", title="Регистрация")


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", info=str(current_user.get_name()))


if __name__ == "__main__":
    app.run(debug=True)