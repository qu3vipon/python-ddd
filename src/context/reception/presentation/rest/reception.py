from fastapi import APIRouter

router = APIRouter(prefix="/display")


@router.get("/rooms")
def get_rooms():
    return


@router.post("/rooms")
def post_rooms():
    return
