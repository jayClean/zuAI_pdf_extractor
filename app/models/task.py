from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from bson import ObjectId

# Custom field for MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# The Task model
class ExtractionTask(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    status: str
    type: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    details: Optional[Dict] = None  # Holds any additional information like extracted data or error message

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "60d5f4a5b6f67c001c8e4df7",
                "status": "pending",
                "type": "pdf_extraction",
                "created_at": "2024-10-01T12:34:56.789Z",
                "updated_at": "2024-10-01T12:34:56.789Z",
                "details": {
                    "extracted_data": {},  # Example structured data or error message
                },
            }
        }
