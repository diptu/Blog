from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.

import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# class PostManager(models.Manager):
#
#
#     def all(self,*args,**kwargs):
#
#         return super(PostManager,self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_file_location(instance,filename):
    return "%s/%s" %(instance.slug , filename)

class Post(models.Model):
    user        =   models.ForeignKey(User , on_delete=models.CASCADE,default=1)
    title       =   models.CharField(max_length=120)
    content     =   models.TextField()
    slug        =   models.SlugField(unique=True)
    image       =   models.FileField(null=True , blank=True ,upload_to = upload_file_location)
    draft       =   models.BooleanField(default=False)
    publish     =   models.DateField(auto_now=False,auto_now_add=False)
    timestamp   =   models.DateTimeField(auto_now=False, auto_now_add=True)
    updated     =   models.DateTimeField(auto_now=True, auto_now_add=False)

    #objects     =   PostManager()

    def __str__(self):
        return self.title
    class Meta:
        ordering    =   ["-timestamp","-updated"]

def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender , instance ,*args , **kwargs):
    if not instance.slug :
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver,sender=Post)
