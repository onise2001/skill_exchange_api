from rest_framework.filters import BaseFilterBackend
from .models import Enrollment

class TutorRatingFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        
        
        tutor_rating = request.query_params.get('tutor_rating')
        name = request.query_params.get("name")
        available = request.query_params.get('available')

        if tutor_rating:
            queryset = queryset.filter(tutor__average_rating__gte=tutor_rating)

        if name:
            queryset = queryset.filter(name__contains=name)  

        if available:
            queryset = queryset.filter(available=available)
        
        return queryset



class ViewStudentsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        
        status = request.query_params.get('status')
           
        if status:
            if status == "admin_added":
                queryset = queryset.filter(admin_added=True)
            elif status == "regular":
                queryset = queryset.filter(admin_added=False)
            else:
                queryset = []
            
        return queryset
        


class MyCoursesFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(students__user=request.user)
        return queryset
    
class CreatedCoursesFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(tutor=request.user)
        return queryset
    
class CourseStudentsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        status = request.query_params.get('status')
        print(status)
        
        if status:
            if status == "admin_added":
               queryset = queryset.filter(admin_added=True)
            elif status == "regular":
               queryset = queryset.filter(admin_added=False)
            else:
               queryset = [] 
        
        return queryset
        