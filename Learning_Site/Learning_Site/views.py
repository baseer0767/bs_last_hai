from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def main(request):
    return render(request,'layout.html')