import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # Save the image to the static folder
            image_path = os.path.join(settings.APPS_DIR, 'static', 'images', 'logo.png')
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
