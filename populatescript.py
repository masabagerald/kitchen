import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Apetite.settings")

import django

django.setup()

from kitchenapp.models import Category, Food


def populate():
    pizza_cat = add_cat('pizza')

    add_food(cat=pizza_cat,
             title="vegetable",
             origin="canada")

    add_food(cat=pizza_cat,
             title="cheese",
             origin="canada")
    add_food(cat=pizza_cat,
             title="chicken",
             origin="usa")

    bakery_cat = add_cat("bakery")

    add_food(cat=bakery_cat,
             title="muffin cake",
             origin="usa")

    add_food(cat=bakery_cat,
             title="queen cake",
             origin="canada")

    add_food(cat=bakery_cat,
             title="chocolate cake",
             origin="italy")

    burger_cat = add_cat("burger")

    add_food(cat=burger_cat,
             title="cheese ",
             origin="france")

    add_food(cat=burger_cat,
             title="beef",
             origin="sa")

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Food.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))


def add_food(cat, title, origin, views=0):
    p = Food.objects.get_or_create(category=cat, title=title)[0]
    p.origin = origin
    p.views = views
    p.save()
    return p


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c


# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
