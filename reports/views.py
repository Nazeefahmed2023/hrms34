import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
# from xhtml2pdf import pisa  # Not needed for React frontend
from django.contrib.auth.decorators import login_required
from employees.models import Employee

@login_required
def report_dashboard(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return HttpResponse("Unauthorized", status=403)
    return render(request, "reports/report_dashboard.html")


@login_required
def employees_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Department', 'Designation', 'DOJ', 'Basic Salary'])
    for emp in Employee.objects.select_related('user', 'department', 'designation'):
        writer.writerow([
            emp.user.get_full_name() or emp.user.username,
            emp.department.name if emp.department else '',
            emp.designation.name if emp.designation else '',
            emp.date_of_joining,
            emp.basic_salary,
        ])
    return response

@login_required
def employees_pdf(request):
    employees = Employee.objects.select_related('user', 'department', 'designation')
    template = get_template('reports/employees_pdf.html')
    html = template.render({'employees': employees})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="employees.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('PDF error')
    return response








from attendance.models import Attendance
from django.db.models import Q
from calendar import month_name
from django.template.loader import get_template


@login_required
def attendance_report(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return HttpResponse("Unauthorized", status=403)

    month = request.GET.get("month")
    year = request.GET.get("year")

    qs = Attendance.objects.select_related("user")

    if month:
        qs = qs.filter(date__month=int(month))
    if year:
        qs = qs.filter(date__year=int(year))

    return render(request, "reports/attendance_report.html", {
        "records": qs,
        "month": month,
        "year": year,
    })


@login_required
def attendance_csv(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return HttpResponse("Unauthorized", status=403)

    month = request.GET.get("month")
    year = request.GET.get("year")

    qs = Attendance.objects.select_related("user")
    if month:
        qs = qs.filter(date__month=int(month))
    if year:
        qs = qs.filter(date__year=int(year))

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="Attendance_Report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Employee", "Date", "Check-in", "Check-out", "Total Hours"])

    for row in qs:
        writer.writerow([
            row.user.get_full_name(),
            row.date,
            row.check_in,
            row.check_out,
            row.total_hours,
        ])
    return response


@login_required
def attendance_pdf(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return HttpResponse("Unauthorized", status=403)

    month = request.GET.get("month")
    year = request.GET.get("year")

    qs = Attendance.objects.select_related("user")
    if month:
        qs = qs.filter(date__month=int(month))
    if year:
        qs = qs.filter(date__year=int(year))

    template = get_template("reports/attendance_pdf.html")
    html = template.render({"records": qs})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Attendance_Report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    return response if not pisa_status.err else HttpResponse("PDF error")


from payroll.models import Payroll
from decimal import Decimal

@login_required
def payroll_report(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return HttpResponse("Unauthorized", status=403)

    month = request.GET.get("month")
    year = request.GET.get("year")

    qs = Payroll.objects.select_related("employee", "employee__user")
    if month:
        qs = qs.filter(month=int(month))
    if year:
        qs = qs.filter(year=int(year))

    return render(request, "reports/payroll_report.html", {
        "records": qs,
        "month": month,
        "year": year,
    })


@login_required
def payroll_pdf(request):
    if request.user.role not in ["ADMIN", "HR"]:
        return HttpResponse("Unauthorized", status=403)

    month = request.GET.get("month")
    year = request.GET.get("year")

    qs = Payroll.objects.select_related("employee", "employee__user")
    if month:
        qs = qs.filter(month=int(month))
    if year:
        qs = qs.filter(year=int(year))

    template = get_template("reports/payroll_pdf.html")
    html = template.render({"records": qs, "month": month, "year": year})
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Payroll_Report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response if not pisa_status.err else HttpResponse("PDF error")
