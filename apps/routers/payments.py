from typing import Optional, Annotated

from fastapi import APIRouter, Form, HTTPException
from fastapi import Response
from pydantic import BaseModel
from starlette import status

from apps.models import User, Shop, WorkTimes, Payment

payment_router = APIRouter(prefix='/payment', tags=['Payment Shop'])


@payment_router.get(path='', name="Payment all")
async def list_category_shop():
    payments = await Payment.all()
    return {"payments": payments}


@payment_router.get(path='/detail', name="Get payments")
async def list_category_shop(payment_id: int):
    payments = await Payment.get(payment_id)
    if payments:
        return payments
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@payment_router.post(path='', name="Create payments")
async def list_category_shop(admin_id: int,
                             name: str = Form(),
                             status_: bool = Form(default=False),
                             token: str = Form()):
    user = await User.get(admin_id)
    if user:
        if user.status.value in ["admin", "superuser"]:
            await Payment.create(name=name, status=status_, token=token)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


class UpdatePayment(BaseModel):
    name: Optional[str] = None
    status: Optional[bool] = None
    token: Optional[str] = None


@payment_router.patch(path='', name="Update Payment")
async def list_category_shop(admin_id: int, payment_id: int, items: Annotated[UpdatePayment, Form()]):
    user = await User.get(admin_id)
    payment = await Payment.get(payment_id)
    if user and payment:
        if user.status.value in ["admin", "superuser"]:
            update_data = {k: v for k, v in items.dict().items() if v is not None}
            if update_data:
                await Payment.update(payment_id, **update_data)
                return {"ok": True}
            else:
                return Response("Nothing update", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yoq", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@payment_router.delete("", name="Delete Payment")
async def user_delete(operator_id: int, payment_id):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ["admin", "superuser"]:
            await Payment.delete(payment_id)
            return {"ok": True, 'id': payment_id}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")
