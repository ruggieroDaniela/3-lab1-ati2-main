import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from django.shortcuts import redirect, render
from pathlib import Path


def cambiarNombre(request):
    if request.method == 'POST':
        # Obtener el nuevo nombre del POST
        new_value = request.POST["new-value"]

        BASE_DIR = Path(__file__).resolve().parent.parent
        file_path = os.path.join(BASE_DIR, 'nombre.txt')
        with open(file_path, 'w') as f:
            f.write(new_value)
        
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename="nombre.txt"'
    
    return redirect(request.META['HTTP_REFERER'])
    