from django.urls import path
from .import views

urlpatterns = [
    path('<int:id>',views.CommentView.as_view(), name='comments')
]
