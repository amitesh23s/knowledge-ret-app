from django.urls import path

from .views import (
    AskAPrompt, AddDocuments
)

urlpatterns = [
    path('ask_prompt', AskAPrompt.as_view()),
    path('upload_doc', AddDocuments.as_view()),
]