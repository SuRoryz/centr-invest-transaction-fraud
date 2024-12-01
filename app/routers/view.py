from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["views"])
templates = Jinja2Templates(directory="build")

@router.get("/")
async def auth(req: Request):
    return templates.TemplateResponse('index.html', {'request': req})

@router.get("/{any}")
async def auth(any: str, req: Request):
    return templates.TemplateResponse('index.html', {'request': req})