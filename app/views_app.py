from django.shortcuts import render



def home(request):
    # exibe a pagina inicial
    return render(request, 'home.html')

    