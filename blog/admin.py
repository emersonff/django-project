from django.contrib import admin
from .models import BigCategory, Category, Tag, Keyword, Article, Notice, Carousel, FriendLink
# Register your models here.
admin.site.site_header = "Blog Administration"
admin.site.site_title = "Blog Admin"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = "create_date" # the change list page will include a date-based drilldown navigation by that field.
    exclude = ("views",) # exclude views from the form
    list_display = ("id", "title", "author", "create_date", "update_date")
    list_display_links = ("title", ) # field title should be linked to the change page for an object
    list_filter = ("create_date", "category")# activate filter in the right side bar
    list_per_page = 50
    filter_horizontal = ("tags", "keywords")

    def get_queryset(self, request):
        """Qverride get_queryset method. Show articles owned by the logged-in user."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author = request.user)




@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "slug")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "slug")

@admin.register(BigCategory)
class BigCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "slug")

@admin.register(Carousel)
class Carousel(admin.ModelAdmin):
    list_display = ("number", "title", "content", "img_url", "url")
    
@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "id")

@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    date_hierarchy = "create_date"
    list_display = ('name', 'description', 'link', 'create_date', 'is_active', 'is_show')
    list_filter = ("is_active", "is_show")
