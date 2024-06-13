from django.shortcuts import render


def render_page(request, template_name):
    return render(request, template_name)
