from django.urls import path 
from . import views 
urlpatterns = [ 
path("health/", views.health), 
path("auth/register/", views.RegisterView.as_view()), 
path("auth/me/", views.me), 
path("notes/", views.NoteListCreateView.as_view()), 
path("notes/<int:pk>/", views.NoteDetailView.as_view()), 
path("bug-reports/", views.BugReportListCreateView.as_view()), 
path("ai/summarize/", views.summarize), 
path("ai/quiz/", views.generate_quiz), 
] 