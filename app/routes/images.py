from fastapi import APIRouter

router = APIRouter(prefix="/images")


@router.get("")
def leaderboards_get():
    pass


@router.post("")
def leaderboards_post():
    pass


@router.delete("")
def leaderboards_delete():
    pass
