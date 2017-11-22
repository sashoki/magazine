# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField
import mptt
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Home(models.Model):
    class Meta():
        db_table = 'home'
        verbose_name_plural = 'Статические страници'
        verbose_name = 'Главная страница'
    home_title = models.CharField(null=True, blank=True, max_length=200)
    home_text = HTMLField(null=True, blank=True)
    home_date = models.DateField(null=True, blank=True)
    home_image = models.ImageField(null=True, blank=True, upload_to='image/', verbose_name=u'Изображение')
    video = EmbedVideoField(null=True, blank=True, verbose_name=u'Видео')

    def __unicode__(self):
        return self.home_title

    def bit_home(self):
        if self.home_image:
            return u'<img src="%s" width="70"/>' % self.home_image.url
        else:
            return u'(none)'
    bit_home.short_descriptio = u'Изображение'
    bit_home.allow_tags = True


class Brands(models.Model):
    class Meta():
        db_table = 'brands'
        verbose_name_plural = 'Бренды'
        verbose_name = 'Бренд'

    name = models.CharField(max_length=50, unique=True, verbose_name='Бренды')

    def __unicode__(self):
        return self.name


class Keywords(models.Model):
    class Meta():
        db_table = 'keywords'
        verbose_name_plural = 'Теги'
        verbose_name = 'Теги'

    name = models.CharField(max_length=50, unique=True, verbose_name=u'Поиск по сайту:')

    def __unicode__(self):
        return self.name



class Author(models.Model):
    class Meta():
        db_table = 'author'
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'

    name = models.CharField(max_length=150)
    author_image = models.ImageField(null=True, blank=True, upload_to="img/", verbose_name="Фото автора",  help_text="250x25")

    def __unicode__(self):
        return self.name

    def bit_author(self):
        if self.author_image:
            return u'<img src="%s" width="70"/>' % self.author_image.url
        else:
            return u'(none)'
    bit_author.short_descriptio = u'Изображение'
    bit_author.allow_tags = True

class Category(MPTTModel):
    class Meta():
        db_table = 'category'
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ('tree_id', 'level')

    name = models.CharField(max_length=150, verbose_name = 'Категория')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'РОДИТЕЛЬСКИЙ класс')

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

mptt.register(Category, order_insertion_by=['name'])

'''class Discount(models.Model):
    name = models.CharField(max_length=150, verbose_name='Скидки')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    discount = models.FloatField()

    def __unicode__(self):
        return '{} "{}": {}'.format(self.content_type.name, self.content_object, self.discount)'''



class Product(models.Model):
    class Meta():
        ordering = ['-product_title']
        db_table = 'product'
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    product_title = models.CharField(max_length=200, verbose_name='Название товара')
    product_price = models.CharField(max_length=200, verbose_name='Цена')
    product_img = models.ImageField(null=True, blank=True, upload_to="img/", verbose_name='Изображения',  help_text="350x200")
    product_video = EmbedVideoField(null=True, blank=True, verbose_name=u'Видео')
    product_text = RichTextField(null=True, blank=True, verbose_name='Описание товара')
    author = models.ForeignKey(Author, max_length=150, verbose_name='Имя автор')
    product_like = models.IntegerField(default=0)
    category = TreeForeignKey(Category, related_name='cat', verbose_name='Категория товара')
    brands = models.ForeignKey(Brands, related_name='brands', related_query_name='brands', verbose_name=u'Бренды')
    product_stock = models.PositiveIntegerField(verbose_name="На складе")
    product_available = models.BooleanField(default=True, verbose_name="Доступен")
    product_created = models.DateTimeField(auto_now_add=True)
    product_updated = models.DateTimeField(auto_now=True)
    keywords = models.ManyToManyField(Keywords, related_name='keywords', related_query_name='keyword', verbose_name=u'Теги')
    #discaunt = models.ManyToManyField(Discount, related_query_name='discount', verbose_name=u'Скидки')

    def __unicode__(self):
        return self.product_title

    def __str__(self):
        return self.product_title

    def bit(self):
        if self.product_img:
            return u'<img src="%s" width="70"/>' % self.product_img.url
        else:
            return '(none)'
    bit.short_description = u'Изображение'
    bit.allow_tags = True

class Comments(models.Model):
    class Meta():
        db_table = 'comments'

    comments_text = models.TextField(null=True, blank=True, verbose_name='Текст коментария')
    comments_product= models.ForeignKey(Product)
    comments_date = models.DateField(u'date', auto_now=True)
    comments_author = models.ForeignKey(User)