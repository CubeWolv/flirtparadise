from django.shortcuts import render

# Create your views here.
def rules(request):

    return render(request, './pages/rules.html')