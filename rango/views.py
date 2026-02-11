from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm


def visitor_cookie_handler(request):
    visits = int(request.session.get('visits', '1'))
    last_visit = request.session.get('last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit.split('.')[0], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit

    request.session['visits'] = visits


def index(request):
    visitor_cookie_handler(request)

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {
        'categories': category_list,
        'pages': page_list,
        'visits': request.session.get('visits', 1),
    }
    return render(request, 'rango/index.html', context_dict)


def about(request):
    visitor_cookie_handler(request)
    return render(request, 'rango/about.html', {'visits': request.session.get('visits', 1)})


def show_category(request, category_name_slug):
    context_dict = {}
    visitor_cookie_handler(request)

    try:
        category = Category.objects.get(slug=category_name_slug)

        # Increment the category views count
        category.views = category.views + 1
        category.save()

        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    context_dict['visits'] = request.session.get('visits', 1)
    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:index')

    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect('rango:index')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect('rango:show_category', category_name_slug=category_name_slug)

    return render(request, 'rango/add_page.html', {'form': form, 'category': category})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'rango/register.html', {'user_form': user_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('rango:index')
            else:
                return render(request, 'rango/login.html', {'error_message': 'Your Rango account is disabled.'})
        else:
            return render(request, 'rango/login.html', {'error_message': 'Invalid login details supplied.'})

    return render(request, 'rango/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('rango:index')
