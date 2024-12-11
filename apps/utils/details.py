from apps.models import Cart, Product, Category, Shop, User


async def sum_from_shop(shop_id, user):
    carts: list['Cart'] = await Cart.get_cart_from_shop(user.id, shop_id)
    sum_ = 0
    for i in carts:
        product: 'Product' = await Product.get(i.product_id)
        if user.type == 'optom':
            sum_ += i.count * product.optom_price
        elif user.type == 'restorator':
            sum_ += i.count * product.restorator_price
        else:
            sum_ += i.count * product.one_price
    return sum_


async def detail_cart(shop_id, user_id):
    user = await User.get(user_id)
    carts: list['Cart'] = await Cart.get_cart_from_shop(user.id, shop_id)
    cart_ = []
    for i in carts:
        sum_ = 0
        product: 'Product' = await Product.get(i.product_id)
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
    categories: list['Category'] = await Category.get_shop_categories(shop_id)
    category = []
    for i in categories:
        products: list['Product'] = await Product.get_products_category(i.id)
        category.append({'category': i, "products": products})
    return category


async def get_shops_unique_cart(carts):
    unique_ids = set()
    unique_cart = []

    for i in carts:
        shop = await Shop.get(i['shop_id'])
        user = await User.get(i['user_id'])
        sum_ = await sum_from_shop(shop.id, user)
        if shop.id not in unique_ids:
            unique_ids.add(shop.id)
            unique_cart.append({'id': shop.id, 'name': shop.name, "sum": sum_})
    return unique_cart


async def check_sum_shops_from_cart(shop_id, user):
    carts: list['Cart'] = await Cart.get_cart_from_shop(user.id, shop_id)
    sum_ = await sum_from_shop(shop_id, user)
    shops = await Shop.all()
