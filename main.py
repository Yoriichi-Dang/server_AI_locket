from fastapi import FastAPI, File, UploadFile
from PIL import Image
from model import vqa, image_caption, image_text_retrieval
from io import BytesIO
import os

app = FastAPI()
SAVE_DIRECTORY = "uploaded_images"
os.makedirs(SAVE_DIRECTORY, exist_ok=True)

@app.post("/image-caption")
async def image_captioning(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return {"error": "File không phải là ảnh JPEG hoặc PNG"}
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        file_path = os.path.join(SAVE_DIRECTORY, file.filename)
        image.save(file_path)
        return image_caption(image=file_path)

    except Exception as e:
        return {"error": f"Lỗi khi xử lý ảnh: {str(e)}"}
@app.post("/vqa")
async def image_visual_question_answer(file: UploadFile = File(...), question: str = ""):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return {"error": "File không phải là ảnh JPEG hoặc PNG"}
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        file_path = os.path.join(SAVE_DIRECTORY, file.filename)
        image.save(file_path)
    except Exception as e:
        return {"error": f"Lỗi khi xử lý ảnh: {str(e)}"}

@app.post("/image-text-retrieval")
async def image_text_retrieval_endpoint(file: UploadFile = File(...), text: str = ""):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return {"error": "File không phải là ảnh JPEG hoặc PNG"}

    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        file_path = os.path.join(SAVE_DIRECTORY, file.filename)
        image.save(file_path)
        return image_text_retrieval(file_path, text)
    except Exception as e:
        return {"error": f"Lỗi khi xử lý ảnh: {str(e)}"}
