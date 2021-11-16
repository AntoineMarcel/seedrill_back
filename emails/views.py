import datetime

from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EmailModel, Person, Sequence
from .serializers import EmailModelSerializer, PersonSerializer, SequenceSerializer
from .utils import send_mailModel
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.mail import EmailMultiAlternatives


class Sequence_API(APIView):
    """
    get:
    ##<p>Link : /sequence/'sequence_token'</p>
    Return sequence data.
    ####<b>Please pass your unique token to auth the request</b>

    put:
    ##<p>Link : /sequence/'sequence_token'</p>
    Update sequence
    Format :
    <pre><code>{
        "data": {
            "id": "589925a9-74eb-4713-9876-69bd81a2f8e7",
            "senderName": "Antoine Marcel",
            "subjectEmail": "Hi guys",
            "replyEmail": "test@test.fr"
        }
    }</code></pre>
    * id : uuid, the unique id of your sequence that you need to store
    * senderName : models.CharField("Name of the sender", max_length=150)
    * subjectEmail : models.CharField("Subject of emails", max_length=150)
    * replyEmail : models.EmailField("Email for reply-to")
    ####<b>Please pass your unique token to auth the request</b>

    post:
    ##<p>Link : /sequence/</p>
    Create new sequence.<br/>
    Format :
    <pre><code>{  
        "data": {  
            "senderName": "Your name",  
            "subjectEmail": "Hi guys",  
            "replyEmail": "test@test.fr"  
        }  
    }</code></pre>
    * senderName : models.CharField("Name of the sender", max_length=150)
    * subjectEmail : models.CharField("Subject of emails", max_length=150)
    * replyEmail : models.EmailField("Email for reply-to")
    ####<b>Please pass your unique token to auth the request</b>
    """
    def get(self, request):
        if request.user.is_authenticated:
            try:
                sequence = Sequence.objects.get(user=request.user)
                serializer = SequenceSerializer(sequence)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except:
                return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "data":"not auth"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if request.user.is_authenticated:
            try:
                sequence = Sequence.objects.get(user=request.user)
                serializer = SequenceSerializer(sequence, data=request.data["data"])
                if serializer.is_valid():
                    serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except:
                return Response({"status": "error", "data":request.data}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "data":"not auth"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        if request.user.is_authenticated:
            try:
                serializer = SequenceSerializer(data=request.data["data"])
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
                return Response({"status": "error", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"status": "error", "data":request.data}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "data":"not auth"}, status=status.HTTP_400_BAD_REQUEST)

class Person_API(APIView):
    """
    ##<p>Link : /person/'sequence_token'</p>
    get:
    Return a list of all existing leads for a campaign.
    ####<b>Please pass your unique token to auth the request</b>

    post:
    Create new leads for the campaign.
    Format (list of new person):
    <pre><code>{
        "data": [
            {
                "firstName": "Antoine",
                "lastName": "Marcel",
                "email": "antoine@joyger.fr"
            },
            {
                "firstName": "Antoine2",
                "lastName": "Marcel2",
                "email": "antoine2@joyger.fr"
            }
        ]
    }</code></pre>
    * firstName = models.CharField("First name", max_length=50)
    * lastName = models.CharField("Last name", max_length=50)
    * email = models.EmailField() ==> email is unique for a campaign
    ####<b>Please pass your unique token to auth the request</b>
    """
    def get(self, request):
        if request.user.is_authenticated:
            try:
                sequence = Sequence.objects.get(user=request.user)
            except:
                return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = PersonSerializer(Person.objects.filter(sequence=sequence), many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data":"not auth"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        if request.user.is_authenticated:
            try:
                sequence = Sequence.objects.get(user=request.user).id
                step = EmailModel.objects.filter(sequence=sequence).order_by("order").first()
                nextStepDate = now().date() + datetime.timedelta(days=step.days)
                step_id = step.id
                serializer_list = []
                for newPerson in request.data["data"]:
                    newPerson["sequence"] = sequence
                    newPerson["nextStep"] = step_id
                    newPerson["nextStepDate"] = nextStepDate
                    serializer = PersonSerializer(data=newPerson)
                    if not serializer.is_valid():
                        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    serializer_list.append(serializer)
                for serializer in serializer_list:
                    serializer.save()
            except:
                return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "data": "Persons added"}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data":"not auth"}, status=status.HTTP_400_BAD_REQUEST)

class DeletePerson_API(APIView):
    """
    ##<p>Link : /person/'sequence_token'/'person_id'</p>
    delete:
    Delete a lead.
    ####<b>Please pass your unique token to auth the request</b>
    """
    def delete(self, request, token=None, id=None):
        if request.user.is_authenticated and id:
            try:
                sequence = Sequence.objects.get(user=request.user)
                person = Person.objects.get(sequence=sequence.id, id=id)
                person.delete()
            except:
                return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "data": "Person deleted"}, status=status.HTTP_200_OK)
        return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


class Emails_API(APIView):
    """
    ##<p>Link : /emails/'sequence_token'/</p>
    get:
    Get email model list.
    ####<b>Please pass your unique token to auth the request</b>

    post:
    Change email model list.  
    Format (list of email models):
    <pre><code>{
        "data": [
            {
                "id": "a7e24afe-ddde-4f32-bc60-dc29796dddfc",
                "days": 1,
                "model": "Hello {{firstName}}, how are you today ??\\r\\nI wanted to reach you about\\r\\nthat thing :\\r\\n\\r\\n\\r\\ntest"
            },
            {
                "days": 1,
                "model": "Hello {{firstName}}, yoyoyoy\\r\\n\\r\\ntest"
            }
        ]
    }</code></pre>
    <p>The list must contain the entire emails. If one mail don't appear on the list, it will be considered as deleted.<br/>
    The order of emails on the json will be the order of your emails.</p>
    * id = unique uuid, pass it if you want to modify existing model, if not id, model will be created  
    * days = models.PositiveIntegerField("Days before send", default=1, validators=[MinValueValidator(1), MaxValueValidator(30)])  
    * model = models.TextField("Model") => the model of email  
    ####<b>Please pass your unique token to auth the request</b>
    """
    def get(self, request, token=None):
        if request.user.is_authenticated:
            try:
                sequence = Sequence.objects.get(user=request.user)
            except:
                return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = EmailModelSerializer(EmailModel.objects.filter(sequence=sequence), many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status": "error", "data":"not auth"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, token=None):
        if request.user.is_authenticated:
            try:
                serializer_list = []
                id_list = []
                for emailModel in request.data["data"]:
                    emailModel["sequence"] = token
                    if "id" in emailModel:
                        id_list.append(emailModel["id"])
                        serializer = EmailModelSerializer(EmailModel.objects.get(id=emailModel["id"]),data=emailModel)
                    else:
                        serializer = EmailModelSerializer(data=emailModel)
                    serializer_list.append(serializer)
                    if not serializer.is_valid():
                        return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                
                #delete emails that don't appears
                for savedEmail in EmailModel.objects.filter(sequence=token):
                    if str(savedEmail.id) not in id_list:
                        savedEmail.delete()

                #save all email models
                for serializer in serializer_list:
                    serializer.save()

                #update steps
                for idx, serializer in enumerate(serializer_list):
                    serializer.instance.to(idx + 1)

                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except Exception as e:
                data = {
                    "except" : str(e),
                    "data" : request.data
                }
                return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "error", "data":"not auth"}, status=status.HTTP_400_BAD_REQUEST)

class SendEmail_API(APIView):
    schema = None
    permission_classes = (IsAdminUser,)
    def get(self, request):
        try:
            persons_to_send:list[Person] = Person.objects.filter(nextStepDate=now())
            sended_count = persons_to_send.count()       
            for person in persons_to_send:
                send_mailModel(person)
                person.refresh_step()
            return Response({"status": "success", "mail_sended":sended_count}, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "except" : str(e),
                "data" : request.data
            }
            return Response({"status": "error", "data": data}, status=status.HTTP_400_BAD_REQUEST)
