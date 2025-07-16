import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MONGO_URI = "mongodb+srv://dummy:1234@cluster0.6wr4bga.mongodb.net/sprintzeal?retryWrites=true&w=majority&appName=Cluster0"
SECRET_KEY = "supersecret"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
