from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer

FRIENDLY_FALLBACK = "I don’t have that information yet, but I can show you related details 🙂."

class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        session_id = request.data.get("session_id")
        message = request.data.get("message", "").strip()
        context = request.data.get("context", {})
        if not message:
            return Response({"detail": "Message is required."}, status=400)

        if session_id:
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        else:
            session = ChatSession.objects.create(user=request.user, context=context)

        ChatMessage.objects.create(session=session, sender="user", message=message)

        # Minimal prototype response (replace with AI integration later)
        ai_text = FRIENDLY_FALLBACK

        ChatMessage.objects.create(session=session, sender="ai", message=ai_text)
        return Response({
            "session_id": str(session.id),
            "user_message": message,
            "ai_response": ai_text
        })

class HistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user).order_by("-updated_at")
        data = [{"session_id": str(s.id), "messages": s.messages.count(), "last_message_at": s.updated_at.isoformat()} for s in sessions]
        return Response({"sessions": data})

class SessionDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, session_id):
        s = get_object_or_404(ChatSession, id=session_id, user=request.user)
        return Response(ChatSessionSerializer(s).data)

class ContextView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        s = ChatSession.objects.filter(user=request.user).order_by("-updated_at").first()
        if not s:
            return Response({"session_id": None, "user_profile": {
                "budget": request.user.budget,
                "location": request.user.location,
                "interests": request.user.interests,
            }, "last_intent": None, "last_entities": []})
        return Response({
            "session_id": str(s.id),
            "user_profile": {
                "budget": request.user.budget,
                "location": request.user.location,
                "interests": request.user.interests,
            },
            "last_intent": "university_info",
            "last_entities": []
        })
