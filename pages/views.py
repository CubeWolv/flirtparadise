from django.shortcuts import render

# Create your views here.

def contact(request):

    return render(request, './pages/contact.html')


def sitemap(request):
  response = render(request, './sitemap.xml')
  response['Content-Type'] = 'application/xml'
  return response