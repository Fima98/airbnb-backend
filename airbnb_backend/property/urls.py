from django.urls import path  # type: ignore

from . import api


urlpatterns = [
    path('', api.properties_list, name='properties_list'),
    path('create/', api.create_property, name='create_property'),
    path('<uuid:pk>/', api.properties_detail, name='properties_detail'),
    path('<uuid:pk>/reserve/', api.reserve_property, name='reserve_property'),
    path('<uuid:pk>/reservations/', api.properties_reservations,
         name='properties_reservations'),
    path('<uuid:pk>/favorite/', api.toggle_favorite, name='toggle_favorite'),
]
