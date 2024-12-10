from apps.models import Cart, Product, Category, Shop, User


async def sum_from_shop(shop_id, user):
    carts: list['Cart'] = await Cart.get_cart_from_shop(shop_id, user.id)
    sum_ = 0
    for i in carts:
        product: 'Product' = await Product.get(i.product_id)
        if user.type == 'optom':
            sum_ += i.count * product.optom_price
        elif user.type == 'restorator':
            sum_ += i.count * product.restorator_price
        elif user.type == "one":
            sum_ += i.count * product.one_price
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
        user = await User.get(i.user_id)
        sum_ = await sum_from_shop(i.shop_id, user.id)
        if shop.id not in unique_ids:
            unique_ids.add(shop.id)
            unique_cart.append({'id': shop.id, 'name': shop.name, "sum": sum_})
    return unique_cart
