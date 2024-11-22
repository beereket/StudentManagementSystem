from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from django.conf import settings
from django.utils import timezone

class APIRequestLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ),
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(using='analytics', *args, **kwargs)

class CoursePopularity(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    request_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.name} - {self.request_count} views"