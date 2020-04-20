from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from upload import views


urlpatterns = [
    path("fetch-collection/", views.fetch_collection, name="fetch_collection"),
    path("collections/<int:collection_id>/", views.get_collection, name="get_collection"),
    path("collections/value_counts/<int:collection_id>", views.get_value_counts, name="get_value_counts"),
    path("collections/", views.collections, name="collections"),
    path("admin/", admin.site.urls),
]

handler404 = views.custom404

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
