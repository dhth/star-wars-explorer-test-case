from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from hello_django import settings as app_settings

from . import io
from .models import Person, PersonCollection


def fetch_collection(request):
    """
    Fetches data from SWAPI people endpoint, and returns metadata
    for newly saved file and database entry
    """
    added_collection = io.fetch_and_save_data_from_endpoint(
        app_settings.swapi_people_endpoint
    )
    if added_collection is None:
        return JsonResponse({"success": False}, status=500)
    return JsonResponse(
        {"success": True, "collection": {"metadata": model_to_dict(added_collection),},}
    )


def collections(request):
    """
    Returns a list of saved collections and their metadata.
    """
    return JsonResponse(
        {
            "collections": list(PersonCollection.objects.order_by("-id").values()),
            "success": True,
        }
    )


def custom404(request, exception=None):
    return JsonResponse(
        {"success": False, "error": "The resource was not found"}, status=404
    )


def collection_from_database(request, collection_id):
    """
    [OPTIONAL]
    Returns entries for a specific collection, read from the
    corresponding database.
    """
    page_num = int(request.GET.get("page_num", 1))

    person_collection = get_object_or_404(PersonCollection, pk=collection_id)
    collection_data_queryset = (
        Person.objects.all()
        .filter(person_collection=person_collection)
        .values()
        .order_by("id")
    )
    paginator = Paginator(collection_data_queryset, 10)
    if page_num > paginator.num_pages:
        return JsonResponse({"success": False, "detail": "page_num exceeded limit"})
    return JsonResponse(
        {
            "success": True,
            "page_num": page_num,
            "collection": {
                "metadata": model_to_dict(person_collection),
                "fields": [f.name for f in Person._meta.get_fields()],
                "data": list(paginator.page(page_num)),
            },
            "total_pages": paginator.num_pages,
        }
    )


def collection_from_file(request, collection_id):
    """
    Returns entries for a specific collection, read from the
    corresponding file.
    """
    page_num = int(request.GET.get("page_num", 1))
    person_collection = get_object_or_404(PersonCollection, pk=collection_id)
    collection_file_name = f"{app_settings.export_dir}/{person_collection.file_name}"
    person_rows = io.get_rows_from_csv_file(collection_file_name, page_num, 10)
    if len(person_rows) > 0:
        return JsonResponse(
            {
                "success": True,
                "page_num": page_num,
                "collection": {
                    "metadata": model_to_dict(person_collection),
                    "fields": app_settings.csv_file_columns,
                    "data": person_rows,
                },
            }
        )
    else:
        return JsonResponse({"success": False, "detail": "page_num exceeded limit"})


def get_collection(request, collection_id):
    """
    Returns entries for a specific collection based on the
    application setting use_database_for_storage.
    """
    if app_settings.use_database_for_storage:
        return collection_from_database(request, collection_id)
    else:
        return collection_from_file(request, collection_id)


def get_value_counts(request, collection_id):
    """
    Returns value counts for a set of fields sent via a query parameter.
    Data read from corresponding file, and transformed using petl.
    """
    fields = request.GET.get("fields", "")
    fields_to_fetch = [field.strip() for field in fields.split(",")]

    person_collection = get_object_or_404(PersonCollection, pk=collection_id)

    collection_file_name = f"{app_settings.export_dir}/{person_collection.file_name}"

    value_counts_data = io.get_value_counts_from_csv_file(
        collection_file_name=collection_file_name, fields_to_fetch=fields_to_fetch
    )
    return JsonResponse(
        {
            "success": True,
            "value_counts": {
                "metadata": model_to_dict(person_collection),
                "fields": [*fields_to_fetch, "count"],
                "data": value_counts_data,
            },
        }
    )
