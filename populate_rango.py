import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def add_page(category, title, url, views=0):
    p = Page.objects.get_or_create(category=category, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, pages=None, likes=0, views=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes = likes
    c.views = views
    c.save()

    if pages:
        for p in pages:
            add_page(c, p['title'], p['url'], p.get('views', 0))

    return c


def populate():
    python_pages = [
        {'title': 'Official Python Tutorial', 'url': 'https://docs.python.org/3/tutorial/', 'views': 128},
        {'title': 'How to Think like a Computer Scientist', 'url': 'http://www.greenteapress.com/thinkpython/', 'views': 64},
        {'title': 'Learn Python in 10 Minutes', 'url': 'http://www.korokithakis.net/tutorials/python/', 'views': 32},
    ]

    django_pages = [
        {'title': 'Official Django Tutorial', 'url': 'https://docs.djangoproject.com/en/2.2/intro/tutorial01/', 'views': 64},
        {'title': 'Django Rocks', 'url': 'http://www.djangorocks.com/', 'views': 32},
        {'title': 'How to Tango with Django', 'url': 'http://www.tangowithdjango.com/', 'views': 16},
    ]

    other_pages = [
        {'title': 'Bottle', 'url': 'http://bottlepy.org/docs/dev/', 'views': 16},
        {'title': 'Flask', 'url': 'http://flask.pocoo.org', 'views': 32},
    ]

    add_cat('Python', pages=python_pages, likes=64, views=128)
    add_cat('Django', pages=django_pages, likes=32, views=64)
    add_cat('Other Frameworks', pages=other_pages, likes=16, views=32)

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c.name} - {p.title}')


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
