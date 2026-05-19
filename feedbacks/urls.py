from django.urls import path
from .views import add_feedback, view_feedbacks ,delete_feedback

urlpatterns = [
    path('add/', add_feedback, name='add_feedback'),
    path('view/', view_feedbacks, name='view_feedbacks'),
     path(
        'delete/<int:pk>/',
        delete_feedback,
        name='delete_feedback'
    ),

]