from django.contrib.auth.decorators import login_required
from .models import Category, Brand
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Cart, CartItem, Color
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from .forms import ProductFilterForm
from .models import PromoCode, UserProfile


def index(request):
    categories = ['kedy', 'krossovki', 'basketbolnye_krossovki', 'accessory', 'cloth']
    category_products = {}

    for category_slug in categories:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)[:4]
        category_products[category_slug] = products

    return render(request, 'main/index.html', {'category_products': category_products})


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    promo_codes = PromoCode.objects.filter(user=request.user)

    return render(request, 'main/profile.html', {
        'user': request.user,
        'qr_code_url': user_profile.qr_code.url if user_profile.qr_code else None,
        'promo_codes': promo_codes,
    })


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    form = ProductFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['brand']:
            products = products.filter(brand=form.cleaned_data['brand'])

        if form.cleaned_data['discount']:
            products = products.filter(old_price__isnull=False)

        if form.cleaned_data['min_price']:
            products = products.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
            products = products.filter(price__lte=form.cleaned_data['max_price'])

        if form.cleaned_data['color']:
            products = products.filter(colors=form.cleaned_data['color'])

        if form.cleaned_data['search']:
            products = products.filter(name__icontains=form.cleaned_data['search'])

        sort = form.cleaned_data['sort']
        if sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'newest':
            products = products.order_by('-id')

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'brands': brands,
        'colors': colors,
        'form': form,
    }
    return render(request, 'main/product_list.html', context)


def product_page(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    sizes = product.sizes.all()
    related_products = Product.objects.all()[:4]
    return render(request, 'main/product_page.html', {'product': product, 'sizes': sizes, 'related_products': related_products})


@csrf_exempt
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                cart, created = Cart.objects.get_or_create(session_key=session_key)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Product added to cart',
                'cart_item_count': cart.items.count()
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Internal server error: {e}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            cart_item.delete()

            if request.user.is_authenticated:
                cart = Cart.objects.get(user=request.user)
            else:
                session_key = request.session.session_key
                cart = Cart.objects.get(session_key=session_key)

            return JsonResponse({
                'status': 'success',
                'message': 'Product removed from cart',
                'cart_item_count': cart.items.count()
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Internal server error: {e}'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def cart_detail(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    return render(request, 'main/cart_detail.html', {'cart': cart})


def register(request):
    registration_error = None
    error = None
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'register':
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password((user_form.cleaned_data['password']))
                user.save()
                login(request, user)
                return redirect('/')
    return render(request, 'main/register.html', {'error': error, 'registration_error': registration_error})


def forgot_password(request):
    return render(request, 'main/forgot.html')


def search_product(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(name__icontains=query)
    results = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        }
        for product in products
    ]
    return JsonResponse({'results': results})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error_message': 'Неверное имя пользователя или пароль'})

    return JsonResponse({'success': False, 'error_message': 'Метод не разрешен'})
