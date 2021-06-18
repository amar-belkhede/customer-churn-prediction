from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from churnprediction import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    churns = db.relationship('Churn', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Churn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Text, nullable=False)
    seniorCitizen = db.Column(db.Text, nullable=False)
    partner = db.Column(db.Text, nullable=False)
    dependents = db.Column(db.Text, nullable=False)
    tenure = db.Column(db.Text, nullable=False)
    phoneService = db.Column(db.Text, nullable=False)
    multipleLines = db.Column(db.Text, nullable=False)
    internetService = db.Column(db.Text, nullable=False)
    onlineSecurity = db.Column(db.Text, nullable=False)
    onlineBackup = db.Column(db.Text, nullable=False)
    deviceProtection = db.Column(db.Text, nullable=False)
    techSupport = db.Column(db.Text, nullable=False)
    streamingTV = db.Column(db.Text, nullable=False)
    streamingmovies = db.Column(db.Text, nullable=False)
    contract = db.Column(db.Text, nullable=False)
    paperlessBilling = db.Column(db.Text, nullable=False)
    paymentMethod = db.Column(db.Text, nullable=False)
    monthlyCharges = db.Column(db.Text, nullable=False)
    totalcharges = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"