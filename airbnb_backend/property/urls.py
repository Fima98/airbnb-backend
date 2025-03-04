from django.urls import path  # type: ignore

from . import api


urlpatterns = [
    path('', api.properies_list, name='properties_list'),
    path('create/', api.create_property, name='create_property'),
]
