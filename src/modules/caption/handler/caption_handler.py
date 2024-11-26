from fastapi import  File, UploadFile,Form
from PIL import Image
from io import BytesIO
from src.modules.caption.service.caption_service import CaptionService
import os
from fastapi import APIRouter, HTTPException,Response
from fastapi.responses import JSONResponse
from src.config.cloudinary_config import upload_image
import requests
from pydantic import BaseModel

class ImageURLRequest(BaseModel):
    image_url: str
SAVE_DIRECTORY = "uploaded_images"
os.makedirs(SAVE_DIRECTORY, exist_ok=True)
caption_service = CaptionService()
router = APIRouter()

@router.post(
    "/image-caption",
    summary="Generate image caption",
    description="This endpoint generates a caption for the given image URL.",
    tags=["Image Caption"]
)
async def image_captioning(request: ImageURLRequest):
    try:
        response = requests.get(request.image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Unable to fetch image from the provided URL.")
        content_type = response.headers.get("Content-Type")
        if content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            raise HTTPException(status_code=400, detail="The provided URL does not point to a JPEG or PNG image.")
        image = Image.open(BytesIO(response.content))
        file_name = os.path.basename(request.image_url)
        file_path = os.path.join(SAVE_DIRECTORY, file_name)
        image.save(file_path)
        cloud_file_path = upload_image(file_path)
        print(cloud_file_path)
        result = caption_service.image_caption(image=cloud_file_path)
        os.remove(file_path)
        return result

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        return {"error": f"An error occurred while processing the image: {str(e)}"}
    
@router.post("/vqa",tags=["Image Caption"])
async def image_visual_question_answer(
    question: str = Form(...),  # Use Form to get form data
    file: UploadFile = File(...),  # Use File to get the uploaded image
):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        return {"error": "File is not a JPEG or PNG image"}
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        file_path = os.path.join(SAVE_DIRECTORY, file.filename)
        image.save(file_path)
        cloud_file_path = upload_image(file_path)
        print(cloud_file_path)
        result = caption_service.vqa(image=cloud_file_path, question=question)
        os.remove(file_path)  # Remove the image from local storage
        return JSONResponse(status_code=201, content={
            "answer":result
        })
    except Exception as e:
        return {"error": f"Error processing image: {str(e)}"}

@router.post("/image-text-retrieval",tags=["Image Caption"] )
async def image_text_retrieval_endpoint(question: str = Form(...), files: list[UploadFile] = File(...)):
    for file in files:
        if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            return {"error": f"File {file.filename} không phải là ảnh JPEG hoặc PNG"}
    try:
        file_paths = []
        for file in files:
            contents = await file.read()
            image = Image.open(BytesIO(contents))
            file_path = os.path.join(SAVE_DIRECTORY, file.filename)
            print(file_path)
            image.save(file_path)
            file_paths.append(file_path)
        results = caption_service.image_text_retrieval(file_paths, question)  # Call your image_text_retrieval function here
        return {"results": results}
    except Exception as e:
        return {"error": f"Lỗi khi xử lý ảnh: {str(e)}"}
