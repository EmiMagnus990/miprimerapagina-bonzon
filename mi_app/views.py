from django.shortcuts import render

# Create your views here.
def index(request):
    context = {"mensaje": "Bienvenido a mi primer app"}
    return render(request, "mi_app/index.html", context)