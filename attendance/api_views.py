from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Attendance
from .serializers import AttendanceSerializer
from employees.models import Employee, Department


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_today_api(request):
    today = timezone.localdate()
    record = Attendance.objects.filter(user=request.user, date=today).first()
    
    if record:
        serializer = AttendanceSerializer(record)
        return Response(serializer.data)
    else:
        return Response({'date': str(today), 'check_in': None, 'check_out': None})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_in_api(request):
    today = timezone.localdate()
    record, created = Attendance.objects.get_or_create(user=request.user, date=today)
    
    if record.check_in:
        return Response({'error': 'Already checked in'}, status=status.HTTP_400_BAD_REQUEST)
    
    record.check_in = timezone.now()
    record.save()
    
    serializer = AttendanceSerializer(record)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out_api(request):
    today = timezone.localdate()
    
    try:
        record = Attendance.objects.get(user=request.user, date=today)
    except Attendance.DoesNotExist:
        return Response({'error': 'No check-in found'}, status=status.HTTP_400_BAD_REQUEST)
    
    if record.check_out:
        return Response({'error': 'Already checked out'}, status=status.HTTP_400_BAD_REQUEST)
    
    record.check_out = timezone.now()
    record.save()
    
    serializer = AttendanceSerializer(record)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_attendance_api(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if not month or not year:
        month = timezone.now().month
        year = timezone.now().year
    
    attendance = Attendance.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).order_by('date')
    
    serializer = AttendanceSerializer(attendance, many=True)
    total_hours = sum([a.total_hours for a in attendance])
    
    return Response({
        'attendance': serializer.data,
        'total_hours': total_hours,
        'month': month,
        'year': year
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_team_attendance_api(request):
    user = request.user
    
    try:
        emp = Employee.objects.get(user=user)
        dept = Department.objects.filter(manager=emp).first()
        if not dept:
            return Response({'error': 'Not a manager'}, status=status.HTTP_403_FORBIDDEN)
    except Employee.DoesNotExist:
        return Response({'error': 'Not a manager'}, status=status.HTTP_403_FORBIDDEN)
    
    today = timezone.localdate()
    team = Employee.objects.filter(department=dept).select_related("user")
    team_attendance = Attendance.objects.filter(date=today)
    
    present_ids = team_attendance.values_list("user_id", flat=True)
    
    from employees.serializers import EmployeeSerializer
    
    present = [EmployeeSerializer(m).data for m in team if m.user.id in present_ids]
    absent = [EmployeeSerializer(m).data for m in team if m.user.id not in present_ids]
    
    return Response({
        'department': dept.name,
        'present': present,
        'absent': absent,
        'today': str(today),
        'present_count': len(present),
        'absent_count': len(absent)
    })
