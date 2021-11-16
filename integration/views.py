from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ParrainSerializer, CreateParrainSerializer
from .models import Parrain, Campaign, Steps

class Banner_API(APIView):
    def get(self, request, campaignID=None, friendCode=None):
        if friendCode and campaignID:
            try:
                item = Parrain.objects.get(friendCode=friendCode)
                if not item.campaign.token == campaignID:
                    return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ParrainSerializer(item)
            item.visits = item.visits + 1
            item.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

class Payment_API(APIView):
    def post(self, request):
        try:
            campaign = Campaign.objects.get(token=request.data['campaignTk'])
            if not campaign.web_site in request.headers["Origin"]:
                return Response({"status": "error", "data": {"origin": request.headers["Origin"], "configured" :campaign.web_site}}, status=status.HTTP_400_BAD_REQUEST)
            parrain = {
                'campaign':campaign.id,
                'firstName': request.data['firstName'],
                'lastName': request.data['lastName'],
                'email': request.data['email'],
                'step': Steps.objects.get(campaign=campaign, order=0).id,
            }
            serializer = CreateParrainSerializer(data=parrain)
            if serializer.is_valid():
                serializer.save()
                if request.data['friendCode']:
                    try:
                        fromUser = Parrain.objects.get(friendCode=request.data['friendCode'])
                        if fromUser.campaign.token == request.data['campaignTk']:
                            fromUser.buy = fromUser.buy + 1
                            fromUser.save()
                    except:
                        pass
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {
                "except" : str(e),
                "data" : request.data
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)