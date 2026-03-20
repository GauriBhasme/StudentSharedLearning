#starter template for a Flask web app
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#configure your app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)

#set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#set up routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/requests')
@login_required
def requests():
    return render_template('requests.html')

@app.route('/new_request', methods=['GET', 'POST'])
@login_required
def new_request():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_request = Request(title=title, description=description, user_id=current_user.id)
        db.session.add(new_request)
        db.session.commit()
        flash('Request submitted successfully!')
        return redirect(url_for('requests'))
    return render_template('new_request.html')
#run your app
if __name__ == '__main__':
    app.run(debug=True)
#TODO: add more routes and functionality as needed, such as editing and deleting requests, user registration, etc.