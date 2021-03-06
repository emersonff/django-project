from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
# Create your views here.
#web pages and other contents are delivered by views. Each view is represented by a method.
#request is an HttpRequest object
from django.http import HttpResponse, HttpResponseRedirect
from . models import Question, Choice
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list" # specify the name of context variable
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]#__lte means less than or equal to

class  DetailView(generic.DetailView):
    model = Question
    template_name = "polls/details.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"]) #request.POST values are always strings
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, "polls/details.html", {"question" : question, "error_message": "You didn`t select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args = (question_id,)))


# def index(request): 
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     #template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list" : latest_question_list
#     }
#     #return HttpResponse(template.render(context,request))
#     return render(request, "polls/index.html", context)



# def detail(request, question_id):
#     #try:
#     #    question = Question.objects.get(pk = question_id)
#     #except: Question.DoesNot.Exist:
#     #    raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, "polls/details.html", {"question" : question})



# def results(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     return render(request, "polls/results.html", {"question" : question})



