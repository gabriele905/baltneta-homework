from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadFileForm

def list(request):
    return render(request, 'list_categories.html', {'object_list': Category.objects.all()})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])

            return HttpResponseRedirect('/categories/')
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})


def handle_uploaded_file(f):
    return
