from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os
import uuid

app = FastAPI()

home_url = "example.com"

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount a static directory to serve uploaded files
app.mount("/static", StaticFiles(directory="uploads"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_homepage():
    content = """
    <html>
        <head>
            <title>Upload Static Files</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                form {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333;
                }
                input[type="file"] {
                    margin-bottom: 20px;
                }
                input[type="submit"] {
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>Static Site Uploader</h1>
            <form action="/upload/" enctype="multipart/form-data" method="post">
                HTML: <input type="file" name="html"><br><br>
                CSS: <input type="file" name="css"><br><br>
                JS: <input type="file" name="js"><br><br>
                <input type="submit">
            </form>
        </body>
    </html>
    """
    return content

@app.post("/upload/")
async def upload_files(html: UploadFile = File(...), css: UploadFile = File(...), js: UploadFile = File(...)):
    # Create a unique directory for this set of uploads
    unique_dir = str(uuid.uuid4())
    os.makedirs(os.path.join(UPLOAD_FOLDER, unique_dir), exist_ok=True)

    file_mappings = {'html': html, 'css': css, 'js': js}
    for file_type, file in file_mappings.items():
        filename = f'index.{file_type}' if file_type == 'html' else f'style.{file_type}' if file_type == 'css' else f'script.{file_type}'
        file_location = os.path.join(UPLOAD_FOLDER, unique_dir, filename)

        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

    return {"message": f"Files uploaded successfully! Access your site at: {home_url}/static/{unique_dir}/index.html"}

@app.get("/site/{unique_dir}/")
async def serve_site(unique_dir: str):
    file_path = os.path.join(UPLOAD_FOLDER, unique_dir, 'index.html')
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Item not found")
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
