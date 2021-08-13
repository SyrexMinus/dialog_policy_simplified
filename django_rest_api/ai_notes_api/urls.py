from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.NoteView.as_view()),
    path('notes/<int:pk>', views.NoteView.as_view())
]
