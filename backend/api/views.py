import os
import json
from openai import OpenAI
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Note, BugReport
from .serializers import (
    RegisterSerializer, UserSerializer,
    NoteSerializer, BugReportSerializer,
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Auth
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


# Notes
class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)



# Bug Reports
class BugReportListCreateView(generics.ListCreateAPIView):
    serializer_class = BugReportSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return BugReport.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


# AI Features
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def summarize(request):
    text = request.data.get("text", "").strip()
    if not text:
        return Response({"error": "text is required"}, status=400)
    if len(text) > 5000:
        return Response({"error": "text too long (max 5000 chars)"}, status=400)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful study assistant. "
                        "Summarize the provided text in clear bullet points. "
                        "Be concise. Do not add information not in the text."
                    ),
                },
                {"role": "user", "content": f"Summarize this:\n\n{text}"},
            ],
            max_tokens=500,
            temperature=0.3,
        )
        return Response({"summary": response.choices[0].message.content})
    except Exception as e:
        return Response({"error": "AI service error", "detail": str(e)}, status=500)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_quiz(request):
    text = request.data.get("text", "").strip()
    count = int(request.data.get("count", 5))
    if not text:
        return Response({"error": "text is required"}, status=400)
    if len(text) > 5000:
        return Response({"error": "text too long (max 5000 chars)"}, status=400)
    if not (1 <= count <= 10):
        return Response({"error": "count must be 1-10"}, status=400)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"Generate {count} multiple-choice questions from the text. "
                        "Return a JSON array: "
                        '[{"question":"...","options":["A)...","B)...","C)...","D)..."],"answer":"A"}]'
                        " Return ONLY the JSON array."
                    ),
                },
                {"role": "user", "content": f"Generate quiz from:\n\n{text}"},
            ],
            max_tokens=1000,
            temperature=0.4,
        )
        raw = response.choices[0].message.content
        questions = json.loads(raw)
        return Response({"questions": questions})
    except Exception as e:
        return Response({"error": "AI service error", "detail": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok", "project": "Study Buddy"})
 