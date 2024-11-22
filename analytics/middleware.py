from .models import APIRequestLog, CoursePopularity
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve


class AnalyticsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            APIRequestLog.objects.create(
                user=request.user,
                endpoint=resolve(request.path).route,
                method=request.method
            )

        if 'courses' in request.path and request.method == 'GET':
            from courses.models import Course
            try:
                course_id = request.resolver_match.kwargs.get('pk')
                if course_id:
                    course = Course.objects.get(pk=course_id)
                    popularity, created = CoursePopularity.objects.get_or_create(course=course)
                    popularity.request_count += 1
                    popularity.save()
            except Course.DoesNotExist:
                pass