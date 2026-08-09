from django.urls import path
from .views import StudentListCreate, StudentDetail


urlpatterns = [
    path("students/", StudentListCreate.as_view(), name="student-list-create"),
    path("students/<int:roll_no>/", StudentDetail.as_view(), name="student-detail"),


    # path("students_list/", student_list),
    # path("create_student/", create_student),
]
