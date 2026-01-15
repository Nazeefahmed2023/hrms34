from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from calendar import monthrange
from django.db.models import Sum, F, ExpressionWrapper, IntegerField
# from xhtml2pdf import pisa  # Not needed for React frontend
from decimal import Decimal
from datetime import date, timedelta

import csv
from django.http import HttpResponse
from calendar import month_name

from .models import Payroll
from employees.models import Employee
from attendance.models import Attendance
from leaves.models import LeaveRequest
from accounts.decorators import role_required  # Ensure this exists


# ------------------ PAYROLL LIST ------------------ #
@login_required
def payroll_list(request):
    mode = request.GET.get("mode")

    # 🔥 HR wants to generate payroll
    if request.user.role in ["ADMIN", "HR"] and mode == "generate":
        employees = Employee.objects.select_related("user", "designation")
        return render(request, "payroll/generate_table.html", {"employees": employees})

    qs = Payroll.objects.select_related("employee", "employee__user")

    # Employee sees only their own payroll
    if request.user.role == "EMPLOYEE":
        qs = qs.filter(employee__user=request.user)

    # Filters
    month = request.GET.get("month")
    year = request.GET.get("year")

    if month:
        qs = qs.filter(month=int(month))
    if year:
        qs = qs.filter(year=int(year))

    # CSV export (Admin/HR only)
    if request.GET.get("export") == "csv" and request.user.role in ["ADMIN", "HR"]:
        response = HttpResponse(content_type='text/csv')
        csv_month = month_name[int(month)] if month else "All"
        csv_year = year if year else "All"

        filename = f"CoreConnect_Payroll_{csv_year}_{str(month).zfill(2) if month else ''}.csv"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response)
        writer.writerow([
            "Employee ID", "Employee Name", "Month", "Year",
            "Gross Salary", "Total Deductions", "Net Salary"
        ])
        for p in qs:
            writer.writerow([
                p.employee.employee_id,
                p.employee.user.get_full_name(),
                month_name[p.month],
                p.year,
                p.gross_salary,
                p.total_deductions,
                p.net_salary
            ])
        return response

    # final render
    records = qs.order_by("-year", "-month")
    return render(request, "payroll/list.html", {"records": records})



# ------------------ PAYSLIP PDF ------------------ #
@login_required
def payslip_pdf(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)

    # Prevent unauthorized access
    if request.user.role == "EMPLOYEE" and payroll.employee.user != request.user:
        return HttpResponse("Unauthorized", status=403)

    template = get_template("payroll/payslip.html")
    html = template.render({"payroll": payroll})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="payslip_{payroll.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response


# ------------------ GENERATE PAYROLL ------------------ #
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from calendar import monthrange
from django.db.models import Sum, F, ExpressionWrapper, IntegerField

from accounts.decorators import role_required
from employees.models import Employee
from attendance.models import Attendance
from leaves.models import LeaveRequest
from .models import Payroll


@login_required
@role_required(["ADMIN", "HR"])
def generate_payroll(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == "POST":
        # -------- 1. Read and validate month/year -------- #
        try:
            month = int(request.POST.get("month"))
            year = int(request.POST.get("year"))
        except (TypeError, ValueError):
            messages.error(request, "Invalid month or year.")
            return redirect("payroll:list")

        # Prevent duplicate payroll
        if Payroll.objects.filter(employee=employee, month=month, year=year).exists():
            messages.error(request, "Payroll already exists for this employee and month.")
            return redirect("payroll:list")

        # -------- 2. Build month date range -------- #
        days_in_month = monthrange(year, month)[1]
        month_start = date(year, month, 1)
        month_end = date(year, month, days_in_month)

        # -------- 3. Working days = all days except Sat/Sun -------- #
        working_dates = []
        current = month_start
        while current <= month_end:
            # Mon=0 ... Sun=6 → 5=Saturday, 6=Sunday
            if current.weekday() not in (5, 6):
                working_dates.append(current)
            current += timedelta(days=1)

        working_days = len(working_dates)

        # Safety: if for some weird reason there are 0 working days
        if working_days == 0:
            messages.error(request, "No working days found for this month.")
            return redirect("payroll:list")

        # -------- 4. Present days from Attendance -------- #
        present_days = Attendance.objects.filter(
            user=employee.user,
            date__range=(month_start, month_end),
            date__in=working_dates,  # ignore attendance on weekends if any
        ).count()

        # -------- 5. Approved leaves (paid vs LOP) -------- #
        approved_leaves = LeaveRequest.objects.filter(
            employee=employee,
            status="APPROVED",
            end_date__gte=month_start,   # overlap with month
            start_date__lte=month_end,
        )

        paid_leave_days = 0
        lop_days = 0

        for leave in approved_leaves:
            # Overlap of leave with this month
            leave_start = max(leave.start_date, month_start)
            leave_end = min(leave.end_date, month_end)

            current = leave_start
            while current <= leave_end:
                # Skip weekends even if leave spans them (rule A)
                if current.weekday() not in (5, 6):
                    if leave.leave_type in ("CL", "SL", "PL"):
                        paid_leave_days += 1
                    elif leave.leave_type == "LOP":
                        lop_days += 1
                current += timedelta(days=1)

        # -------- 6. Absent days (pure no-show on working day) -------- #
        absent_days = working_days - (present_days + paid_leave_days + lop_days)
        if absent_days < 0:
            # In case of weird overlap or data issues, don't go negative
            absent_days = 0

        # -------- 7. Salary components -------- #
        basic = employee.basic_salary or Decimal("0.00")

        # Earnings
        hra = (basic * Decimal("0.40")).quantize(Decimal("0.01"))
        allowance = (basic * Decimal("0.20")).quantize(Decimal("0.01"))
        gross = (basic + hra + allowance).quantize(Decimal("0.01"))

        # Per-day salary based on working days
        per_day = (gross / Decimal(working_days)).quantize(Decimal("0.01"))

        # LOP deduction (only LOP reduces salary)
        lop_amount = (Decimal(lop_days) * per_day).quantize(Decimal("0.01"))

        # Standard deductions (you can later make these configurable)
        pf = (basic * Decimal("0.12")).quantize(Decimal("0.01"))
        professional_tax = Decimal("200.00")

        total_deductions = (lop_amount + pf + professional_tax).quantize(Decimal("0.01"))
        net = (gross - total_deductions).quantize(Decimal("0.01"))

        # -------- 8. Create Payroll record -------- #
        Payroll.objects.create(
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

        messages.success(request, "Payroll generated successfully!")
        return redirect("payroll:list")

    # GET → show form
    return render(request, "payroll/generate.html", {"employee": employee})
