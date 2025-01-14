import os
from django.http import JsonResponse
from pathlib import Path
from decouple import config, Config, RepositoryEnv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
config = Config(RepositoryEnv(os.path.join(BASE_DIR, ".env")))
IS_PRODUCTION = config('IS_PRODUCTION', default=False, cast=bool)
env_file = '.env.production' if IS_PRODUCTION else '.env.development'
config = Config(RepositoryEnv(os.path.join(BASE_DIR, env_file)))

class FrontendAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("host")
        print(config("WEBSITE_HOSTNAME"))
        allowed_origin = config("WEBSITE_HOSTNAME")
        if request.META.get('HTTP_ORIGIN') != allowed_origin:
            return JsonResponse({'error': 'Unauthorized origin'}, status=403)
        return self.get_response(request)
