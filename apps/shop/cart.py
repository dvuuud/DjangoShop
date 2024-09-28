from .models import Product

CART_SESSION_ID = 'cart'  # Определяем идентификатор сессии корзины

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """Удаляет товар из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def get_items(self):
        """Возвращает список всех товаров в корзине."""
        items = []
        for product_id, item in self.cart.items():
            items.append({
                'product': Product.objects.get(id=product_id),  # Получаем объект продукта
                'quantity': item['quantity'],
                'price': item['price'],
            })
        return items

    def get_total_price(self):
        """Возвращает общую стоимость товаров в корзине."""
        total = 0
        for item in self.cart.values():
            total += int(item['price']) * item['quantity']
        return total
