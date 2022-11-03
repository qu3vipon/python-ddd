from fastapi import APIRouter

router = APIRouter(prefix="/reception")


@router.get("/reservations")
def get_reservations(

):

    return


@router.post("/reservations")
def post_reservations():
    return


@router.patch("/reservations/{reservation_number}")
def patch_reservation():
    return


@router.post("/reservations/{reservation_number}/check-in")
def post_reservation_check_in(
):
    return


@router.post("/reservations/{reservation_number}/check-out")
def post_reservation_check_out():
    return


@router.post("/reservations/{reservation_number}/cancel")
def post_reservation_cancel():
    return