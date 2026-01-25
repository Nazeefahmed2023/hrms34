from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

from employees.models import Employee, Department, EmployeeProfile
from leaves.models import LeaveRequest
from attendance.models import Attendance
from django.utils import timezone
from django.db.models import Exists, OuterRef


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    user = request.user
    role = user.role
    
    context = {
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
        'pending_leaves': LeaveRequest.objects.filter(status='PENDING').count(),
    }
    
    # Check if user is a manager
    try:
        emp = Employee.objects.get(user=user)
        dept = Department.objects.filter(manager=emp).first()
        
        if dept:
            from employees.serializers import EmployeeSerializer, EmployeeProfileSerializer

            profile, _ = EmployeeProfile.objects.get_or_create(user=emp.user)
            context['employee'] = EmployeeSerializer(emp).data
            context['profile'] = EmployeeProfileSerializer(profile, context={'request': request}).data
            context['profile_pending'] = not profile.verified
            context['managed_department'] = dept.name
            
            today = timezone.localdate()
            today_attendance = Attendance.objects.filter(
                user=OuterRef('user'),
                date=today,
                check_in__isnull=False
            )
            
            team = (
                Employee.objects.filter(department=dept)
                .select_related("user", "designation")
                .annotate(is_present=Exists(today_attendance))
            )
            
            team_data = []
            present_count = 0
            absent_count = 0
            
            for member in team:
                member_data = EmployeeSerializer(member).data
                member_data['is_present'] = member.is_present
                team_data.append(member_data)
                
                if member.is_present:
                    present_count += 1
                else:
                    absent_count += 1
            
            context['team'] = team_data
            context['present_count'] = present_count
            context['absent_count'] = absent_count
            context['total_team'] = len(team_data)
            context['role'] = 'MANAGER'
            
            return Response(context)
    
    except Employee.DoesNotExist:
        pass
    
    # Employee dashboard
    if role == "EMPLOYEE":
        from employees.serializers import EmployeeSerializer, EmployeeProfileSerializer
        
        emp = Employee.objects.get(user=user)
        profile, _ = EmployeeProfile.objects.get_or_create(user=emp.user)
        
        context['employee'] = EmployeeSerializer(emp).data
        context['profile'] = EmployeeProfileSerializer(profile, context={'request': request}).data
        context['profile_pending'] = not profile.verified
        context['role'] = 'EMPLOYEE'
        
        return Response(context)
    
    # Admin dashboard
    if role == "ADMIN":
        from employees.serializers import EmployeeSerializer
        from leaves.serializers import LeaveRequestSerializer
        
        leaves = LeaveRequest.objects.select_related("employee").order_by("-created_at")[:10]
        employees = Employee.objects.select_related("user", "designation")
        
        context['leaves'] = LeaveRequestSerializer(leaves, many=True).data
        context['employees'] = EmployeeSerializer(employees, many=True).data
        context['role'] = 'ADMIN'
        
        return Response(context)
    
    # HR dashboard
    if role == "HR":
        from employees.serializers import EmployeeSerializer
        from leaves.serializers import LeaveRequestSerializer
        
        context['pending_profiles_count'] = EmployeeProfile.objects.filter(
            verified=False,
            user__role="EMPLOYEE"
        ).count()
        
        leaves = LeaveRequest.objects.select_related("employee").order_by("-created_at")[:10]
        employees = Employee.objects.select_related("user", "designation")
        
        context['leaves'] = LeaveRequestSerializer(leaves, many=True).data
        context['employees'] = EmployeeSerializer(employees, many=True).data
        context['role'] = 'HR'
        
        return Response(context)
    
    return Response(context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats_api(request):
    data = (
        Department.objects
        .annotate(count=Count('employee'))
        .values('name', 'count')
    )
    return Response(list(data))
