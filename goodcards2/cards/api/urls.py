from django.urls import path
from cards.api.views import CardListView, CardDetailView

urlpatterns = [
    path('api/card-list', CardListView.as_view(), name='cards'),
    path('api/<int:pk>', CardDetailView.as_view(), name='card-details')
]
