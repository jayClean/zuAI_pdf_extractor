from models.paper import Paper  # Adjust the import based on your project structure
from repositories.task_repository import TaskRepository
from models.task import ExtractionTask
from fastapi import HTTPException
from vertexai.generative_models import GenerativeModel, Part
from database import database
import os
import vertexai

# Initialize Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Initialize collections and repository
task_collection = database["tasks"]
task_repo = TaskRepository(collection=task_collection)

async def extract_and_convert_to_json(pdf_uri: str) -> str:
    # Create a new task with status "pending"
    task = ExtractionTask(status="pending", type="pdf_extraction")
    task_id = await task_repo.create_task(task)

    try:
        # Initialize the generative model
        model = GenerativeModel("gemini-1.5-flash-002")

        # Update the prompt with specific instructions and an example
        prompt = """
        You are a professional document extraction specialist. Please extract the text from the PDF file
        and structure it according to the following JSON format for a sample paper:
        
        {
            "title": "Title of the paper",
            "type": "mock_test",
            "time": 120,
            "marks": 80,
            "params": {
                "board": "CBSE",
                "grade": 9,
                "subject": "Maths"
            },
            "tags": [
                "algebra",
                "linear equations"
            ],
            "chapters": [
                "Linear Equations",
                "Polynomials"
            ],
            "sections": [
                {
                    "marks_per_question": 4,
                    "type": "default",
                    "questions": [
                        {
                            "question": "Sample question",
                            "answer": "Sample answer",
                            "type": "short",
                            "question_slug": "unique-question-slug",
                            "reference_id": "QID001",
                            "hint": "Hint for the question",
                            "params": {}
                        }
                    ]
                }
            ]
        }
        
        Ensure that each section and question is extracted and structured properly. Please maintain the hierarchy and include relevant metadata.
        """

        # Prepare the PDF file as input
        pdf_file = Part.from_uri(uri=pdf_uri, mime_type="application/pdf")
        
        # Call the model asynchronously
        response = await model.generate_content_async([pdf_file, prompt])
        
        # Convert the response to the Paper model
        structured_data = Paper.parse_raw(response.text)

        # Update the task status to "completed" with the extracted data
        await task_repo.update_task(task_id, "completed", {"extracted_data": structured_data.dict()})
    except Exception as e:
        # Update the task status to "failed" and store the error message
        await task_repo.update_task(task_id, "failed", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"PDF extraction failed: {str(e)}")

    return task_id

async def extract_and_convert_text_to_json(text: str) -> str:
    # Create a new task with status "pending"
    task = ExtractionTask(status="pending", type="text_extraction")
    task_id = await task_repo.create_task(task)

    try:
        # Initialize the generative model
        model = GenerativeModel("gemini-1.5-flash-002")

        # Update the prompt with specific instructions and an example
        prompt = """
        You are a professional document extraction specialist. Please extract and structure the given plain text
        into the following JSON format for a sample paper:
        
        {
            "title": "Title of the paper",
            "type": "mock_test",
            "time": 120,
            "marks": 80,
            "params": {
                "board": "CBSE",
                "grade": 9,
                "subject": "Maths"
            },
            "tags": [
                "algebra",
                "linear equations"
            ],
            "chapters": [
                "Linear Equations",
                "Polynomials"
            ],
            "sections": [
                {
                    "marks_per_question": 4,
                    "type": "default",
                    "questions": [
                        {
                            "question": "Sample question",
                            "answer": "Sample answer",
                            "type": "short",
                            "question_slug": "unique-question-slug",
                            "reference_id": "QID001",
                            "hint": "Hint for the question",
                            "params": {}
                        }
                    ]
                }
            ]
        }
        
        Ensure that each section and question is properly structured. Maintain the hierarchy and include any relevant metadata.
        """

        # Call the model asynchronously
        response = await model.generate_content_async([text, prompt])
        
        # Convert the response to the Paper model
        structured_data = Paper.parse_raw(response.text)

        # Update the task status to "completed" with the extracted data
        await task_repo.update_task(task_id, "completed", {"extracted_data": structured_data.dict()})
    except Exception as e:
        # Update the task status to "failed" and store the error message
        await task_repo.update_task(task_id, "failed", {"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")

    return task_id
