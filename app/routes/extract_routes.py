from fastapi import APIRouter, HTTPException, Body
from services.extract_service import extract_and_convert_to_json, extract_and_convert_text_to_json
from database import database
from repositories.task_repository import TaskRepository

task_collection = database["tasks"]
task_repository = TaskRepository(collection=task_collection)


router = APIRouter()

@router.post("/pdf/extract-and-convert")
async def extract_and_convert_pdf_endpoint(pdf_uri: str):
    try:
        task_id = await extract_and_convert_to_json(pdf_uri)
        return {"task_id": task_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/text/extract-and-convert")
async def extract_and_convert_text_endpoint(text: str = Body(..., example="Your plain text goes here")):
    try:
        task_id = await extract_and_convert_text_to_json(text)
        return {"task_id": task_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    try:
        task = await task_repository.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"task_id": task_id, "status": task.get("status"), "data": task.get("data")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
