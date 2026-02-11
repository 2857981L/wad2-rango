import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from django.template.defaultfilters import slugify
from rango.models import Category

for c in Category.objects.all():
    c.slug = slugify(c.name)
    c.save()
    print(c.name, "->", c.slug)
