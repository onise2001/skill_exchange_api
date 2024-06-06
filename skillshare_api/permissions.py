from rest_framework.permissions import BasePermission


class CanCreateCourse(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == "Tutor" or request.user.role == "Administrator") and request.user.is_authenticated


class CanEditCourse(BasePermission):
    def has_object_permission(self, request, view, obj):        
        return request.user == obj.tutor or request.user.role == "Administrator"
    


class CanDeleteCourse(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.tutor or request.user.role == "Administrator"


class CanEnroll(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.role == "Student" and (request.user.id  not in [student.user.id for student in obj.students.all()]) and obj.available) or request.user.role == "Administrator"
    
class CanReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.id in [student.user.id  for student in obj.students.all()]) or request.user.role == "Administrator"
    

class CanLeaveCourse(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id in [user.id for user in obj.students.all()]
    


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Administrator"

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Student"    
    
class IsTutor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Tutor"

class CanViewAdminAdded(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['Administrator', 'Tutor']
    


class CanViewCourseStudents(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == "Administrator" or request.user == obj.tutor
    

