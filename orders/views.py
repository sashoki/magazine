# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import OrderCreated
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

@staff_member_required
def AdminOrderDetail(request, order_id):
    order =get_object_or_404(Order, id=order_id)
    return render(request, 'orders/admin/orders/order/detail.html', {'order': order})

@staff_member_required
def AdminOrderPDF(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
               stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + '/bootstrap-3.3.7/css/bootstrap.min.css')])
    return response


def OrderCreate(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            if cart.cupon:
                order.cupon = cart.cupon
                order.discount = cart.cupon.discount
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # Асинхронная отправка сообщения
            OrderCreated.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))

    form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart,
                                                        'form': form})
