from rest_framework.views import APIView
from rest_framework.response import Response
from .models import APIRequestLog, CoursePopularity
from django.db.models import Count

class UserAnalyticsView(APIView):
    def get(self, request):
        most_active_users = (
            APIRequestLog.objects.values('user__username')
            .annotate(request_count=Count('id'))
            .order_by('-request_count')[:5]
        )
        return Response({
            'most_active_users': most_active_users
        })

class CoursePopularityView(APIView):
    def get(self, request):
        popular_courses = (
            CoursePopularity.objects.values('course__name')
            .annotate(view_count=Count('request_count'))
            .order_by('-view_count')[:5]
        )
        return Response({
            'popular_courses': popular_courses
        })