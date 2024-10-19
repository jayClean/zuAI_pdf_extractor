from app.database import paper_collection
from app.models.paper import Paper
from bson import ObjectId
from services.cache_service import invalidate_cache

async def create_paper(paper: Paper):
    paper_dict = paper.dict()
    print(paper_dict)
    result = await paper_collection.insert_one(paper_dict)
    return str(result.inserted_id)

async def get_paper(paper_id: str):
    paper = await paper_collection.find_one({"_id": ObjectId(paper_id)})
    if paper:
        paper["id"] = str(paper["_id"])
        return paper

async def update_paper(paper_id: str, paper_data: Paper):
    update_result = await paper_collection.update_one(
        {"_id": ObjectId(paper_id)}, {"$set": paper_data.dict()}
    )
    if update_result.modified_count:
        # Invalidate cache for this paper
        await invalidate_cache(f"paper:{paper_id}")
    return update_result.modified_count > 0

async def delete_paper(paper_id: str):
    delete_result = await paper_collection.delete_one({"_id": ObjectId(paper_id)})
    if delete_result.deleted_count:
        # Invalidate cache for this paper
        await invalidate_cache(f"paper:{paper_id}")
    return delete_result.deleted_count > 0
