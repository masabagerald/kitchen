import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Apetite.settings")

import django

django.setup()

from kitchenapp.models import Category, Food


def populate():
    cheese_food = [
        {"title": "  cheese burger",
         "origin": "usa"},
        {"title": "  beef burger ",
         "origin": "  canada "},
        {"title": " chicken burger ",
         "title": "  usa "},

    ]

    pizza_food = [
        {"title": "  cheese pizza",
         "origin": "usa"},
        {"title": "  beef pizza ",
         "origin": "  canada "},
        {"title": " vegetable pizza ",
         "title": "  usa "},

    ]

    baked_food = [
        {"title": " muffin cake",
         "origin": "britain"},
        {"title": "  queen cake ",
         "origin": "  britain "},
        {"title": " cinammon cake ",
         "title": "  italy "},

    ]

    cats = {"burger": {"food": cheese_food},
            "pizza": {"food": pizza_food},
            "baked": {"food": baked_food}}

    for cat, cat_data in cats.iteritems():

        c = add_cat(cat)
        for p in cat_data["food"]:
            add_food(c,p["title"],p["origin"])

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


if __name__ == '__main__':
    print ("Starting Rango population script...")
    populate()
