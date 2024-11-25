from django.urls import path
from . import views
urlpatterns = [
    path('recommend/', views.RecommenderView.as_view(), name = 'Recommender')
]