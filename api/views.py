from api.serializers import *
from api.models import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Case, When
from .models import *




# AdminRegister **
class AdminRegister(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['username'] = request.POST['email']
        request.POST._mutable = mutable
        serializer = UserSerializer(data=request.data)
        validate = serializer.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors})

        user = User.objects.create_user(name=request.POST['name'], phone_number=request.POST['phone_number'], username=request.POST['email'],
                                        email=request.POST['email'], password=request.POST['password'])
        user.is_active = True
        user.is_admin = True
        user.is_gmail_authenticated = True
        user.save()

        fields = ('id', 'username', 'email', 'phone_number', 'name')
        data = UserSerializer(user, many=False, fields=fields)
        response = {
            'success': 'True',
            'status': 200,
            'message': 'User created successfully',
            'data': data.data,
        }

        return Response(response)


# adminLogin **
class adminLogin(APIView):
    permission_classes = [AllowAny]

    class Validation(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):

        validation = self.Validation(data=request.data)
        validate = validation.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": validation.errors})

        user = User.objects.filter(is_admin=True,
            email=request.POST['email'], is_gmail_authenticated=True).first()

        if user:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = request.POST['password']
            request.POST._mutable = mutable
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User logged in successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)
        else:
            response = {
                'success': 'True',
                'status': 200,
                'message': 'Admin Not found with these credentials',
                
            }
            return Response(response)



# registration and auto login **
class adminRegisterandLogin(APIView):
    permission_classes = [AllowAny]

    class Validation(serializers.Serializer):
        email = serializers.CharField()
        name = serializers.CharField()

    def post(self, request):

        validation = self.Validation(data=request.data)
        validate = validation.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": validation.errors})

        user = User.objects.filter(is_admin=True,
            email=request.POST['email'], is_gmail_authenticated=True).first()

        if user:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = 'captainamerica'
            request.POST._mutable = mutable
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User logged in  successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)
        else:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = 'captainamerica'
            request.POST['username'] = request.POST['email']
            request.POST._mutable = mutable
            serializer = UserSerializer(data=request.data)
            validate = serializer.is_valid()
            if validate is False:
                return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors})

            user = User.objects.create_user(name=request.POST['name'], username=request.POST['email'],
                                            email=request.POST['email'], password='captainamerica')
            user.is_admin = True
            user.is_active = True
            user.is_gmail_authenticated = True
            user.save()

            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User created and logged in  successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)



# authenticated_userr **
class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(items, many=True)
        return Response({'data':serializer.data,'status': 200, "message": "success"})
    
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Staff, Student, Course, User
from .serializers import *


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        students = Student.objects.all()
        staff = Staff.objects.all()
        courses = Course.objects.all()

        student_name = request.query_params.get('student_name')
        course_name = request.query_params.get('course_name')
        staff_name = request.query_params.get('staff_name')

        if student_name:
            students = students.filter(user__name__icontains=student_name)
        if course_name:
            courses = courses.filter(name__icontains=course_name)
        if staff_name:
            staff = staff.filter(user__name__icontains=staff_name)

        students_serializer = StudentSerializer(students, many=True)
        staff_serializer = StaffSerializer(staff, many=True)
        courses_serializer = CourseSerializer(courses, many=True)

        return Response({
            'students': students_serializer.data,
            'staff': staff_serializer.data,
            'courses': courses_serializer.data,
        })


class manageStaff(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        staff = Staff.objects.all()
        serializer = StaffManageSerializer(staff, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffManageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            staff = Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StaffManageSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            staff = Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class manageStudents(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentManageSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentManageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            students = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudentManageSerializer(students, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            students = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        students.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class manageCourse(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseManageSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseManageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            courses = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseManageSerializer(courses, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            courses = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        courses.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    




# staffRegister **
class StaffRegister(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['username'] = request.POST['email']
        request.POST._mutable = mutable
        serializer = UserSerializer(data=request.data)
        validate = serializer.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors})

        user = User.objects.create_user(name=request.POST['name'], phone_number=request.POST['phone_number'], username=request.POST['email'],
                                        email=request.POST['email'], password=request.POST['password'])
        user.is_active = True
        user.is_staff = True
        user.is_gmail_authenticated = True
        user.save()

        fields = ('id', 'username', 'email', 'phone_number', 'name')
        data = UserSerializer(user, many=False, fields=fields)
        response = {
            'success': 'True',
            'status': 200,
            'message': 'User created successfully',
            'data': data.data,
        }

        return Response(response)


# staffLogin **
class staffLogin(APIView):
    permission_classes = [AllowAny]

    class Validation(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):

        validation = self.Validation(data=request.data)
        validate = validation.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": validation.errors})

        user = User.objects.filter(is_staff=True,
            email=request.POST['email'], is_gmail_authenticated=True).first()

        if user:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = request.POST['password']
            request.POST._mutable = mutable
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User logged in successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)
        else:
            response = {
                'success': 'True',
                'status': 200,
                'message': 'Admin Not found with these credentials',
                
            }
            return Response(response)


class TeacherStudentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  
        students = Student.objects.filter(course__teacher=user) 

        student_name = request.query_params.get('student_name')
        course_name = request.query_params.get('course_name')

        if student_name:
            students = students.filter(user__name__icontains=student_name)
        if course_name:
            students = students.filter(course__name__icontains=course_name)

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)





# studentRegister **
class StudentRegister(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['username'] = request.POST['email']
        request.POST._mutable = mutable
        serializer = UserSerializer(data=request.data)
        validate = serializer.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors})

        user = User.objects.create_user(name=request.POST['name'], phone_number=request.POST['phone_number'], username=request.POST['email'],
                                        email=request.POST['email'], password=request.POST['password'])
        user.is_active = True
        user.is_student = True
        user.is_gmail_authenticated = True
        user.save()

        fields = ('id', 'username', 'email', 'phone_number', 'name')
        data = UserSerializer(user, many=False, fields=fields)
        response = {
            'success': 'True',
            'status': 200,
            'message': 'User created successfully',
            'data': data.data,
        }

        return Response(response)


# studentLogin **
class StudentLogin(APIView):
    permission_classes = [AllowAny]

    class Validation(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):

        validation = self.Validation(data=request.data)
        validate = validation.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": validation.errors})

        user = User.objects.filter(is_student=True,
            email=request.POST['email'], is_gmail_authenticated=True).first()

        if user:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = request.POST['password']
            request.POST._mutable = mutable
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User logged in successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)
        else:
            response = {
                'success': 'True',
                'status': 200,
                'message': 'Admin Not found with these credentials',
                
            }
            return Response(response)



class studentCourse(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  
        student = Student.objects.get(user=user)

        courses = Course.objects.filter(students=student)
        courses_serializer = CourseSerializer(courses, many=True)

        student_serializer = StudentSerializer(student)

        return Response({
            'courses': courses_serializer.data,
            'student': student_serializer.data
        })