from django.shortcuts import render
from .models import Course, Review, Enrollment, TutorEnrollment
from .serializers import CourseSerializer, ReviewSerializer, EnrollmentSerializer, TutorEnrollmentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView
from .permissions import CanCreateCourse, CanEditCourse, CanDeleteCourse, CanEnroll, CanReview, CanLeaveCourse, IsAdmin, CanViewAdminAdded, CanViewCourseStudents, IsStudent, IsTutor
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from decimal import Decimal
from .filters import TutorRatingFilter, ViewStudentsFilter, MyCoursesFilter, CreatedCoursesFilter, CourseStudentsFilter
from users.models import CustomUser
# Create your views here.

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [TutorRatingFilter]


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Enrollment.objects.filter(course=instance).delete()
        Review.objects.filter(course=instance).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
        

    def get_permissions(self):
        if self.action in SAFE_METHODS:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == "create":
            self.permission_classes = [CanCreateCourse]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [CanEditCourse]
        elif self.action == 'destroy':
            self.permission_classes = [CanDeleteCourse]

        return [permission() for permission in self.permission_classes]




class EnrollView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def put(self,request, *args, **kwargs):

        course = self.get_object()
        #if course.available:
        enrollment = Enrollment.objects.create(user=request.user)
        course.students.add(enrollment)
        course.normal_students += 1
        course.current_students += 1
        course.save()
        course_serializer = CourseSerializer(course)
        return Response(course_serializer.data, status=status.HTTP_200_OK)
    
    

    def get_permissions(self):
        permission_classes = [CanEnroll]
        return [permission() for permission in permission_classes]
    
 
    

class ReviewView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def post(self,request, pk):
        course = self.get_object()
        review = Review(**request.data)
        review.user = request.user
        review.save()
        course.reviews.add(review)
        course_serializer = self.serializer_class(course)
        return Response(data=course_serializer.data, status= status.HTTP_200_OK)
        
        
    
    def get_permissions(self):
        self.permission_classes = [CanReview]
        return [permission() for permission in self.permission_classes]
    


class LeaveCourseView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def destroy(self, request,*args, **kwargs):
        course = self.get_object()
        if request.user.id in [student.user.id for student in course.students.all()]:
            student = Enrollment.objects.get(course=course, user=request.user)
            course.current_students -= 1
            if student.admin_added:
                course.admin_added_students -= 1
            else:
                course.normal_students -= 1
            
            serializer = self.serializer_class(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response({'Eror': "You are not enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)
        




class RateTutorView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'


    def put(self, request, *args, **kwargs):
        course = self.get_object()
    
        rating = Decimal(request.data.get('rating'))
        course.tutor.all_ratings += rating
        course.tutor.rated_by += 1
        course.tutor.average_rating =  course.tutor.all_ratings / course.tutor.rated_by
        course.tutor.save() 
        serializer = self.serializer_class(course)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
    def get_permissions(self):
        self.permission_classes = [CanReview]
        return [permission() for permission in self.permission_classes]
    
    


class AdminAddStudent(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'pk'

    def put(self,request,id, *args, **kwargs):
        course = self.get_object()
        student = CustomUser.objects.get(pk=id)
        enrollment = Enrollment.objects.create(user=student, admin_added=True)
        course.students.add(enrollment)
        course.current_students += 1
        course.admin_added_students += 1
        course.save()
        course_serializer = CourseSerializer(course)
        return Response(course_serializer.data, status=status.HTTP_200_OK)
    
    

    def get_permissions(self):
        permission_classes = [IsAdmin, CanEnroll]
        return [permission() for permission in permission_classes]
    


class TutorEnrollPermView(ModelViewSet):
    queryset = TutorEnrollment.objects.all()
    serializer_class = TutorEnrollmentSerializer
    permission_classes = [IsAdmin]
    


class TutorEnrollView(UpdateAPIView):
    queryset = TutorEnrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def put(self,request,*args,**kwargs):
        tutor_enroll = self.queryset.filter(tutor=request.user, student=request.data.get('student'), course=request.data.get('course'))[0]
        if tutor_enroll:
            enrollment = Enrollment.objects.create(user=tutor_enroll.student, admin_added=True)
            tutor_enroll.course.students.add(enrollment)
            tutor_enroll.course.admin_added_students += 1
            tutor_enroll.course.current_students += 1
            tutor_enroll.course.save()
            course_serializer = CourseSerializer(tutor_enroll.course)
            tutor_enroll.delete()
            return Response(course_serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "No Such Permission"}, status=status.HTTP_400_BAD_REQUEST)
    

# class GetAdminAdded(ListAPIView):
#     queryset = Enrollment.objects.filter(admin_added=True)
#     serializer_class = EnrollmentSerializer
#     permission_classes = [CanViewAdminAdded]


class SeeStudentsOnCourse(ListAPIView):
    #queryset = Course.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [CourseStudentsFilter]
    permission_classes = [CanViewCourseStudents]
    #lookup_field = 'pk'
    def get(self, request, *args,**kwargs):

        queryset = self.get_queryset()
        students = self.filter_queryset(queryset)
        serializer = self.serializer_class(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def get_queryset(self):
        course_id = self.request.query_params.get('course')
        course = Course.objects.get(pk=course_id)
        self.check_object_permissions(self.request, course)
        queryset = course.students.all()
        return queryset

    def get_permissions(self):
        permission_classes = [IsAdmin | CanViewCourseStudents]
        return [permission() for permission in permission_classes]
    


class MyCoursesView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsStudent]
    filter_backends = [MyCoursesFilter]


class MyCreatedCoursesView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsTutor]
    filter_backends = [CreatedCoursesFilter]

    