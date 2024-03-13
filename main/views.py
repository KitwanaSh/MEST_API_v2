from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
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

        queryset = Query.objects.all()
        serializer = QuerySerializer(queryset, many=True)

        return generate_200_response(serializer.data)
