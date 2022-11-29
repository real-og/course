import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import db
from user import User
import logic
import json


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
        email = request.form['email']
        user_dict = db.get_user_by_email(email)
        remember = True if request.form.get('remainme') else False
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
    return redirect(url_for('index'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['email']) > 0 and len(request.form['psw']) > 0 \
            and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            db.add_user(request.form['name'], request.form['email'], hash, int(request.form['age']))
            return redirect(url_for('login'))
        else:
            flash("Неверно заполнены поля", "error")
    return render_template("register.html")


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", info=current_user.get_user(), word_count=db.get_word_count_by_user(current_user.get_id()), song_count=db.get_song_count_by_user(current_user.get_id()))

@app.route('/dictionary')
@login_required
def dictionary():
    words = db.get_words_by_user(current_user.get_id())
    return render_template("dictionary.html", words=words, tracks=['Maru Nara twox'])

@app.route('/study', methods=["POST", "GET"])
@login_required
def study():
    if request.method == "POST":
        uuid = logic.create_url(request.form['author'] + ' ' + request.form['track_name'], start='')
        return redirect(url_for('study_track',  track_uuid=uuid, name=request.form['track_name'], author=request.form['author']))
    return render_template("study.html")

@app.route('/study/<track_uuid>', methods=['GET', 'POST'])
@login_required
def study_track(track_uuid):
    if request.method == "POST":
        flash('Добавлено', 'success')
        db.add_song_to_user(current_user.get_id(), request.form['track_name'], request.form['author'])
        return redirect(url_for('study_track',  track_uuid=track_uuid, name=request.form['track_name'], author=request.form['author']))
    lyrics = logic.LyricsParser('https://genius.com/' + track_uuid).get_lyrics()
    if not len(lyrics):
        lyrics = 'Упс, не смог найти...'
    return render_template("study_track.html",
                            lyrics=lyrics.replace('\n', ' <br> ').split(' '),
                            name=track_uuid[:-7],
                            count=len(logic.get_unknown_by_user(current_user.get_id(), lyrics.split())),
                            track_name=request.args.get('name'),
                            author=request.args.get('author'))

@app.route('/show-unknown/<track_uuid>')
@login_required
def show_new(track_uuid):
    lyrics = logic.LyricsParser('https://genius.com/' + track_uuid).get_lyrics()
    unknown = logic.get_unknown_by_user(current_user.get_id(), lyrics.split())
    if not len(unknown):
        unknown = "Поздравляю, ты всё знаешь!"
    return render_template("pick.html", unknown=unknown, count=len(unknown))




@app.route('/train')
@login_required
def train():
    return render_template("train.html", last_words=['err', 'rter'])

@app.route('/rating')
@login_required
def rating():
    return render_template("rating.html", users=db.get_top_by_words())

@app.route('/add/', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        text = json.loads(request.data).get('text')
        db.add_word_to_user(current_user.get_id(), text)
        return 'nice'

@app.route('/delete/', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        text = json.loads(request.data).get('text')
        print(text)
        db.delete_word_from_user(current_user.get_id(), text)
        return 'great'






if __name__ == "__main__":
    app.run(debug=True)
