import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import db
from werkzeug.utils import secure_filename
from user import User
import logic
import json
import time
import base64
import ai_helper
 



#app config
DEBUG = True
SECRET_KEY = str(os.environ.get('flask_key'))
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
    return redirect(url_for('index'))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['email']) > 0 and len(request.form['psw']) > 0 and len(request.form['age']) > 0\
            and '@' in request.form['email'] \
            and request.form['psw'] == request.form['psw2'] \
            and request.form['age'].isdigit() and len(request.form['age']) < 4:
            hash = generate_password_hash(request.form['psw'])
            db.add_user(request.form['name'], request.form['email'], hash, int(request.form['age']))
            return redirect(url_for('login'))
        else:
            flash("Неверно заполнены поля", "error")
    return render_template("register.html")


@app.route('/profile')
@login_required
def profile():
    user_info = current_user.get_user()
    if user_info['photo'] is None:
        photo = '../static/images/profile_d.png'
    else:
        photo = f"data:image/jpeg;base64,{base64.b64encode(user_info['photo']).decode('utf-8')}"
    return render_template("profile.html",
                            photo = photo,
                            info=user_info,
                            word_count=db.get_word_count_by_user(current_user.get_id()),
                            song_count=db.get_song_count_by_user(current_user.get_id()),
                            age_since_redister=logic.get_age_by_date(user_info.get('joindate'))
            )

@app.route('/dictionary')
@login_required
def dictionary():
    words = db.get_words_by_user(current_user.get_id())
    return render_template("dictionary.html", words=words)

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
    lyrics = logic.get_lyrics(request.args.get('name'), request.args.get('author'))

    

    if request.method == "POST":
        flash('Добавлено', 'success')
        db.add_song_to_user(current_user.get_id(), request.form['track_name'], request.form['author'])
        db.add_full_lyrics(current_user.get_id(), lyrics)
        return redirect(url_for('study_track',  track_uuid=track_uuid, name=request.form['track_name'], author=request.form['author']))
    
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
    lyrics = logic.get_lyrics(request.args.get('name'), request.args.get('author'))
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
        db.delete_word_from_user(current_user.get_id(), text)
        return 'great'
    

@app.route('/get_explaination/', methods=['GET', 'POST'])
def get_explaination():
    if request.method == "POST":
        selected_text = json.loads(request.data).get('selectedText')
        return ai_helper.get_explanation(selected_text)
    

@app.route('/get_unknown/', methods=['POST'])
@login_required
def get_unknown():
    if request.method == "POST":
        email = current_user.get_id()
        lyrics_to_check = request.get_data(as_text=True)
        r = {'highlightedWords': logic.get_unknown_by_user(email, lyrics_to_check.split())}
        return r
    
@app.route('/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    avatar = request.files['avatar']
    filename = secure_filename(avatar.filename)
    photo_data = avatar.read()
    if logic.is_photo(filename):
        db.change_photo_by_user(current_user.get_id(), photo_data)
        return jsonify({'message': 'Аватарка успешно загружена'})
    return jsonify({'message': 'Неверный тип файла'})

@app.route('/change_user_translation', methods=['POST'])
@login_required
def change_user_translation():
    email = current_user.get_id()
    word = json.loads(request.data).get('word')
    translation = json.loads(request.data).get('translation')
    db.change_custom_translate(email, word, translation)
    return jsonify({'message': 'успех'})
    

if __name__ == "__main__":
    app.run(host='0.0.0.0')
