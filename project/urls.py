from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls')),
]
# -- added: route for the weather dashboard --
try:
    # import is tolerant if already present
    from django.urls import path
    from weather.views import dashboard_view
    urlpatterns += [
        path("dashboard/", dashboard_view, name="dashboard"),
    ]
except Exception:
    # falls urlpatterns noch nicht existiert, füge fallback hinzu
    try:
        from django.urls import path
        from weather.views import dashboard_view
        urlpatterns = [
            path("dashboard/", dashboard_view, name="dashboard"),
        ]
    except Exception:
        pass
# -- end added --
