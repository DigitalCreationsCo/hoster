import mimetypes
from django.forms import ValidationError
from rest_framework.viewsets import ModelViewSet

from . import models
from .serializers import ProjectSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Project
from .storage import StorageService
from django.conf import settings

class ProjectViewSet(ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = ProjectSerializer

@csrf_exempt
def upload_project(request):
    if request.method == 'POST':
        try:
            # Extract POST parameters
            name = request.POST.get('name')
            domain = request.POST.get('domain')
            uploaded_file = request.FILES.get('file')

            name="Project"
            description ="description"
            domain="domain"
            # Validate required fields
            if not name:
                return JsonResponse({'status': 'error', 'message': 'Project name is required'}, status=400)
            if not domain:
                return JsonResponse({'status': 'error', 'message': 'Project domain is required'}, status=400)
            if not uploaded_file:
                return JsonResponse({'status': 'error', 'message': 'File is required'}, status=400)

            # Get the storage backend and attempt file upload
            storage_backend = StorageService.get_storage_backend()
            try:
                ext = mimetypes.guess_extension(uploaded_file.name)
                print(f"ext: {ext}")
                is_zip = ext == ".zip"

                file_url = storage_backend.upload_file(uploaded_file, uploaded_file.name, is_zip)
                print(f"file_url: {file_url}")

            except Exception as e:
                print(f"File upload failed: {e}")
                return JsonResponse({'status': 'error', 'message': 'Failed to upload file'}, status=500)

            # Create project instance
            try:
                project = Project.objects.create(name=name, description=description, file=file_url, domain=domain)
                print("project created")
                print(project)
                
            except ValidationError as ve:
                print(f"Project creation failed: {ve}")
                return JsonResponse({'status': 'error', 'message': 'Invalid project data'}, status=400)
            except Exception as e:
                print(f"Unexpected error during project creation: {e}")
                return JsonResponse({'status': 'error', 'message': 'Failed to create project'}, status=500)

            # Success response
            return JsonResponse({'status': 'success', 'project_id': project.id, 'file_url': file_url})

        except Exception as e:
            # Catch unexpected exceptions
            print(f"Unexpected error in upload_project: {e}")
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred'}, status=500)

    # Handle non-POST requests
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_project(request, project_id):
    if request.method == 'DELETE':
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return JsonResponse({'status': 'success', 'message': 'Project deleted'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def assign_domain(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        domain = request.POST.get('domain')
        project.domain = domain
        project.save()
        return JsonResponse({'status': 'success', 'message': 'Domain assigned'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
