from rest_framework import serializers
from .models import Employee, Department, Designation, EmployeeProfile
from accounts.serializers import UserSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'manager', 'manager_name']
    
    def get_manager_name(self, obj):
        if obj.manager:
            return obj.manager.user.get_full_name() or obj.manager.user.username
        return None


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_name = serializers.CharField(source='designation.name', read_only=True)
    is_manager = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'employee_id', 'department', 'department_name',
            'designation', 'designation_name', 'date_of_joining',
            'basic_salary', 'is_manager'
        ]
    
    def get_is_manager(self, obj):
        return hasattr(obj, 'managing_department') and obj.managing_department is not None


class EmployeeProfileSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='user.get_full_name', read_only=True)
    employee_username = serializers.CharField(source='user.username', read_only=True)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'user', 'employee_name', 'employee_username',
            'photo', 'photo_url', 'phone', 'personal_email', 'address',
            'date_of_birth', 'emergency_contact', 'bank_name',
            'account_number', 'ifsc_code', 'verified',
            'created_at', 'updated_at'
        ]
    
    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
        return None


class EmployeeCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    designation = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all())
    date_of_joining = serializers.DateField()
    basic_salary = serializers.DecimalField(max_digits=10, decimal_places=2)
