from django.urls import path  # type: ignore

from . import api


urlpatterns = [
    path('', api.properies_list, name='properties_list'),
    path('create/', api.create_property, name='create_property'),
    path('<uuid:pk>/', api.properties_detail, name='properties_detail'),
    path('<uuid:pk>/book/', api.book_property, name='book_property'),
    path('<uuid:pk>/reservations/', api.properties_reservations,
         name='properties_reservations'),

]
