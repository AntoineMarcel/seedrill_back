
from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('', include('emails.urls')),
    path('authentification/', include('authentification.urls')),
    path('integration/', include('integration.urls')),
    path('docs/', include_docs_urls(title='Sidrill API')),
    path('admin/', admin.site.urls),
]
