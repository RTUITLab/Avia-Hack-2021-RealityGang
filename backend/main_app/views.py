from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .serializers import *
from .models import *
from rest_framework import status
import requests
import base64
import json
from .toKML import gen_kml


class ShowCurrentMessageView(APIView):
    """
    Shows current message
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, message_pk):
        message = Message.objects.get(pk=message_pk)
        if message.user == request.user:
            message = MessageSerializer(message, context={'request': request}).data
            return Response(message)
        else:
            return Response(status.HTTP_403_FORBIDDEN)


class TestView(APIView):
    """
    Test
    """

    def quantity_from_json(self, answers: dict) -> dict:
        quantity = {}
        quantity['correct'] = sum(map(('correct').__eq__, answers.values()))
        quantity['incorrect'] = len(answers.values()) - quantity['correct']
        return quantity

    def pretty_json(self, answers: dict) -> dict:
        for key, val in answers.items():
            answers[key] = 'correct' if val == 0 else 'incorrect'
        return answers

    def post(self, request):
        print('start')
        message = Message.objects.create(
            user=request.user,
            description=request.data['description'],
        )
        message.save()

        response = requests.post('http://ml:8000/predict',
                                 json={"file": base64.b64encode(request.FILES['file'].read()).decode('UTF-8')}).json()
        answers = response['answers']
        answers = self.pretty_json(answers)

        with open(f'media/answers/answer_{message.pk}.json', 'w') as outfile:
            outfile.write(json.dumps(answers, indent=4))

        with open(f'media/corrects/correct_{message.pk}.txt', 'wb') as outfile:
            outfile.write(base64.b64decode(response['corrects']))

        with open(f'media/incorrects/incorrect_{message.pk}.txt', 'wb') as outfile:
            outfile.write(base64.b64decode(response['incorrects']))

        goodTracksFile = base64.b64decode(response['corrects']).decode('utf-8')
        badTracksFile = base64.b64decode(response['incorrects']).decode('utf-8')

        with open(f'media/kml/kml_{message.pk}.kml', 'w') as outfile:
            outfile.write(gen_kml(badTracksFile, goodTracksFile))

        message.answer = f'answers/answer_{message.pk}.json'
        message.correct = f'corrects/correct_{message.pk}.txt'
        message.incorrect = f'incorrects/incorrect_{message.pk}.txt'
        message.kml = f'kml/kml_{message.pk}.kml'
        message.save()

        message = MessageSerializer(message, context={'request': request}).data
        print('done')
        return Response({
            'quantity': self.quantity_from_json(answers),
            'message': message
        })


class AddNewMessageView(APIView):
    """
    Adds new message
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print('i got new message')
        files = {
            'file': request.FILES['file']
        }

        message = Message.objects.create(
            user=request.user,
            description=request.data['description'],
        )
        message.save()

        # response = requests.post('http://127.0.0.1:8003/predict', data={}, files=files).json()
        # response = requests.post('http://127.0.0.1:8003/predict', json={"file": base64.b64encode(request.FILES['file'].read()).decode('UTF-8')}).json()
        response = requests.post('http://ml/predict',
                                 json={"file": base64.b64encode(request.FILES['file'].read()).decode('UTF-8')}).json()
        answers = response['answers']

        with open(f'media/answers/answer_{message.pk}.json', 'w') as outfile:
            outfile.write(json.dumps(answers, indent=4))

        with open(f'media/corrects/correct_{message.pk}.txt', 'wb') as outfile:
            outfile.write(base64.b64decode(response['corrects']))

        with open(f'media/incorrects/incorrect_{message.pk}.txt', 'wb') as outfile:
            outfile.write(base64.b64decode(response['incorrects']))

        goodTracksFile = base64.b64decode(response['corrects']).decode('utf-8')
        badTracksFile = base64.b64decode(response['incorrects']).decode('utf-8')

        # print(gen_kml(goodTracksFile, badTracksFile))

        with open(f'media/kml/kml_{message.pk}.kml', 'w') as outfile:
            outfile.write(gen_kml(badTracksFile, goodTracksFile))

        message.answer = f'answers/answer_{message.pk}.json'
        message.correct = f'corrects/correct_{message.pk}.txt'
        message.incorrect = f'incorrects/incorrect_{message.pk}.txt'
        message.kml = f'kml/kml_{message.pk}.kml'
        message.save()

        message = MessageSerializer(message, context={'request': request}).data
        print('i sent new message')
        return Response(message)


class GetMessagesView(APIView):
    """
    Returns messages of current user
    """

    permission_classes = (IsAuthenticated,)

    # def post(self, request):
    #     messages = Message.objects.filter(user=request.user)
    #     messages = MessageSerializer(messages, context={'request': request}, many=True).data
    #
    #     return Response(messages)

    def is_digit(self, find_by_letters):
        if find_by_letters.isdigit():
            return True
        else:
            try:
                float(find_by_letters)
                return True
            except ValueError:
                return False

    def post(self, request):
        find_by_letters = request.data['find_by_letters']
        # find_by_letters = ''

        data = []
        next_page = 1
        previous_page = 1

        if self.is_digit(find_by_letters):
            messages = Message.objects.filter(
                Q(user=request.user),
                Q(pk=find_by_letters) |
                Q(description__icontains=find_by_letters) |
                Q(description__icontains=find_by_letters.capitalize()) |
                Q(description__icontains=find_by_letters.lower()) |
                Q(description__icontains=find_by_letters.upper())
            )
        else:
            messages = Message.objects.filter(
                Q(user=request.user),
                Q(description__icontains=find_by_letters) |
                Q(description__icontains=find_by_letters.capitalize()) |
                Q(description__icontains=find_by_letters.lower()) |
                Q(description__icontains=find_by_letters.upper())
            )

        page = request.GET.get('page', 1)
        paginator = Paginator(messages, 3)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = MessageSerializer(data, context={'request': request}, many=True)

        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({
            'messages': serializer.data,
            'count': paginator.count,
            'numpages': paginator.num_pages,
            'nextlink': '/api/get_messages?page=' + str(next_page),
            'prevlink': '/api/get_messages?page=' + str(previous_page)
        })


class IsAuthenticatedView(APIView):
    """
    Returns true if user is authenticated, else - false
    """

    def get(self, request):
        return Response(request.user.is_authenticated)
