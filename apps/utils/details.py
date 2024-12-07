from apps.models import Cart, Product


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
