from flask import Flask, render_template, request, send_from_directory, abort
from werkzeug.utils import safe_join
import os
import uuid

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        # Create a unique directory for this set of uploads
        unique_dir = str(uuid.uuid4())
        os.makedirs(os.path.join(UPLOAD_FOLDER, unique_dir), exist_ok=True)

        # Save the uploaded files
        for file_type in ['html', 'css', 'js']:
            file = request.files.get(file_type)
            if file:
                filename = f'index.{file_type}' if file_type == 'html' else f'style.{file_type}' if file_type == 'css' else f'script.{file_type}'
                file.save(os.path.join(UPLOAD_FOLDER, unique_dir, filename))

        return f'Files uploaded successfully! Access your site at: /site/{unique_dir}'

    return '''
    <!doctype html>
    <title>Upload your Static Site files</title>
    <h1>Upload HTML, CSS, and JavaScript files</h1>
    <form method=post enctype=multipart/form-data>
      HTML: <input type=file name=html><br>
      CSS: <input type=file name=css><br>
      JS: <input type=file name=js><br>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/site/<path:unique_dir>/<path:filename>')
def serve_file(unique_dir, filename):
    safe_path = safe_join(app.config['UPLOAD_FOLDER'], unique_dir)
    try:
        return send_from_directory(safe_path, filename)
    except FileNotFoundError:
        abort(404)

@app.route('/site/<path:unique_dir>/')
def serve_site(unique_dir):
    return serve_file(unique_dir, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)