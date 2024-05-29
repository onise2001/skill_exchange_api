from django.shortcuts import render
from .models import Course, Review, Enrollment
from .serializers import CourseSerializer, ReviewSerializer, EnrollmentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, DestroyAPIView
from .permissions import CanCreateCourse, CanEditCourse, CanDeleteCourse, CanEnroll, CanReview, CanLeaveCourse
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


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




class EnrollView(CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    #permission_classes = [CanEnroll]

    def post(self,request,id):
        self.check_permissions(request)

        course = Course.objects.get(pk=id)
    
        if course:
            
            if request.user.id not in [user.id for user in course.students.all()] and course.current_students < course.max_students:
                enrollment = Enrollment.objects.create(user=request.user)
                course.students.add(enrollment)
                course.current_students += 1
                course.save()
                course_serializer = CourseSerializer(course)
                return Response(course_serializer.data, status=status.HTTP_200_OK)
            return Response({'Eror': "Already Enrolled"}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({'Eror': "no such course"}, status=status.HTTP_400_BAD_REQUEST)
    

    def get_permissions(self):
        self.permission_classes = [CanEnroll]
        return [permission() for permission in self.permission_classes]
    
    def check_permissions(self, request):
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                self.permission_denied(request)
 
    

class ReviewView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    #permission_classes = [CanReview]

    def post(self,request, pk):
        course = Course.objects.get(pk=pk)
        #print(course.students.all())
        self.check_object_permissions(request, course)
        if course:
            review = Review(**request.data)
            review.user = request.user
            review.save()
            course.reviews.add(review)
            course_serializer = CourseSerializer(course)
            return Response(data=course_serializer.data, status= status.HTTP_200_OK)
        
        
        return Response({'Eror': "no such course"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        self.permission_classes = [CanReview]
        return [permission() for permission in self.permission_classes]
    
    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            print("Checking permissions")
            if not permission.has_object_permission(request,self,obj):
                self.permission_denied(request)
   

        





class LeaveCourseView(DestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = CourseSerializer

    def destroy(self, request, pk,*args, **kwargs):
        course = Course.objects.get(pk=pk)
        if course:
            if request.user.id in [student.user.id for student in course.students.all()]:
                Enrollment.objects.filter(course=course, user=request.user).delete()
                serializer = self.serializer_class(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response({'Eror': "You are not enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'Eror': "no such course"}, status=status.HTTP_400_BAD_REQUEST)

