from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import date, timedelta
from calendar import monthrange
from decimal import Decimal

from .models import Payroll
from employees.models import Employee
from attendance.models import Attendance
from leaves.models import LeaveRequest
from .serializers import PayrollSerializer, PayrollGenerateSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payroll_list_api(request):
    qs = Payroll.objects.select_related("employee", "employee__user")
    
    if request.user.role == "EMPLOYEE":
        qs = qs.filter(employee__user=request.user)
    
    month = request.GET.get("month")
    year = request.GET.get("year")
    
    if month:
        qs = qs.filter(month=int(month))
    if year:
        qs = qs.filter(year=int(year))
    
    records = qs.order_by("-year", "-month")
    serializer = PayrollSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payroll_detail_api(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    
    # Prevent unauthorized access
    if request.user.role == "EMPLOYEE" and payroll.employee.user != request.user:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = PayrollSerializer(payroll)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_payroll_api(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = PayrollGenerateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    employee_id = serializer.validated_data['employee_id']
    month = serializer.validated_data['month']
    year = serializer.validated_data['year']
    
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Prevent duplicate payroll
    if Payroll.objects.filter(employee=employee, month=month, year=year).exists():
        return Response(
            {'error': 'Payroll already exists for this employee and month.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Build month date range
    days_in_month = monthrange(year, month)[1]
    month_start = date(year, month, 1)
    month_end = date(year, month, days_in_month)
    
    # Working days = all days except Sat/Sun
    working_dates = []
    current = month_start
    while current <= month_end:
        if current.weekday() not in (5, 6):
            working_dates.append(current)
        current += timedelta(days=1)
    
    working_days = len(working_dates)
    
    if working_days == 0:
        return Response(
            {'error': 'No working days found for this month.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Present days from Attendance
    present_days = Attendance.objects.filter(
        user=employee.user,
        date__range=(month_start, month_end),
        date__in=working_dates,
    ).count()
    
    # Approved leaves (paid vs LOP)
    approved_leaves = LeaveRequest.objects.filter(
        employee=employee,
        status="APPROVED",
        end_date__gte=month_start,
        start_date__lte=month_end,
    )
    
    paid_leave_days = 0
    lop_days = 0
    
    for leave in approved_leaves:
        leave_start = max(leave.start_date, month_start)
        leave_end = min(leave.end_date, month_end)
        
        current = leave_start
        while current <= leave_end:
            if current.weekday() not in (5, 6):
                if leave.leave_type in ("CL", "SL", "PL"):
                    paid_leave_days += 1
                elif leave.leave_type == "LOP":
                    lop_days += 1
            current += timedelta(days=1)
    
    # Absent days
    absent_days = working_days - (present_days + paid_leave_days + lop_days)
    if absent_days < 0:
        absent_days = 0
    
    # Salary components
    basic = employee.basic_salary or Decimal("0.00")
    
    hra = (basic * Decimal("0.40")).quantize(Decimal("0.01"))
    allowance = (basic * Decimal("0.20")).quantize(Decimal("0.01"))
    gross = (basic + hra + allowance).quantize(Decimal("0.01"))
    
    per_day = (gross / Decimal(working_days)).quantize(Decimal("0.01"))
    
    lop_amount = (Decimal(lop_days) * per_day).quantize(Decimal("0.01"))
    
    pf = (basic * Decimal("0.12")).quantize(Decimal("0.01"))
    professional_tax = Decimal("200.00")
    
    total_deductions = (lop_amount + pf + professional_tax).quantize(Decimal("0.01"))
    net = (gross - total_deductions).quantize(Decimal("0.01"))
    
    # Create Payroll record
    payroll = Payroll.objects.create(
        employee=employee,
        month=month,
        year=year,
        basic_salary=basic,
        hra=hra,
        allowance=allowance,
        gross_salary=gross,
        working_days=working_days,
        present_days=present_days,
        absent_days=absent_days,
        lop_days=lop_days,
        lop_amount=lop_amount,
        pf=pf,
        professional_tax=professional_tax,
        total_deductions=total_deductions,
        net_salary=net,
    )
    
    return Response(
        PayrollSerializer(payroll).data,
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employees_for_payroll_api(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    from employees.serializers import EmployeeSerializer
    employees = Employee.objects.select_related("user", "designation")
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)
