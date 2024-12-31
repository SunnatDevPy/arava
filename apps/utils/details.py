from apps.models import Cart, ShopProductPhoto, ShopProduct, ShopProductCategory, PanelCategory, PanelProduct, Shop, User, OrderItem
from apps.models import Order


async def sum_from_shop(shop_id, user):
    carts: list['Cart'] = await Cart.get_cart_from_shop(user.id, shop_id)
    sum_ = 0
    price = 0
    for i in carts:
        product: 'ShopProduct' = await ShopProduct.get(i.product_id)
        if user.type == 'optom':
            sum_ += i.count * product.optom_price
            price = product.optom_price
        elif user.type == 'restorator':
            sum_ += i.count * product.restorator_price
            price = product.restorator_price
        else:
            sum_ += i.count * product.one_price
            price = product.one_price
    return sum_, price


async def detail_cart(shop_id, user_id):
    user = await User.get(user_id)
    carts: list['Cart'] = await Cart.get_cart_from_shop(user.id, shop_id)
    cart_ = []
    for i in carts:
        sum_ = 0
        product: 'ShopProduct' = await ShopProduct.get(i.product_id)
        if user.type == 'optom':
            sum_ += i.count * product.optom_price
            price = product.optom_price
        elif user.type == 'restorator':
            sum_ += i.count * product.restorator_price
            price = product.restorator_price
        else:
            sum_ += i.count * product.one_price
            price = product.one_price
        cart_.append({
            'id': i.id,
            "user_id": i.user_id,
            "shop_id": i.shop_id,
            "product_id": i.product_id,
            "count": i.count,
            "price": price,
            "sum": sum_
        })
    return cart_


# async def detail_cart2(shop_id, user_id):
#     user = await User.get(user_id)
#     carts: list['Cart'] = await Cart.get_cart_from_shop(shop_id, user.id)
#     cart_ = []
#     for i in carts:
#         sum_ = 0
#         product: 'Product' = await Product.get(i.product_id)
#         if user.type == 'optom':
#             sum_ += i.count * product.optom_price
#             price = product.optom_price
#         elif user.type == 'restorator':
#             sum_ += i.count * product.restorator_price
#             price = product.restorator_price
#         else:
#             sum_ += i.count * product.one_price
#             price = product.one_price
#         cart_.append({
#             'id': i.id,
#             "user_id": i.user_id,
#             "shop_id": i.shop_id,
#             "product_id": i.product_id,
#             "count": i.product_id,
#             "price": price,
#             "sum": sum_
#         })
#     return cart_


async def get_products_utils(shop_id):
    categories: list['ShopProductCategory'] = await ShopProductCategory.get_shop_categories(shop_id)
    category = []
    for i in categories:
        products: list['ShopProduct'] = await ShopProduct.get_products_category(i.id)
        category.append({'category': i, "products": products})
    return category


async def get_shops_unique_cart(carts):
    unique_ids = set()
    unique_cart = []
    for i in carts:
        shop = await Shop.get(i.shop_id)
        user = await User.get(i.user_id)
        sum_ = await sum_from_shop(shop.id, user)
        if shop.id not in unique_ids:
            unique_ids.add(shop.id)
            unique_cart.append({'id': shop.id, 'name': shop.name, "sum": sum_})
    return unique_cart


async def get_carts_(user_id):
    carts = await Cart.get_cart_from_user(user_id)
    shops = await get_shops_unique_cart(carts)
    list_ = []
    for i in shops:
        cart_from_shop = await Cart.get_cart_from_shop(user_id, i['id'])
        list_.append({"shop": i, "carts": cart_from_shop})
    return list_


async def check_sum_shops_from_cart(shop_id, user):
    carts: list['Cart'] = await Cart.get_cart_from_shop(user.id, shop_id)
    sum_ = await sum_from_shop(shop_id, user)
    shops = await Shop.all()


async def detail_orders(orders: list['Order']):
    detail_ = []
    for i in orders:
        order_items: list['OrderItem'] = await OrderItem.get_order_items(i.id)
        items = []
        for j in order_items:
            product = await ShopProduct.get(j.product_id)
            items.append({'name': product.name, "price": j.price_product, "count": j.count,
                          "total": j.price_product * j.count})
        detail_.append({"order": i, "order_items": items})
    return detail_
