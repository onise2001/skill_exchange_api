from django.shortcuts import render
from .models import Course, Review, Enrollment
from .serializers import CourseSerializer, ReviewSerializer, EnrollmentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from .permissions import CanCreateCourse, CanEditCourse, CanDeleteCourse, CanEnroll, CanReview
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


    def destroy(self, request, *args, **kwargs):
        ...

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
    permission_classes = [CanEnroll]

    def post(self,request,id):
        course = Course.objects.get(pk=id)
        if course:
            
            if request.user.id not in [user.id for user in course.students.all()]:
                enrollment = Enrollment.objects.create(user=request.user)
                course.students.add(enrollment)
                course.save()
                course_serializer = CourseSerializer(course)
                return Response(course_serializer.data, status=status.HTTP_200_OK)
            return Response({'Eror': "Already Enrolled"}, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({'Eror': "no such course"}, status=status.HTTP_400_BAD_REQUEST)
 
    

class ReviewView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CanReview]

    def post(self,request, pk):
        course = Course.objects.get(pk=pk)
        review = Review(**request.data)
        review.user = request.user
        review.save()
        course.reviews.add(review)
        course_serializer = CourseSerializer(course)
        return Response(data=course_serializer.data, status= status.HTTP_200_OK)
        






# new_en = Enrollment.objects.create(user=request.user)
# course = self.get_object()

# course.students.add(new_en)
# course.save()