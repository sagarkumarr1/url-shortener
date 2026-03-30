from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import URL
import random
import string

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def home(request):
    if request.method == 'POST':
        original_url = request.POST.get('url')
        urls = URL.objects.all().order_by('-created_at')
        existing = URL.objects.filter(original_url=original_url).first()
        
        if existing:
            url_obj = existing
        else:
            short_code = generate_short_code()
            url_obj = URL.objects.create(
                original_url=original_url,
                short_code=short_code
            )
        
      
        short_url = f"http://127.0.0.1:8000/{url_obj.short_code}"
        return render(request, 'shortener/home.html', {
            'short_url': short_url,
            'original_url': original_url,
            'urls': urls 
        })
    

    urls = URL.objects.all().order_by('-created_at')
    return render(request, 'shortener/home.html', {'urls': urls})
    

def redirect_url(request, short_code):
    try:
        url_obj = URL.objects.get(short_code=short_code)
        url_obj.click_count += 1
        url_obj.save()
        return redirect(url_obj.original_url)
    except URL.DoesNotExist:
        return HttpResponse("URL not found!", status=404)
