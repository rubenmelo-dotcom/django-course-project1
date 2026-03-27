from django.shortcuts import render
from .forms import RegisterForm


def register_view(request):
    if request.POST:
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'authors/pages/register_view.html',
        context,
    )

