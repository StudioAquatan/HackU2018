from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from . import listener_button


def index(request):
    template_name = 'poll/index.html'

    return render(request, template_name)
    # return HttpResponse("Hello, world. You're at the polls index.")


def listener(request):
    template_name = 'poll/listener.html'

    if request.method == 'POST':
        if 'button_1' in request.POST:
            # ボタン1がクリックされた場合の処理
            button1()
        elif 'button_2' in request.POST:
            # ボタン2がクリックされた場合の処理
            button2()
        elif 'button_3' in request.POST:
            # ボタン2がクリックされた場合の処理
            button3()

    return render(request, template_name)


def speaker(request):
    template_name = 'poll/speaker.html'

    return render(request, template_name)


def speaker_res(request):
    template_name = 'poll/speaker_res.html'

    return render(request, template_name)
