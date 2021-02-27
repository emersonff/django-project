from django.db import models
from django.conf import settings
from django.shortcuts import reverse

from django.conf import settings
import markdown
import re
# Create your models here.


class BigCategory(models.Model):
    """Big catergories in the navigation bar"""
    name = models.CharField("Big category", max_length = 50) # name of category with Big category as vrebose name
    slug = models.SlugField(unique = True) # generating unique url for each article. A slug is a short label for something
    description = models.TextField(max_length = 240, default = settings.SITE_DESCRIPTION, help_text = "description") # d in seo
    keywords = models.TextField(max_length = 240, default = settings.SITE_KEYWORDS, help_text = "keywords") # k in seo

    class Meta: # using class Meta to add extra parameters to a class
        verbose_name = "big category" # if isn`t given, Django will use a munged version of class name which is 'big category'
        verbose_name_plural = "big categories" # varbose_name + 's' if is not given

    def __str__(self):
        return self.name




class Category(models.Model):
    """Categories under big categories"""
    name = models.CharField("Article category", max_length = 50)
    slug = models.SlugField(unique = True)
    description = models.TextField(max_length = 240, default = settings.SITE_DESCRIPTION, help_text = "description") # d in seo
    bigcategory = models.ForeignKey(BigCategory, verbose_name = "Big category", null = True, on_delete = models.SET_NULL)# ManyToOne 

    class Meta:
        #verbose_name = "category"
        #verbose_name_plural = "categories"
        ordering = ["name"] # set default ordering. case sensitive

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", kwargs = {"slug" : self.slug, "bigslug" : self.bigcategory.slug})

    def get_article_list(self):
        return Article.objects.filter(category = self) # return a QuerySet containing articles in this category
    

class Tag(models.Model):
    """Tag for article"""
    name = models.CharField("Tag", max_length = 30)
    slug = models.SlugField(unique = True)
    description = models.TextField(max_length = 240, default = settings.SITE_DESCRIPTION, help_text = "description") # d in seo

    class Meta:
        #verbose_name = "tag"
        #verbose_name_plural = "tags"
        ordering = ["id"]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:tag", kwargs = {"tag" : self.name})
    
    def get_article_list(self):
        return Article.objects.filter(tags = self) 


class Keyword(models.Model):
    """KeyWord. K in SEO(Search Engine Optimization"""
    name = models.CharField("Keyword", max_length = 30)

    class Meta:
        #verbose_name = "keyword"
        #verbose_name_plural = "keywords"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    IMG_LINK = "/static/images/summary.jpg"
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = "author", on_delete = models.CASCADE)# delete articles when the user is deleted
    title = models.CharField(max_length = 100)
    summary = models.TextField(max_length = 240, default = "This is the summary of your article.")
    body = models.TextField()
    img_link = models.CharField(default = IMG_LINK, max_length = 255)# verbose name is 'img link'
    create_date = models.DateTimeField(auto_now_add = True)# auto_now_add : Automatically set the field to now when the object is first created.
    update_date = models.DateTimeField(auto_now = True) # auto_now :Automatically set the field to now every time the object is saved.
    views = models.IntegerField(default = 0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(unique = True)# unique identifier for article
    category = models.ForeignKey(Category, null = True, on_delete = models.SET_NULL)#set to NULL when the category is deleted
    tags = models.ManyToManyField(Tag) #ManyToMany
    keywords = models.ManyToManyField(Keyword, help_text = "K in SEO. Usually an article should have 3 to 4 keywords.")

    class Meta:
        ordering = ["-create_date"]# - indicates descending order

    def __str__(self):
        return self.title[:20]

    def get_absolute_url(self):
        return reverse("blog:article", kwargs = {"slug" : self.slug})
    
    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions = [
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields = ["views"]) # save field views

    def get_pre(self):
        return Article.objects.filter(id__lt = self.id).order_by("-id").first()
    
    def get_next(self):
        return Article.objects.filter(id__gt = self.id).order_by("id").first()

class Notice(models.Model):
    """Public Notice"""
    text = models.TextField(null = True) # If null = True, Django will store empty values as NULL in database
    is_active = models.BooleanField(default = False)
    add_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.id


class Carousel(models.Model):
    """"""
    number = models.IntegerField(help_text = "Number determines the playing order")
    title = models.CharField(max_length = 100, blank = True, null = True, help_text = "Title can be NULL")
    content = models.CharField(max_length = 100)
    img_url = models.CharField(max_length = 200)
    url = models.CharField(max_length = 200, default = "#", help_text = "Hyperlink for image jump. #: no jumping.")

    class Meta:
        ordering = ["number", "-id"]

    def __str__(self):
        return self.content[:25]


class FriendLink(models.Model):
    """"""
    name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 100, blank = True)
    link = models.URLField()
    logo = models.URLField(blank = True)
    create_date = models.DateTimeField(auto_now_add = True)
    is_active = models.BooleanField(default = True)
    is_show = models.BooleanField(default = False)

    class Meta:
        ordering = ["create_date"]
