from fastapi import FastAPI

from app.schemas import PostingRequest
from app.services.posting_service import post_to_all_platforms

app = FastAPI(
    title="Automated Multi-Platform Posting System",
    version="1.0.0",
)

@app.post("/posting")
async def create_post(request: PostingRequest):
    results = await post_to_all_platforms(request.message)

    return {
        "success": any(result["status"] == "success" for result in results),
        "results": results,
    }