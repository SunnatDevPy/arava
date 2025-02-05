from apps.models import Cart, ShopProductPhoto, ShopProduct, ShopCategory, PanelCategory, PanelProduct, Shop, \
    AdminPanelUser,BotUser, OrderItem
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
    user = await BotUser.get(user_id)
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
            "user_id": i.bot_user_id,
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
    categories: list['ShopCategory'] = await ShopCategory.get_shop_categories(shop_id)
    category = []
    for i in categories:
        products: list['ShopProduct'] = await ShopProduct.get_products_category(i.id)
        prod = []
        for i in products:
            shtrix_code = await PanelProduct.get_product_shtrix(i.shtrix_code)
            if i.photo == None:
                prod.append({'product': i, "photo": shtrix_code.photo})
            else:
                prod.append({'product': i, "photo": shtrix_code.photo})
        category.append({'category': i, "products": prod})
    return category


async def get_shops_unique_cart(carts):
    unique_ids = set()
    unique_cart = []

    for i in carts:
        shop = await Shop.get(i.get('shop_id'))
        user = await BotUser.get(i.get("user_id"))
        sum_ = await sum_from_shop(shop.id, user)
        if shop.id not in unique_ids:
            unique_ids.add(shop.id)
            unique_cart.append({'id': shop.id, 'name': shop.name, "sum": sum_})
    return unique_cart


async def get_shops_unique(carts):
    unique_ids = set()
    unique_cart = []

    for i in carts:
        shop = await Shop.get(i.shop_id)
        user = await BotUser.get(i.user_id)
        sum_ = await sum_from_shop(shop.id, user)
        if shop.id not in unique_ids:
            unique_ids.add(shop.id)
            unique_cart.append({'id': shop.id, 'name': shop.name, "sum": sum_})
    return unique_cart


async def get_carts_(user_id):
    carts = await Cart.get_cart_from_user(user_id)
    shops = await get_shops_unique(carts)
    list_ = []
    for i in shops:
        cart_from_shop = await Cart.get_cart_from_shop(user_id, i['id'])
        list_.append({"shop": i, "carts": cart_from_shop, "optimal_price": await get_cheapest_shops(user_id, i['id'])})
    return list_


# async def check_sum_shops_from_cart(shop_id, user):
#     carts: list['Cart'] = await Cart.get_cart_from_shop(user.id, shop_id)
#     sum_ = await sum_from_shop(shop_id, user)
#     shops = await Shop.all()


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


# async def detail_orders_all_statuses(orders: list['Order']):
#     detail_ = []
#     for i in orders:
#         order_items: list['OrderItem'] = await OrderItem.get_order_items(i.id)
#         items = []
#         for j in order_items:
#             product = await ShopProduct.get(j.product_id)
#             items.append({'name': product.name, "price": j.price_product, "count": j.count,
#                           "total": j.price_product * j.count})
#         detail_.append({"order": i, "order_items": items})
#     return detail_


async def update_products(products):
    list_ = []
    for i in products:
        shop = await Shop.get(i.shop_id)
        i.shop = shop
        list_.append(i)
    return list_


# Оптимизация корзины
async def get_cheapest_shops(user_id: int, shop_id: int):
    shops: list['Shop'] = await Shop.all()
    carts: list['Cart'] = await Cart.get_cart_from_shop(user_id, shop_id)
    shop_totals = []

    for shop in shops:
        total_cost = 0
        all_products_available = True

        for cart_item in carts:
            product = await ShopProduct.get_products_from_shop2(shop.id, cart_item.shtrix_code)

            if not product:
                all_products_available = False
                break

            price = product.one_price
            total_cost += price * cart_item.count

        if all_products_available:
            if shop.id != shop_id:
                shop_totals.append({"shop_name": shop.name, "total_cost": total_cost})

    sorted_shops = sorted(shop_totals, key=lambda x: x["total_cost"])[:3]
    return sorted_shops


async def detail_order(order: Order):
    order_items: list['OrderItem'] = await OrderItem.get_order_items(order.id)
    text = ''
    count = 1
    for i in order_items:
        product = await ShopProduct.get(i.product_id)
        text += f"{count}) {product.name} {i.price_product} x {i.count} = {i.price_product * i.count}\n"
    return f"""
<b>Buyurtma soni</b>: {order.id}
<b>Ism-Familiya</b>: {order.last_first_name}
<b>Manzil</b>: {order.address}
<b>Tel</b>: {order.phone}
<b>To'lov turi</b>: {order.payment_name}

<b>Mahsulotlar</b>
{text}

<b>Yo'l kira narxi</b>: {order.driver_price}
<b>Umumiy summa</b>: {order.total_sum}
    """
