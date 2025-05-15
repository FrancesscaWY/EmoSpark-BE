from fastapi import APIRouter, UploadFile,File
from starlette.responses import JSONResponse

from app.modules.image.analyze_emotion_image import analyze_emotion_from_image

router = APIRouter()

@router.post("/child/emotion-analyze")
async def get_emotion(file:UploadFile = File(...)):
    try:
        image_data = await file.read()

        # 调用 analyze_emotion_from_image 进行情绪分析
        result = analyze_emotion_from_image(image_data)

        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error":str(e)})
