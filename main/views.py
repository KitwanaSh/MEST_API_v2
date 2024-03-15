from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination

from .models import *
from .serializers import *
from datetime import datetime
from API_v2.utils import *


@api_view(['GET'])
def fetch_class_schedules(request):
    queryset = ClassSchedule.objects.all()
    serializer = ClassScheduleSerializer(queryset, many=True)

    return Response({"data": serializer.data}, status.HTTP_200_OK)

@api_view(['POST'])
def create_class_schedule(request):
    title = request.data.get("title")
    description = request.data.get("description")
    start_date_and_time = request.data.get("start_date_and_time")
    end_date_and_time = request.data.get("end_date_and_time")
    cohort_id = request.data.get("cohort_id")
    venue = request.data.get("vanue")
    facilitator_id = request.data.get("facilitator_id")
    is_repeated = request.data.get("is_repeated")
    repeat_frequency = request.data.get("repeat_frequency")
    course_id = request.data.get("course_id")
    meeting_type = request.data.get("meeting_type")


    if not title:
        return Response({"message": "My friend, send me a title"}, status.HTTP_400_BAD_REQUEST)
    
    cohort = None
    facilitator = None
    course = None

    try:
        cohort = Cohort.objects.get(id=cohort_id)
    except Cohort.DoesNotExist:
        return Response({"message": "Body, this cohort does not exist!"}, status.HTTP_400_BAD_REQUEST)
    
    try:
        facilitator = IMUser.objects.get(id=facilitator_id)
    except IMUser.DoesNotExist:
        return Response({"message": "Body, this facilitator does not exist!"}, status.HTTP_400_BAD_REQUEST)
    
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response({"message": "Body, this course does not exist!"}, status.HTTP_400_BAD_REQUEST)
    

    class_schedule = ClassSchedule.objects.create(
        title=title,
        description=description,
        venue=venue,
        is_repeated=is_repeated,
        repeat_frequency=repeat_frequency,
        start_date_and_time=datetime.now(),
        end_date_and_time=datetime.now(),
        facilitator=facilitator,
        cohort=cohort,
        course=course,
        organizer=facilitator
    )

    class_schedule.save()
    serializer = ClassScheduleSerializer(class_schedule, many=False)

    return Response({"message": "Schedule successfully created", "data": serializer.data}, status.HTTP_200_OK)

class QueryModelView(viewsets.ModelViewSet):
    @action(detail=False, methods=["post"])
    def raise_query(self, request):
        title = request.data.get("title")
        description = request.data.get("description", None)
        query_type = request.data.get("query_type", None)
        assignee = None

        # if query_type == "FACILITY":
        #     assignee = IMUser.objects.get(email="lucky@mail.com")

        query = Query.objects.create(
            title = title,
            description = description,
            query_type = query_type,
            submitted_by = request.user,
            author=request.user
        )

        query.save()

        return Response({"message": "Query successfully submitted"})
    
    @action(detail=False, methods=["post"])
    def filter_queries(self, request):
        search_text = request.data.get("search_text")
        status = request.data.get("status")
        paginator = PageNumberPagination()

        queryset = Query.objects.all()
        serializer = QuerySerializer(queryset, many=True)

        return paginator.get_paginated_response(serializer.data)
    
    @action(detail=False, methods=["post"])
    def update_queries(self, request, id):
        status = request.data.get("resolution_status")

        queryset = Query.objects.get(id)
        serializer = QuerySerializer(instance=queryset, data=status)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def my_queries(self, request, id):
        user_type = request.data.get("user_type")

        if user_type == "ADMIN":
            queryset = Query.objects.all()
            serializer = QuerySerializer(queryset, many=True)

        if user_type == "IT":
            queryset = Query.objects.get(id)
            serializer = QuerySerializer(queryset, many=False)

        return Response(serializer.data)

class MeetingModelView(viewsets.ModelViewSet):
    """
        To create a meeting schedule
    """
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def filter_class_schedules(self, request):
        queryset = self.queryset.order_by('start_date_and_time')
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)
