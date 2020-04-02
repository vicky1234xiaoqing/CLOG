from django.shortcuts import render
 
def hello(request):
    context          = {}
    context['hello'] = 'Hello World!'
    return render(request, 'login.html', context)