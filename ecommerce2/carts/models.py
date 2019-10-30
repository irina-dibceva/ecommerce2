from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product

User = get_user_model()


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        # user_obj = None
        # if user is not None:
        #     if user.is_authenticated:
        #         user_obj = user
        user = user if user and user.is_authenticated else None
        is_created = False
        cart = self.model.objects.filter(user=user).order_by('-timestamp').first()
        if not cart:
            is_created = True
            cart = self.model.objects.create(user=user)
        return cart, is_created
        # return self.model.objects.get_or_create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    subtotal = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    # tax_percentage  = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
    # tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    # def update_subtotal(self):
    #     subtotal = 0
    #     items = self.cartitem_set.all()
    #     for item in items:
    #         subtotal += item.line_item_total
    #     self.subtotal = "%.2f" % (subtotal)
    #     self.save()


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)
