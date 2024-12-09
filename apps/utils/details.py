from apps.models import Cart, Product, Category, Shop


async def get_sum_from_user(shop_id, user):
    carts: list['Cart'] = await Cart.get_cart_from_user(shop_id, user.id)
    sum_ = 0
    for i in carts:
        product = await Product.get(i.product_id)
        if user.type == 'OPTOM':
            sum_ += product.optom_price
        elif user.type == 'RESTORATOR':
            sum_ += product.restorator_price
        elif user.type == "ONE":
            sum_ += product.one_price
    return sum_


async def get_products_utils(shop_id):
    categories: list['Category'] = await Category.get_shop_categories(shop_id)
    category = []
    for i in categories:
        products: list['Product'] = await Product.get_products_category(i.id)
        category.append({'category': i, "products": products})
    return category


async def get_shops_unique_cart(carts):
    cart = []
    for i in carts:
        shop = await Shop.get(i.shop_id)
        m = {'id': shop.id, "name": shop.name}
        if m in carts:
            continue
        else:
            cart.append(m)
    return cart
