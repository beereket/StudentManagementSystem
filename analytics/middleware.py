from .models import APIRequestLog, CoursePopularity
from courses.models import Course
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve


class AnalyticsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                APIRequestLog.objects.create(
                    user=request.user,
                    endpoint=resolve(request.path).route,
                    method=request.method
                )
            except Exception as e:
                print(f"Error logging API request: {e}")

        if 'courses' in request.path and request.method == 'GET':
            try:
                if request.resolver_match and request.resolver_match.kwargs:
                    course_id = request.resolver_match.kwargs.get('pk')
                    if course_id:
                        course = Course.objects.get(pk=course_id)
                        popularity, _ = CoursePopularity.objects.get_or_create(course=course)
                        popularity.request_count += 1
                        popularity.save()
            except Course.DoesNotExist:
                print(f"Course with ID {course_id} does not exist.")
            except Exception as e:
                print(f"Error updating course popularity: {e}")
