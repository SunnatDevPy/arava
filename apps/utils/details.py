from apps.models import Cart, Product, Category, Shop


async def get_sum_from_user(shop_id, user):
    carts: list['Cart'] = await Cart.get_cart_from_shop(shop_id, user.id)
    sum_ = 0
    for i in carts:
        sum_ = i.total_sum
    return sum_


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
        shop = await Shop.get(i.shop_id)
        if shop.id not in unique_ids:
            unique_ids.add(shop.id)
            unique_cart.append({'id': shop.id, 'name': shop.name})

    return unique_cart
