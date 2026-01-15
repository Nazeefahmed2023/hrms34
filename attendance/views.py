from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Attendance
from datetime import date

@login_required
def attendance_page(request):
    today = timezone.localdate()
    record = Attendance.objects.filter(user=request.user, date=today).first()

    return render(request, 'attendance/mark.html', {
        'record': record,
        'today': today,
    })


@login_required
def check_in(request):
    today = timezone.localdate()
    record, created = Attendance.objects.get_or_create(user=request.user, date=today)

    # Prevent double check-in
    if record.check_in:
        return redirect('attendance:page')

    record.check_in = timezone.now()
    record.save()

    return redirect('attendance:page')


@login_required
def check_out(request):
    today = timezone.localdate()

    try:
        record = Attendance.objects.get(user=request.user, date=today)
    except Attendance.DoesNotExist:
        return redirect('attendance:page')

    # Prevent double check-out
    if record.check_out:
        return redirect('attendance:page')

    record.check_out = timezone.now()
    record.save()

    return redirect('attendance:page')


@login_required
def monthly(request):
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

    total_hours = sum([a.total_hours for a in attendance])

    return render(request, 'attendance/monthly.html', {
        'attendance': attendance,
        'month': month,
        'year': year,
        'total_hours': total_hours,
    })


@login_required
def manager_team_attendance(request):
    from employees.models import Employee, Department  # avoid circular import

    user = request.user

    try:
        emp = Employee.objects.get(user=user)
        dept = Department.objects.filter(manager=emp).first()
        if not dept:
            return redirect('/dashboard/')
    except Employee.DoesNotExist:
        return redirect('/dashboard/')

    today = timezone.localdate()

    team = Employee.objects.filter(department=dept).select_related("user")
    team_attendance = Attendance.objects.filter(date=today)

    present_ids = team_attendance.values_list("user_id", flat=True)
    present = [m for m in team if m.user.id in present_ids]
    absent = [m for m in team if m.user.id not in present_ids]

    return render(request, 'attendance/manager_team.html', {
        "dept": dept,
        "present": present,
        "absent": absent,
        "today": today,
    })
