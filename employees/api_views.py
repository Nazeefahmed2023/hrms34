from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from accounts.models import User
from .models import Employee, Department, Designation, EmployeeProfile
from .serializers import (
    EmployeeSerializer, DepartmentSerializer, DesignationSerializer,
    EmployeeProfileSerializer, EmployeeCreateSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_list_api(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    employees = Employee.objects.select_related("user", "department", "designation")
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_employee_api(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = EmployeeCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Create user
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
            email=serializer.validated_data.get('email', ''),
            role='EMPLOYEE'
        )
        
        # Create employee
        employee = Employee.objects.create(
            user=user,
            department=serializer.validated_data['department'],
            designation=serializer.validated_data['designation'],
            date_of_joining=serializer.validated_data['date_of_joining'],
            basic_salary=serializer.validated_data['basic_salary']
        )
        
        # Create employee profile
        EmployeeProfile.objects.create(employee=user)
        
        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_detail_api(request, pk):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Update employee details
        if 'department' in request.data:
            employee.department_id = request.data['department']
        if 'designation' in request.data:
            employee.designation_id = request.data['designation']
        if 'basic_salary' in request.data:
            employee.basic_salary = request.data['basic_salary']
        if 'date_of_joining' in request.data:
            employee.date_of_joining = request.data['date_of_joining']
        
        employee.save()
        return Response(EmployeeSerializer(employee).data)
    
    elif request.method == 'DELETE':
        employee.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def departments_api(request):
    departments = Department.objects.prefetch_related("employee_set", "manager")
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_department_manager_api(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    department_id = request.data.get('department_id')
    manager_id = request.data.get('manager_id')
    
    department = get_object_or_404(Department, id=department_id)
    
    if manager_id:
        manager = get_object_or_404(Employee, id=manager_id)
        department.manager = manager
    else:
        department.manager = None
    
    department.save()
    return Response(DepartmentSerializer(department).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def designations_api(request):
    designations = Designation.objects.all()
    serializer = DesignationSerializer(designations, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def employee_profile_api(request):
    user = request.user
    profile, _ = EmployeeProfile.objects.get_or_create(employee=user)
    
    if request.method == 'GET':
        serializer = EmployeeProfileSerializer(profile, context={'request': request})
        
        # Include employee record if exists
        try:
            emp_record = Employee.objects.get(user=user)
            data = serializer.data
            data['employee_record'] = EmployeeSerializer(emp_record).data
            return Response(data)
        except Employee.DoesNotExist:
            return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = EmployeeProfileSerializer(
            profile, data=request.data, partial=True, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            # Reset verification on update
            profile.verified = False
            profile.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_profile_api(request):
    emp_id = request.GET.get('emp')
    user = request.user
    role = getattr(user, 'role', None)
    
    logged_in_emp = None
    if role in ["MANAGER", "EMPLOYEE"]:
        try:
            logged_in_emp = Employee.objects.get(user=user)
        except Employee.DoesNotExist:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    if not emp_id:
        if not logged_in_emp:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        target = logged_in_emp
    else:
        target = get_object_or_404(Employee, employee_id=emp_id)
        
        if role in ["ADMIN", "HR"]:
            pass
        elif role == "MANAGER":
            if not logged_in_emp or target.department_id != logged_in_emp.department_id:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        else:
            if not logged_in_emp or target.user_id != user.id:
                return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    profile, _ = EmployeeProfile.objects.get_or_create(employee=target.user)
    
    return Response({
        'employee': EmployeeSerializer(target).data,
        'profile': EmployeeProfileSerializer(profile, context={'request': request}).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_profiles_api(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    pending = EmployeeProfile.objects.filter(
        verified=False,
        employee__role="EMPLOYEE"
    )
    serializer = EmployeeProfileSerializer(pending, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_profile_api(request, profile_id):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    profile = get_object_or_404(EmployeeProfile, id=profile_id)
    profile.verified = True
    profile.save()
    return Response({'message': 'Profile approved successfully'})
