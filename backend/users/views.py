from rest_framework import generics, permissions
from .models import CustomUser
from backend.main_app.models import Comments
from .serializers import CustomUserSerializer
from backend.main_app.serializers import CommentSerializer


class CustomUserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



