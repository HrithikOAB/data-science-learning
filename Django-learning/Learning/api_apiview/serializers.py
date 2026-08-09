from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"



class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'email', 'marks']

    def create(self, validated_data):
        if Student.objects.filter(roll_no=validated_data['roll_no']).exists():
            raise serializers.ValidationError("A student with this roll number already exists.")

        if Student.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError("A student with this name already exists.")

    
        return super().create(validated_data)
