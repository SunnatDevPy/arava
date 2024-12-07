import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from apps.admin import ProductAdmin, CategoryAdmin, ProductPhotoAdmin, MainPhotoAdmin
from apps.models import db
from apps.routers import product_router, user_router, shop_category_router, \
    main_photos_router, category_router
from apps.routers.cart import cart_router
from apps.routers.orders import order_router
from apps.routers.shop import shop_router
from config import conf


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists('static'):
        os.mkdir('static')

    app.mount("/static", StaticFiles(directory='static'), name='static')
    app.include_router(user_router)
    app.include_router(product_router)
    # app.include_router(generate_router)
    app.include_router(shop_router)
    app.include_router(shop_category_router)
    app.include_router(main_photos_router)
    app.include_router(order_router)
    app.include_router(category_router)
    app.include_router(cart_router)
    await db.create_all()
    yield


# from minio import Minio
# minioClient = Minio('127.0.0.1:9000',
#                 access_key='xxxx',
#                 secret_key='xxxx',
#                 secure=False)

app = FastAPI(docs_url="/docs", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=conf.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "https://arava1.vercel.app"],
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(app, db._engine)
admin.add_view(ProductAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(ProductPhotoAdmin)
admin.add_view(MainPhotoAdmin)

# @app.get("/media/{full_path:path}", name='media')
# async def get_media(full_path):
#     image_path = Path(f'media/{full_path}')
#     if not image_path.is_file():
#         return Response("Image not found on the server", status.HTTP_404_NOT_FOUND)
#     return FileResponse(image_path)
#
#
# @app.exception_handler(status.HTTP_401_UNAUTHORIZED)
# def auth_exception_handler(request: Request, exc):
#     return RedirectResponse(request.url_for('login_page'))
#

# @app.get("/banner", name="Banner photos")
# async def list_photo_banner():
#     list_ = []
#     image_path = os.listdir('media/banner')
#     if not image_path:
#         return Response("Image not found on the server", status.HTTP_404_NOT_FOUND)
#     for i in image_path:
#         file_path = 'media/banners/' + i
#         if i.endswith('png'):
#             type = 'png'
#         else:
#             type = 'jpeg'
#         list_.append(FileResponse(file_path, media_type=f"image/{type}", filename=i))
#     return {"banner": list_}
#
#
# @app.get(path='/photo-all/', name="Get Shop Photos all")
# async def list_category_shop():
#     return {'shop-photos': await ShopPhoto.all()}
