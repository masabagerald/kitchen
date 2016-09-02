from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    class  Meta:
        verbose_name_plural ='categories'


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return  self.user.username



class Food(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    origin = models.CharField(max_length=128)
    views = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title

