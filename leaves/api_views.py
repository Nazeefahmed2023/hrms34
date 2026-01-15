from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from employees.models import Employee, Department
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer, LeaveApplySerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leave_list_api(request):
    if request.user.role == 'EMPLOYEE':
        employee = Employee.objects.get(user=request.user)
        leaves = LeaveRequest.objects.filter(employee=employee).order_by('-created_at')
    else:
        leaves = LeaveRequest.objects.select_related("employee", "employee__department").order_by("-created_at")
    
    serializer = LeaveRequestSerializer(leaves, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_leave_api(request):
    if request.user.role != 'EMPLOYEE':
        return Response({'error': 'Only employees can apply for leave'}, status=status.HTTP_403_FORBIDDEN)
    
    employee = Employee.objects.get(user=request.user)
    serializer = LeaveApplySerializer(data=request.data)
    
    if serializer.is_valid():
        leave = LeaveRequest.objects.create(
            employee=employee,
            leave_type=serializer.validated_data['leave_type'],
            start_date=serializer.validated_data['start_date'],
            end_date=serializer.validated_data['end_date'],
            reason=serializer.validated_data['reason'],
            status='PENDING'
        )
        
        return Response(
            LeaveRequestSerializer(leave).data,
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_leave_list_api(request):
    if request.user.role not in ['ADMIN', 'HR']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    leaves = LeaveRequest.objects.select_related("employee", "employee__department").order_by("-created_at")
    serializer = LeaveRequestSerializer(leaves, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_leave_api(request, pk):
    if request.user.role not in ['ADMIN', 'HR']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    leave = get_object_or_404(LeaveRequest, id=pk)
    leave.status = 'APPROVED'
    leave.approved_by = request.user
    leave.save()
    
    return Response(LeaveRequestSerializer(leave).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_leave_api(request, pk):
    if request.user.role not in ['ADMIN', 'HR']:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    leave = get_object_or_404(LeaveRequest, id=pk)
    leave.status = 'REJECTED'
    leave.approved_by = request.user
    leave.save()
    
    return Response(LeaveRequestSerializer(leave).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_leave_list_api(request):
    user = request.user
    
    try:
        emp = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        return Response({'error': 'Not an employee'}, status=status.HTTP_403_FORBIDDEN)
    
    dept = Department.objects.filter(manager=emp).first()
    if not dept:
        return Response({'error': 'Not a manager'}, status=status.HTTP_403_FORBIDDEN)
    
    leaves = (
        LeaveRequest.objects
        .filter(employee__department=dept)
        .exclude(employee=emp)
        .select_related("employee__user")
        .order_by("-created_at")
    )
    
    serializer = LeaveRequestSerializer(leaves, many=True)
    return Response({
        'department': dept.name,
        'leaves': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manager_approve_leave_api(request, pk):
    user = request.user
    
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        return Response({'error': 'Not an employee'}, status=status.HTTP_403_FORBIDDEN)
    
    managed_department = Department.objects.filter(manager=employee).first()
    if not managed_department:
        return Response({'error': 'Not a manager'}, status=status.HTTP_403_FORBIDDEN)
    
    leave = get_object_or_404(
        LeaveRequest,
        id=pk,
        employee__department=managed_department
    )
    
    leave.status = 'APPROVED'
    leave.approved_by = user
    leave.save()
    
    return Response(LeaveRequestSerializer(leave).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manager_reject_leave_api(request, pk):
    user = request.user
    
    try:
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        return Response({'error': 'Not an employee'}, status=status.HTTP_403_FORBIDDEN)
    
    managed_department = Department.objects.filter(manager=employee).first()
    if not managed_department:
        return Response({'error': 'Not a manager'}, status=status.HTTP_403_FORBIDDEN)
    
    leave = get_object_or_404(
        LeaveRequest,
        id=pk,
        employee__department=managed_department
    )
    
    leave.status = 'REJECTED'
    leave.approved_by = user
    leave.save()
    
    return Response(LeaveRequestSerializer(leave).data)
