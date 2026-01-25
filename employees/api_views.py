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
    user = request.user
    if user.role in ["ADMIN", "HR"]:
        employees = Employee.objects.select_related("user", "department", "designation")
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    elif user.role == "EMPLOYEE":
        try:
            employee = Employee.objects.select_related("user", "department", "designation").get(user=user)
            serializer = EmployeeSerializer(employee)
            return Response([serializer.data])
        except Employee.DoesNotExist:
            return Response({'error': 'Employee record not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_employee_api(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = EmployeeCreateSerializer(data=request.data)
    try:
        if serializer.is_valid():
            # Check if username already exists
            user = User.objects.filter(username=serializer.validated_data['username']).first()
            if user is None:
                # Create user if not exists
                user = User.objects.create_user(
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password'],
                    first_name=serializer.validated_data.get('first_name', ''),
                    last_name=serializer.validated_data.get('last_name', ''),
                    email=serializer.validated_data.get('email', ''),
                    role='EMPLOYEE'
                )

            # If employee already exists for this user, return it
            employee = getattr(user, 'employee', None)
            if employee is None:
                employee = Employee.objects.create(
                    user=user,
                    department=serializer.validated_data['department'],
                    designation=serializer.validated_data['designation'],
                    date_of_joining=serializer.validated_data['date_of_joining'],
                    basic_salary=serializer.validated_data['basic_salary']
                )
                # Create employee profile with default values for required fields
                EmployeeProfile.objects.create(
                    user=user,
                    phone='',
                    personal_email=user.email or '',
                    address=''
                )

            return Response(
                EmployeeSerializer(employee).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        return Response({'error': str(e), 'trace': traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_detail_api(request, pk):
    user = request.user
    employee = get_object_or_404(Employee, pk=pk)
    # Only ADMIN/HR or the employee themselves can access
    if user.role in ["ADMIN", "HR"] or (user.role == "EMPLOYEE" and employee.user_id == user.id):
        if request.method == 'GET':
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        elif request.method == 'PUT':
            # Only ADMIN/HR can update all fields, employee can update only their own allowed fields (if any)
            if user.role in ["ADMIN", "HR"]:
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
            elif user.role == "EMPLOYEE" and employee.user_id == user.id:
                # Allow employee to update their own department, designation, date_of_joining, basic_salary
                allowed_fields = ["department", "designation", "date_of_joining", "basic_salary"]
                updated = False
                for field in allowed_fields:
                    if field in request.data:
                        if field in ["department", "designation"]:
                            setattr(employee, f"{field}_id", request.data[field])
                        else:
                            setattr(employee, field, request.data[field])
                        updated = True
                if updated:
                    employee.save()
                    return Response(EmployeeSerializer(employee).data)
                else:
                    return Response({'error': 'No valid fields to update.'}, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if user.role in ["ADMIN", "HR"]:
                employee.user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Not allowed to delete employee record.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


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
    profile, _ = EmployeeProfile.objects.get_or_create(user=user)
    
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
    
    profile, _ = EmployeeProfile.objects.get_or_create(user=target.user)
    
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
        user__role="EMPLOYEE"
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
