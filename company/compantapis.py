from doctest import FAIL_FAST
from fastapi import APIRouter

router=APIRouter()

@router.get("/")
async def get_company_name():
    return {"Company Name": "Example Company LOC"}

@router.get("/employees")
async def get_employees():
    return 162