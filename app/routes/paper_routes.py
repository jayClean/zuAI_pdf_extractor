from fastapi import APIRouter, HTTPException
from app.models.paper import Paper
from app.services.paper_service import create_paper, get_paper, update_paper, delete_paper
from services.cache_service import get_cache, set_cache
import logging

router = APIRouter()

@router.post("/", response_model=str)
async def create_new_paper(paper: Paper):
    try:
        # Attempt to create a paper
        result = await create_paper(paper)
        print(result)
        return result
    except Exception as e:
        # Log the exception
        logging.error(f"Error creating paper: {e}")
        # Return a detailed error message
        raise HTTPException(status_code=400, detail=f"An error occurred while creating the paper: {str(e)}")

@router.get("/{paper_id}", response_model=Paper)
async def get_paper(paper_id: str):
    # Define the cache key
    cache_key = f"paper:{paper_id}"

    # Check if the paper is in the cache
    cached_paper = await get_cache(cache_key)
    if cached_paper:
        return cached_paper

    # If not in the cache, fetch from the database
    paper = await get_paper(paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    # Cache the result
    await set_cache(cache_key, paper.dict())

    return paper

@router.put("/{paper_id}", response_model=bool)
async def update_existing_paper(paper_id: str, paper: Paper):
    return await update_paper(paper_id, paper)

@router.delete("/{paper_id}", response_model=bool)
async def delete_existing_paper(paper_id: str):
    return await delete_paper(paper_id)
