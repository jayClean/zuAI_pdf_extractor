from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import Optional, Dict, Any

class TaskRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create_task(self, task_data: Dict[str, Any]) -> str:
        """Create a new task and return its ID."""
        result = await self.collection.insert_one(task_data)
        return str(result.inserted_id)

    async def update_task(self, task_id: str, status: str, data: Optional[Dict[str, Any]] = None):
        """Update the status of a task and optionally set its data."""
        update_fields = {"status": status}
        if data:
            update_fields["data"] = data
        await self.collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_fields})

    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a task by its ID."""
        task = await self.collection.find_one({"_id": ObjectId(task_id)})
        return task
