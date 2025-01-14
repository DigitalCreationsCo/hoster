from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import views

router = DefaultRouter()

@csrf_exempt
def handle_request(request):
    print("handle projects request")
    print("method "+ request.method)
    if request.method == 'GET':
        viewset = views.ProjectViewSet.as_view({'get': 'list'})
        return viewset(request)
    elif request.method == 'POST':
        return views.upload_project(request)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


# Define URL patterns with the prefix applied
project_urlpatterns = [
    path('', handle_request, name='projects'),
    path('<int:project_id>/', views.delete_project, name='delete_project'),
    path('<int:project_id>/domain/', views.assign_domain, name='assign_domain'),
]

# Apply the prefix to all routes
urlpatterns = [
    path('api/projects/', include((project_urlpatterns, 'projects'))),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
