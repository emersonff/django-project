from django.contrib import admin
from .models import Question, Choice
# Register your models here.

class ChoiceInline(admin.TabularInline): # SIMILAR TO StackedInline but save screen space
    model = Choice
    extra = 3 #provide enough fields for 3 choices

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {"fields" : ["question_text"]}),
        ("Date information", {"fields" : ["pub_date"], "classes" : ["collapse"]})
    ]   
    inlines = [ChoiceInline] #Choice objects are edited on the Question admin page
    list_display = ("question_text", "pub_date", "was_published_recently")# change the display style in the object list. tuple of field names to display
    list_filter = ["pub_date"] # add a filter sidebar
    search_fields = ['question_text'] #adds a search box at the top of the change list






admin.site.register(Question,QuestionAdmin)
