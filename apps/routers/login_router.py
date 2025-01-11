from fastapi import APIRouter, Form, HTTPException
from fastapi import Response
from starlette import status

from apps.models import User, Shop, Cart, PanelProduct
from apps.models.users import LoginModel
from apps.utils.details import sum_from_shop, get_shops_unique_cart, detail_cart, get_carts_

