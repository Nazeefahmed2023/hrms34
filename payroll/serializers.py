from rest_framework import serializers
from .models import Payroll


class PayrollSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    department_name = serializers.CharField(source='employee.department.name', read_only=True)
    month_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Payroll
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'department_name',
            'month', 'month_name', 'year', 'basic_salary', 'hra', 'allowance',
            'gross_salary', 'working_days', 'present_days', 'absent_days',
            'lop_days', 'lop_amount', 'pf', 'professional_tax',
            'total_deductions', 'net_salary', 'created_at'
        ]
    
    def get_month_name(self, obj):
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return month_names[obj.month - 1] if 1 <= obj.month <= 12 else ""


class PayrollGenerateSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    month = serializers.IntegerField(min_value=1, max_value=12)
    year = serializers.IntegerField(min_value=2000, max_value=2100)
