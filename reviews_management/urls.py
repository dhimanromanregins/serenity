from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:pk>/review/', views.submit_review, name='submit_review'),
    path('review/<int:pk>/edit/', views.ReviewUpdateView.as_view(), name='review_edit'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
]
