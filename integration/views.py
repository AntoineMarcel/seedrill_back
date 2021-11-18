from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from emails.utils import create_lead
from .serializers import BannerSerializer, CreateParrainSerializer
from emails.models import Sequence, Person
class Banner_API(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, sequenceID=None, friendCode=None):
        if friendCode and sequenceID:
            try:
                person = Person.objects.get(friendCode=friendCode)
                if not str(person.sequence.id) == str(sequenceID):
                    return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = BannerSerializer(person)
            person.visits = person.visits + 1
            person.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

class Payment_API(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, sequenceID=None):
        if sequenceID:
            try:
                sequence = Sequence.objects.get(id=sequenceID)
                if not sequence.web_site in request.headers["Origin"]:
                    return Response({"status": "error", "data": {"origin": request.headers["Origin"], "configured" :sequence.web_site}}, status=status.HTTP_400_BAD_REQUEST)
                data = create_lead(request.data,sequence)
                if (data["status"] == "success"):
                    return Response({"status": "success", "data": data["data"]}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "success", "data": data["data"]}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                data = {
                    "except" : str(e),
                    "data" : request.data
                }
                return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
