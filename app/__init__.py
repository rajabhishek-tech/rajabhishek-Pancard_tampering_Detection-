from flask import Flask

app = Flask(__name__)

# Configuration settings
app.config['UPLOADS_FOLDER'] = 'app/static/uploads'
app.config['EXISTING_IMAGES_FOLDER'] = 'app/static/original'
app.config['GENERATED_IMAGES_FOLDER'] = 'app/static/generated'
app.config['ENV'] = 'development'  # Set a default value for 'ENV'

if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from app import views