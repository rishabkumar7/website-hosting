from fastapi.testclient import TestClient
from fast import app

client = TestClient(app)

def test_read_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']

def test_upload_files():
    # Create some dummy files to upload
    files = {
        "html": ("index.html", "<html><body>Hello</body></html>", "text/html"),
        "css": ("style.css", "body {background: red;}", "text/css"),
        "js": ("script.js", "console.log('Hello')", "application/javascript"),
    }
    response = client.post("/upload/", files=files)
    assert response.status_code == 201
    # You can add more assertions here based on what your /upload/ endpoint returns
