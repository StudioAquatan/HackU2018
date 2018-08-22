from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404


def index(request):
    template_name = 'poll/index.html'

    return render(request, template_name)
    # return HttpResponse("Hello, world. You're at the polls index.")


def listener(request):
    template_name = 'poll/listener.html'

    return render(request, template_name)


def speaker(request):
    template_name = 'poll/speaker.html'

    understand_vote = Vote.objects.filter(votetype=0)
    have_known_vote = Vote.objects.filter(votetype=1)
    not_understand_vote = Vote.objects.filter(votetype=2)

    context = {
        'understand_vote': understand_vote.len,
        'have_known_vote': have_known_vote.len,
        'not_understand_vote': not_understand_vote.len,
    }

    return render(request, template_name, context)


def speaker_res(request):
    template_name = 'poll/speaker_res.html'

    return render(request, template_name)
