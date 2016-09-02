from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # url(r'^about/$', views.about, name='about'),

    url(r'^add_category/$', views.add_category, name='add_category'),

    url(r'^category/(?P<category_slug>[\w\-]+)/$', views.category, name='category'),

    url(r'^category/(?P<category_slug>[\w\-]+)/add_food/$', views.add_food, name='add_food'),

    url(r'^register/$', views.register, name='register'),

    url(r'^login/$', views.signin, name='login'),


    url(r'^restricted/', views.restricted, name='restricted'),

    url(r'^logout/$', views.signout, name='logout'),

    url(r'^search/$', views.search, name='search'),

    url(r'^like_category/$', views.like_category, name='like_category'),


]

# /kitchen/category/<category_name_url>/add_food/
