from django.urls import path, include
from .views import CourseViewSet, EnrollView, ReviewView, LeaveCourseView, RateTutorView, AdminAddStudent, TutorEnrollPermView, TutorEnrollView, SeeStudentsOnCourse, MyCoursesView, MyCreatedCoursesView
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'course', CourseViewSet)
router.register(r'tutor_admin/', TutorEnrollPermView)

urlpatterns = [
    path('', include(router.urls)),
    path('enroll/<int:pk>',EnrollView.as_view()),
    path('leave_course/<int:pk>', LeaveCourseView.as_view()),
    path('review/<int:pk>',ReviewView.as_view()),
    path('rate_tutor/<int:pk>', RateTutorView.as_view()),
    path('add_student/<int:pk>/<int:id>',AdminAddStudent.as_view()),
    path('tutor_add_student/',TutorEnrollView.as_view()),
    path('students_on_course/',SeeStudentsOnCourse.as_view()),
    path('my_courses/', MyCoursesView.as_view()),
    path('created_courses/', MyCreatedCoursesView.as_view()),
]


