from flask import Flask, render_template, request
import os
import uuid
from werkzeug.utils import secure_filename

# Configuration
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'avi'}
UPLOAD_FOLDER = os.path.join('static', 'reels')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function to validate file
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Upload (create) route
@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()

    if request.method == "POST":
        req_id = request.form.get("uuid")
        desc = request.form.get("text")

        for key, file in request.files.items():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                print("Saved to:", filepath)

        # Save description (optional)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], "desc.txt"), "w") as f:
            f.write(desc)

    return render_template("create.html", myid=myid)

# Gallery route
@app.route("/gallery")
def gallery():
    reels = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith(('.mp4', '.webm', '.avi'))]
    print("Files in gallery:", reels)
    return render_template("gallery.html", reels=reels)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
