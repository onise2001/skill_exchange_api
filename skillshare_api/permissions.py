from rest_framework.permissions import BasePermission


class CanCreateCourse(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.role == "Tutor" and request.user.is_authenticated


class CanEditCourse(BasePermission):
    def has_object_permission(self, request, view, obj):        
        return request.user == obj.tutor
    


class CanDeleteCourse(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.tutor or request.user.role == "administrator"


class CanEnroll(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Student" and request.user.is_authenticated
    
class CanReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        return request.user.id in [student.user.id  for student in obj.students.all()]
    

class CanLeaveCourse(BasePermission):
    def has_object_permission(self, request, view, obj):
        print([user.id for user in obj.students.all()])
        print(request.user.id)
        return request.user.id in [user.id for user in obj.students.all()]