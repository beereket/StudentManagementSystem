from django.urls import path
from .views import UserAnalyticsView, CoursePopularityView

urlpatterns = [
    path('user-analytics/', UserAnalyticsView.as_view(), name='user-analytics'),
    path('course-popularity/', CoursePopularityView.as_view(), name='course-popularity'),
]