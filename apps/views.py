from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from .models import Table, Staff


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = Staff.objects.get(username=username, password=password)
                request.session['waiter_id'] = user.id  # Store in session
                return redirect('tables')  # Redirect to tables page after login
            except Staff.DoesNotExist:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def tables_view(request):
    # Retrieve all tables and the number of clients at each table
    tables = Table.objects.all()
    return render(request, 'tables.html', {'tables': tables})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu, Table


def menu_view(request, table_id):
    # Verify the apps is logged in
    if not request.session.get('waiter_id'):
        return redirect('login')

    table = get_object_or_404(Table, id=table_id)
    menu_items = Menu.objects.all().order_by('category', 'name')

    context = {
        'table': table,
        'menu_items': menu_items
    }
    return render(request, 'menu.html', context)


def add_to_cart(request, table_id, menu_id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        note = request.POST.get('note', '').strip()
        menu_item = get_object_or_404(Menu, id=menu_id)
        cart = request.session.get('cart', {})

        item_key = f"{menu_id}_{note}"

        if item_key in cart:
            cart[item_key]['quantity'] += quantity
        else:
            cart[item_key] = {
                'menu_id': menu_item.id,
                'name': menu_item.name,
                'price': float(menu_item.price),  # Decimal qiymatini float ga o'zgartirdik
                'quantity': quantity,
                'note': note,
            }

        # Stolni occupied qilish
        table = get_object_or_404(Table, id=table_id)
        table.is_occupied = True
        table.save()

        request.session['cart'] = cart
        return redirect('menu', table_id=table_id)



def view_cart(request, table_id):
    cart = request.session.get('cart', {})
    subtotal = 0
    updated_cart = {}

    for key, item in cart.items():
        total = float(item['price']) * int(item['quantity'])
        item['total'] = total
        updated_cart[key] = item
        subtotal += total

    service_charge = subtotal * 0.15
    total_price = subtotal + service_charge

    context = {
        'table_id': table_id,
        'cart': updated_cart,
        'subtotal': subtotal,
        'service_charge': service_charge,
        'total': total_price
    }
    return render(request, 'cart.html', context)


def remove_from_cart(request, table_id, item_key):
    cart = request.session.get('cart', {})
    if item_key in cart:
        del cart[item_key]
    request.session['cart'] = cart
    return redirect('view_cart', table_id=table_id)


from .models import OrderHistory


def place_order(request, table_id):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu', table_id=table_id)

    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    service_charge = round(subtotal * 0.15, 2)
    total = round(subtotal + service_charge, 2)

    order_details = cart  # JSONField avtomatik dictionary qabul qiladi

    OrderHistory.objects.create(
        table_id=table_id,
        order_details=order_details,
        subtotal=subtotal,
        service_charge=service_charge,
        total_price=total
    )

    request.session['cart'] = {}
    return redirect('menu', table_id=table_id)
