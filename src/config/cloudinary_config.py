import cloudinary
import cloudinary.uploader
import dotenv
import os

dotenv.load_dotenv()

cloudinary.config( 
    cloud_name = os.getenv("API_CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret = os.getenv("API_SECRET_KEY")
)

def upload_image(file_path):
    try:
        response = cloudinary.uploader.upload(
            file_path,
            folder="process_data"
        )
        return response["secure_url"]
    except Exception as e:
        return {"error": f"Lỗi khi upload ảnh: {str(e)}"}