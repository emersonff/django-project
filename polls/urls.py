from django.urls import path

from . import views

app_name = "polls" #namespace
urlpatterns = [
    # ex: /polls/5/
    #Using angle brackets “captures” part of the URL and sends it as a keyword argument to the view function
    #The :question_id> part of the string defines the name that will be used to identify the matched pattern,
    #and the <int: part is a converter that determines what patterns should match this part of the URL path.
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
