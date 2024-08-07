from django.shortcuts import render
from backend.middlewares.login import login_exempt


# Home page
@login_exempt
def index(request):
    return render(request, 'index.html')
