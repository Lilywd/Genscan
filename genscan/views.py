from unicodedata import name
from django.conf import settings
from django.shortcuts import render, redirect
from qrcode import *
import time
from .models import QrCode
from pyzbar.pyzbar import decode
from PIL import Image

def dashboard(request):
    return render(request, 'genscan/dashboard.html')

def generator(request):
    if request.method == 'POST':
        data = request.POST['data']
        img = make(data)
        img_name = 'qr' + str(time.time()) + '.png'
        img.save(settings.MEDIA_ROOT + '/' + img_name)
        return render(request, 'genscan/generator.html', {'img_name': img_name})
    return render(request, 'genscan/generator.html')



def scanner(request):
    if request.method == "POST" and request.FILES['file']:
       context = {}
       qr_image = request.FILES['file']
       context['decoded'] = decode(Image.open(qr_image))[0].data.decode('ascii')       
       return render(request, 'genscan/scanner.html', context)

    return render(request, 'genscan/scanner.html')