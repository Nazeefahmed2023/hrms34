from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

from employees.models import Employee, Department, EmployeeProfile
from leaves.models import LeaveRequest
from employees.models import EmployeeProfile
from django.utils import timezone
from django.db.models import Exists, OuterRef
from attendance.models import Attendance


def dashboard_context():
    return {
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
        'pending_leaves': LeaveRequest.objects.filter(status='PENDING').count(),
    }


@login_required
def dashboard(request):
    user = request.user
    role = user.role
    context = dashboard_context()

    # ==========================================
    # 1️⃣ MANAGER
    # ==========================================
    try:
        emp = Employee.objects.get(user=user)
        dept = Department.objects.filter(manager=emp).first()

        if dept:
            profile, _ = EmployeeProfile.objects.get_or_create(employee=request.user)    






            context["emp"] = emp
            context["profile"] = profile
            context["profile_pending"] = not profile.verified
            context["managed_department"] = dept

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

            context["team"] = team
            context["present_count"] = team.filter(is_present=True).count()
            context["absent_count"] = team.filter(is_present=False).count()
            context["total_team"] = team.count()

            return render(request, "dashboard/manager_dashboard.html", context)

    except Employee.DoesNotExist:
        pass

    # ==========================================
    # 2️⃣ EMPLOYEE
    # ==========================================
    if role == "EMPLOYEE":
        emp = Employee.objects.get(user=user)
        profile, _ = EmployeeProfile.objects.get_or_create(employee=emp.user)


        context["emp"] = emp
        context["profile"] = profile
        context["profile_pending"] = not profile.verified

        if not profile.verified:
            messages.warning(request, "Profile pending HR approval.")

        return render(request, "dashboard/employee_dashboard.html", context)

    # ==========================================
    # 3️⃣ ADMIN
    # ==========================================
    if role == "ADMIN":
        context["leaves"] = LeaveRequest.objects.select_related("employee").order_by("-created_at")[:10]
        context["employees"] = Employee.objects.select_related("user", "designation")
        return render(request, "dashboard/admin_dashboard.html", context)

    # ==========================================
    # 4️⃣ HR
    # ==========================================
    if role == "HR":
        context["pending_profiles_count"] = EmployeeProfile.objects.filter(
            verified=False,
            employee__role="EMPLOYEE"
        ).count()
        context["leaves"] = LeaveRequest.objects.select_related("employee").order_by("-created_at")[:10]
        context["employees"] = Employee.objects.select_related("user", "designation")
        context["show_payroll"] = request.GET.get("show_payroll") == "true"
        return render(request, "dashboard/hr_dashboard.html", context)

    return redirect("/")

@login_required
def stats_api(request):
    data = (
        Department.objects
        .annotate(count=Count('employee'))
        .values('name', 'count')
    )
    from django.http import JsonResponse
    return JsonResponse(list(data), safe=False)
