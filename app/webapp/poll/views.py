from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404


def index(request):
    template_name = 'poll/index.html'

    return render(request, template_name)
    # return HttpResponse("Hello, world. You're at the polls index.")