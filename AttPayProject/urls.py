
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('accounts/', include('accounts.urls')),
    path('<path:dummy>/', RedirectView.as_view(url='/notfound')),
]
