from django.shortcuts import render
import os
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

def contact(request):
    return render(request, './pages/contact.html')


def sitemap(request):
  response = render(request, './sitemap.xml')
  response['Content-Type'] = 'application/xml'
  return response

def robots_txt(request):
    # Path to your robots.txt file in the static directory
    robots_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')

    try:
        with open(robots_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type="text/plain")
    except FileNotFoundError:
        return HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")