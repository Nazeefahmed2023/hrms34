from rest_framework import serializers
from .models import LeaveRequest
from employees.models import Employee


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'department_name',
            'leave_type', 'start_date', 'end_date', 'reason', 'status',
            'approved_by', 'approved_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['employee', 'status', 'approved_by']


class LeaveApplySerializer(serializers.Serializer):
    leave_type = serializers.ChoiceField(choices=LeaveRequest.LEAVE_TYPES)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    reason = serializers.CharField()
