from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    total_hours = serializers.SerializerMethodField()
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'user', 'user_name', 'username', 'date',
            'check_in', 'check_out', 'total_hours'
        ]
    
    def get_total_hours(self, obj):
        return obj.total_hours
