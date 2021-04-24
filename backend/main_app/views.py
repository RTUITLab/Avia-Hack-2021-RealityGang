from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .serializers import *
from .models import *


class AddNewMessageView(APIView):
    """
    Adds new message
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        message = Message.objects.create(
            user=request.user,
            description=request.data['description']
        )
        message.save()
        message = MessageSerializer(message, context={'request': request}).data
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
