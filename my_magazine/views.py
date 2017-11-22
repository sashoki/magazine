from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from my_magazine.models import Product, Comments, Category, Keywords, Brands, Author, Home
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404
from forms import CommentForm, BrandsForm, KeywordsForm
from django.core.context_processors import csrf
from django.contrib import auth
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm


def index(request):
    return render(request, 'index.html')


def products(request, page_number=1):
    brands_form = BrandsForm
    keywords_form = KeywordsForm
    args = {}
    all_products = Product.objects.filter(product_available=True)
    current_page = Paginator(all_products, 20)
    args['products'] = current_page.page(page_number)
    args['projects'] = Category.objects.all()
    args['brands'] = Brands.objects.all()
    args['keywords'] = Keywords.objects.all()
    args['username'] = auth.get_user(request).username
    args['authors'] = Author.objects.all()
    args['form_brands'] = brands_form
    args['form_keywords'] = keywords_form
    return render(request, 'my_magazine/products.html', args)

def product(request, product_id=1):
    comment_form = CommentForm
    brands_form = BrandsForm
    keywords_form = KeywordsForm
    cart_product_form = CartAddProductForm()
    args = {}
    args.update(csrf(request))
    args['product'] = get_object_or_404(Product, id=product_id, product_available=True)
    args['cart_product_form'] = cart_product_form
    args['projects'] = Category.objects.all()
    args['category'] = Category.objects.filter(id=product_id)
    args['comments'] = Comments.objects.filter(comments_product_id=product_id)
    args['n_comments'] = args['comments'] .count()
    args['brands'] = Brands.objects.all()
    args['keywords'] = Keywords.objects.all()
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    args['authors'] = Author.objects.all()
    args['form_brands'] = brands_form
    args['form_keywords'] = keywords_form
    return render(request, 'my_magazine/product.html', args)

def addlike(request, product_id):
    try:
        if product_id in request.COOKIES:
            return_path = request.META.get('HTTP_REFERER', '/')
            return redirect(return_path)
        else:
            product = Product.objects.get(id=product_id)
            product.product_like += 1
            product.save()
            return_path = request.META.get('HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(product_id, "test")
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')

def addcomment(request, product_id):
    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_author = request.user
            comment.comments_product = Product.objects.get(id=product_id)
            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('/products/get/%s/' % product_id)

def product_cat(request, category_id=1):
    brands_form = BrandsForm
    keywords_form = KeywordsForm
    args = {}
    args['projects'] = Category.objects.all()
    args['category'] = Category.objects.get(id=category_id)
    args['products'] = Product.objects.filter(category_id=category_id)
    args['username'] = auth.get_user(request).username
    args['brands'] = Brands.objects.all()
    args['keywords'] = Keywords.objects.all()
    args['form_brands'] = brands_form
    args['form_keywords'] = keywords_form
    branch_categories = args['category'].get_descendants(include_self=True)
    args['category_products'] = Product.objects.filter(category__in=branch_categories).distinct()
    args['authors'] = Author.objects.all()
    return render(request, 'my_magazine/product_cat.html', args)


def keywords(request):
    keywords_form = KeywordsForm
    return_path = request.META.get('HTTP_REFERER', '/')
    args= {}
    args['authors'] = Author.objects.all()
    args['keywords'] = Keywords.objects.all()
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username
    args['form_keywords'] = keywords_form
    args.update(csrf(request))
    if request.POST:
        key = request.POST.get('name', '')
        args['key_name'] = key
        args['products'] = Product.objects.filter(keywords__name__exact=key)
        if args['products']:
            return render(request, 'my_magazine/keywpage.html', args)
        else:
            return render(request, 'my_magazine/keywpage_no.html', args)
    else:
        return render(return_path)

def brands(request):
    brands_form = BrandsForm
    return_path = request.META.get('HTTP_REFERER', '/')
    args= {}
    args['authors'] = Author.objects.all()
    args['brands'] = Brands.objects.all()
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username
    args['form_brands'] = brands_form
    args.update(csrf(request))
    if request.POST:
        key = request.POST.get('name', '')
        args['key_name'] = key
        args['products'] = Product.objects.filter(brands__name__exact=key)
        if args['products']:
            return render(request, 'my_magazine/brandspage.html', args)
        else:
            return render(request, 'my_magazine/brandspage_no.html', args)
    else:
        return render(return_path)

def authors(request, id):
    brands_form = BrandsForm
    keywords_form = KeywordsForm
    args= {}
    args['authors'] = Author.objects.all()
    args['author_s'] = Author.objects.get(id=id)
    args['products'] = Product.objects.filter(author__name__exact=args['author_s'])
    args['projects'] = Category.objects.all()
    args['brands'] = Brands.objects.all()
    args['keywords'] = Keywords.objects.all()
    args['username'] = auth.get_user(request).username
    args['form_brands'] = brands_form
    args['form_keywords'] = keywords_form
    return render(request, 'my_magazine/author_page.html', args)

def home(request):
    brands_form = BrandsForm
    keywords_form = KeywordsForm
    args= {}
    args['products'] = Product.objects.all()
    args['authors'] = Author.objects.all()
    args['projects'] = Category.objects.all()
    args['username'] = auth.get_user(request).username
    args['brands'] = Brands.objects.all()
    args['keywords'] = Keywords.objects.all()
    args['homes'] = Home.objects.all()
    args['form_brands'] = brands_form
    args['form_keywords'] = keywords_form
    return render(request, 'my_magazine/home.html', args)