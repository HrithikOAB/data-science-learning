from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Student
from .serializers import StudentSerializer, CreateStudentSerializer



class StudentListCreate(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    

class StudentDetail(APIView):
    permission_classes = [AllowAny]

    def get(self, request, roll_no):
        student = get_object_or_404(Student, roll_no=roll_no)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, roll_no):
        student = get_object_or_404(Student, roll_no=roll_no)
        serializer = CreateStudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, roll_no):
        student = get_object_or_404(Student, roll_no=roll_no)
        serializer = CreateStudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, roll_no):
        student = get_object_or_404(Student, roll_no=roll_no)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)












# # unsecured api 
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def student_list(request):
#     students = Student.objects.filter(marks__gte=80)
#     serializer = StudentSerializer(students, many=True)

#     return JsonResponse({'students': serializer.data}, safe=False)



# def create_student(request):
#     if request.method == 'POST':
#         data = request.POST
#         new_student_name = data.get('name')
#         new_student_roll_no = data.get('roll_no')
#         new_student_marks = data.get('marks')

#         if Student.objects.filter(roll_no=new_student_roll_no).exists():
#             return JsonResponse({'error': 'Student with this roll number already exists.'}, status=400)
#         if Student.objects.filter(name=new_student_name).exists():
#             return JsonResponse({'error': 'Student with this name already exists.'}, status=400)
        
#         student = Student.objects.create(name=new_student_name, roll_no=new_student_roll_no, marks=new_student_marks)
#         student.save()

#         return JsonResponse({'message': 'Student created successfully.'}, status=201)

#     if request.method == 'GET':
#         students = Student.objects.all()
#         serializer = StudentSerializer(students, many=True)
#         return JsonResponse({'students': serializer.data}, safe=False)