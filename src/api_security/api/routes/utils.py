from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def heath_check() -> dict[str, str]:
    return {"status": "OK"}
