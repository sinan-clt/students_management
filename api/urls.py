from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user_details', views.UserDetails.as_view()),

    # admin
    path('admin_register', views.AdminRegister.as_view()),
    path('admin_login', views.adminLogin.as_view()),
    path('admin_register_and_Login', views.adminRegisterandLogin.as_view()),
    path('admin_dashboard', views.AdminDashboardView.as_view()),
    path('manage_staff', views.manageStaff.as_view()),
    path('manage_student', views.manageStudents.as_view()),
    path('manage_course', views.manageCourse.as_view()),
    
    # staff 
    path('staff_register', views.StaffRegister.as_view()),
    path('staff_login', views.staffLogin.as_view()),
    path('staff_students', views.TeacherStudentsView.as_view()),

    # student 
    path('student_register', views.StudentRegister.as_view()),
    path('student_login', views.StudentLogin.as_view()),
    path('course_student', views.studentCourse.as_view()),
    
    

]