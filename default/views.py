from django.http import HttpResponse


def index(request):
    return HttpResponse("<meta http-equiv=\"refresh\" content=\"0;url=/control\">")
