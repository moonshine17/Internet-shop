from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render
from django.template import context
from traitlets import default

from goods.models import Products
from goods.utils import q_search


# Create your views here.
def catalog(request, category_slug=None):
    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)
        
    if order_by and order_by != "default":
        if order_by == 'price':
            # Сортировка по возрастанию цены с учетом скидки
            goods = sorted(goods, key=lambda x: x.total_price())
        elif order_by == '-price':
            # Сортировка по убыванию цены с учетом скидки
            goods = sorted(goods, key=lambda x: x.total_price(), reverse=True)

    paginator = Paginator(goods, 6)
    current_page = paginator.page(int(page))

    context = {
        "title": "OLI catalog",
        "goods": current_page,  
        "slug_url": category_slug,
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    context = {"product": product}

    return render(request, "goods/product.html", context=context)
