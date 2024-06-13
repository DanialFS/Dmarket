from django.shortcuts import render


def wardrobe(request):
    return render(request, 'wardrobe/wardrobe.html')
