from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import openai
import base64
import json
from dotenv import load_dotenv
from food_analyzer import analyze_food_image  # Import our new module

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calorie_app.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    activity_level = db.Column(db.String(20))
    dietary_restrictions = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Use our new food analyzer function
def get_calories_from_image(image_path):
    return analyze_food_image(image_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        activity_level = request.form.get('activity_level')
        dietary_restrictions = request.form.get('dietary_restrictions')

        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(
            email=email,
            name=name,
            age=age,
            gender=gender,
            height=height,
            weight=weight,
            activity_level=activity_level,
            dietary_restrictions=dietary_restrictions
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({
            'error': 'No image provided',
            'calories': 'N/A',
            'nutritional_value': 'Analysis failed',
            'health_recommendation': 'Unable to provide recommendations',
            'food_items': [],
            'meal_balance': 'Analysis failed',
            'suggestions': 'Unable to provide suggestions'
        }), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({
            'error': 'No selected file',
            'calories': 'N/A',
            'nutritional_value': 'Analysis failed',
            'health_recommendation': 'Unable to provide recommendations',
            'food_items': [],
            'meal_balance': 'Analysis failed',
            'suggestions': 'Unable to provide suggestions'
        }), 400

    if file:
        try:
            # Check file type
            if not file.content_type.startswith('image/'):
                return jsonify({
                    'error': 'File is not an image',
                    'calories': 'N/A',
                    'nutritional_value': 'Analysis failed',
                    'health_recommendation': 'Unable to provide recommendations',
                    'food_items': [],
                    'meal_balance': 'Analysis failed',
                    'suggestions': 'Unable to provide suggestions'
                }), 400

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Analyze the image using our new function
            result = get_calories_from_image(filepath)
            
            # Check if there was an error in the analysis
            if 'error' in result and result['error']:
                app.logger.error(f"Error analyzing image: {result['error']}")
            
            return jsonify(result)
        except Exception as e:
            app.logger.error(f"Error processing image: {str(e)}")
            return jsonify({
                'error': str(e),
                'calories': 'N/A',
                'nutritional_value': 'Analysis failed',
                'health_recommendation': 'Unable to provide recommendations',
                'food_items': [],
                'meal_balance': 'Analysis failed',
                'suggestions': 'Unable to provide suggestions'
            }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
