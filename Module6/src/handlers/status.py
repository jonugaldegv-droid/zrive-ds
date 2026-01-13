from fastapi import APIRouter

router = APIRouter() 

@router.get("/status")
async def get_status():
    return "200: Status OK"
