from django.urls import path, include
from .views import CourseViewSet, EnrollView, ReviewView
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'course', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('enroll/<int:id>',EnrollView.as_view()),
    path('review/<int:pk>',ReviewView.as_view()),
]


