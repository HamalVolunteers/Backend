from fastapi import FastAPI
from pydantic import BaseModel
import parser as parser
from typing import Any

class RequestModel(BaseModel):
    action: str
    payload: dict | None = None


class ResponseModel(BaseModel):
    status: str
    data: Any = None


app = FastAPI()
parserObject = parser.Parser()

@app.post("/api", response_model=ResponseModel)
async def handle_request(request: RequestModel):
    # Send the request to the parser
    result = parserObject.parse({
    "action": request.action,
    "payload": request.payload or {}
})
    if "status" not in result:
        return {"status": "error", "data": None}
    if "data" not in result:
        result["data"] = None
    return result
