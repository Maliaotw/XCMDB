from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import UserProfile
from common.serializers import UserProfileSerializer


# Create your views here.
class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        s = UserProfileSerializer(self.request.user)
        return Response(s.data)
