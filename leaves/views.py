from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from employees.models import Employee, Department
from .models import LeaveRequest
from .forms import LeaveRequestForm
from accounts.decorators import role_required


# =========================
# EMPLOYEE VIEWS
# =========================

@login_required
@role_required(["EMPLOYEE"])
def leave_list(request):
    # current employee -> see only their own leaves
    employee = Employee.objects.get(user=request.user)
    leaves = LeaveRequest.objects.filter(employee=employee).order_by('-created_at')
    return render(request, 'leaves/list.html', {'leaves': leaves})


@login_required
@role_required(["EMPLOYEE"])
def apply_leave(request):
    employee = Employee.objects.get(user=request.user)

    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = employee
            leave.status = "PENDING"
            leave.save()
            messages.success(request, "Leave applied successfully.")
            return redirect('leaves:list')
    else:
        form = LeaveRequestForm()

    return render(request, 'leaves/apply.html', {'form': form})


# =========================
# ADMIN / HR VIEWS
# =========================

@login_required
@role_required(["ADMIN", "HR"])
def admin_leave_list(request):
    leaves = LeaveRequest.objects.select_related("employee", "employee__department").order_by("-created_at")
    return render(request, "leaves/admin_list.html", {"leaves": leaves})


@login_required
@role_required(["ADMIN", "HR"])
def approve_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, id=pk)
    leave.status = "APPROVED"
    leave.approved_by = request.user
    leave.save()
    messages.success(request, "Leave approved successfully.")
    return redirect("leaves:admin_list")


@login_required
@role_required(["ADMIN", "HR"])
def reject_leave(request, pk):
    leave = get_object_or_404(LeaveRequest, id=pk)
    leave.status = "REJECTED"
    leave.approved_by = request.user
    leave.save()
    messages.error(request, "Leave rejected.")
    return redirect("leaves:admin_list")


# =========================
# MANAGER VIEWS
# =========================

@login_required
def manager_leave_list(request):
    """
    Show pending leaves for the manager's own department only.
    """
    # logged-in user must be an Employee
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        raise PermissionDenied

    # find department where this employee is manager
    managed_department = Department.objects.filter(manager=employee).first()
    if managed_department is None:
        # not a manager = no access
        raise PermissionDenied

    # team = employees in this department
    team_members = Employee.objects.filter(department=managed_department)

    # leaves only from this team
    leaves = (
        LeaveRequest.objects
        .select_related("employee", "employee__department")
        .filter(employee__in=team_members)
        .order_by("-created_at")
    )

    return render(request, "leaves/manager_list.html", {
        "leaves": leaves,
        "managed_department": managed_department,
    })


@login_required
def manager_approve_leave(request, pk):
    """
    Manager can approve only leaves of employees in their own department.
    """
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        raise PermissionDenied

    managed_department = Department.objects.filter(manager=employee).first()
    if managed_department is None:
        raise PermissionDenied

    leave = get_object_or_404(
        LeaveRequest,
        id=pk,
        employee__department=managed_department  # security: only own team
    )

    leave.status = "APPROVED"
    leave.approved_by = request.user
    leave.save()
    messages.success(request, "Leave approved successfully.")
    return redirect("leaves:manager_list")


@login_required
def manager_reject_leave(request, pk):
    """
    Manager can reject only leaves of employees in their own department.
    """
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        raise PermissionDenied

    managed_department = Department.objects.filter(manager=employee).first()
    if managed_department is None:
        raise PermissionDenied

    leave = get_object_or_404(
        LeaveRequest,
        id=pk,
        employee__department=managed_department
    )

    leave.status = "REJECTED"
    leave.approved_by = request.user
    leave.save()
    messages.error(request, "Leave rejected.")
    return redirect("leaves:manager_list")
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from employees.models import Employee, Department
from .models import LeaveRequest


@login_required
def manager_leave_list(request):
    user = request.user

    # 1) Get Employee record for this user
    try:
        emp = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        # Not an employee → no manager view
        return redirect('/dashboard/')

    # 2) Check if this employee is a manager of any department
    dept = Department.objects.filter(manager=emp).first()
    if not dept:
        # Not assigned as manager
        return redirect('/dashboard/')

    # 3) Get leave requests of team members in this department (exclude manager himself)
    leaves = (
        LeaveRequest.objects
        .filter(employee__department=dept)
        .exclude(employee=emp)
        .select_related("employee__user")
        .order_by("-created_at")
    )

    return render(request, "leaves/manager_list.html", {
        "department": dept,
        "leaves": leaves,
    })
