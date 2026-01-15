from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from accounts.models import User
from .models import Employee, Department, EmployeeProfile
from .forms import EmployeeCreateForm, EmployeeProfileForm


@login_required
def employee_list(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    employees = Employee.objects.select_related("user", "department", "designation")
    return render(request, "employees/list.html", {"employees": employees})


@login_required
def create_employee(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    if request.method == "POST":
        form = EmployeeCreateForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # 1) Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                role="EMPLOYEE"
            )

       
            # 2) Create employee record
            emp = Employee.objects.create(
                user=user,
                department=form.cleaned_data["department"],
                designation=form.cleaned_data["designation"],
                date_of_joining=form.cleaned_data["date_of_joining"],
                basic_salary=form.cleaned_data["basic_salary"]
            )

            # 3) Automatically create employee profile
            EmployeeProfile.objects.create(employee=user)
    # ✔ correct



            messages.success(request, "Employee created successfully!")
            return redirect("employees:employee_list")

    else:
        form = EmployeeCreateForm()

    return render(request, "employees/create.html", {"form": form})


@login_required
def manage_departments(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    if request.method == "POST":
        dept_id = request.POST.get("department_id")
        manager_id = request.POST.get("manager_id")

        try:
            department = Department.objects.get(id=dept_id)
        except Department.DoesNotExist:
            messages.error(request, "Invalid department selected.")
            return redirect("employees:manage_departments")

        if manager_id:
            try:
                manager = Employee.objects.get(id=manager_id)
            except Employee.DoesNotExist:
                messages.error(request, "Invalid manager selected.")
                return redirect("employees:manage_departments")

            department.manager = manager
        else:
            department.manager = None

        department.save()
        messages.success(request, f"Manager updated for {department.name}.")
        return redirect("employees:manage_departments")

    departments = Department.objects.prefetch_related("employee_set", "manager")
    return render(request, "employees/departments.html", {"departments": departments})


# =============================================
# 🔥 EMPLOYEE PROFILE UPDATE (employee side)
# =============================================
@login_required
def update_profile(request):
    user = request.user
    profile, _ = EmployeeProfile.objects.get_or_create(employee=user)

    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            profile.verified = False  # Every update requires HR re-approval
            profile.save()
            return redirect("/dashboard/")
    else:
        form = EmployeeProfileForm(instance=profile)

    emp_record = Employee.objects.get(user=user)

    return render(request, "employees/update_profile.html", {
        "form": form,
        "emp": emp_record,
        "profile": profile,
    })



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Employee, EmployeeProfile

@login_required
def view_profile(request):
    emp_id = request.GET.get("emp")
    user = request.user
    role = getattr(user, "role", None)

    # Only MANAGER and EMPLOYEE are guaranteed to have an Employee record
    logged_in_emp = None
    if role in ["MANAGER", "EMPLOYEE"]:
        logged_in_emp = get_object_or_404(Employee, user=user)

    # ----------------- TARGET EMPLOYEE -----------------
    if not emp_id:
        # No ?emp → must view own profile
        if not logged_in_emp:
            # HR / ADMIN without Employee record trying to view "own" profile
            raise PermissionDenied
        target = logged_in_emp
    else:
        # We are searching using employee_id (E0001, E0002...)
        target = get_object_or_404(Employee, employee_id=emp_id)

        # ------ ROLE PERMISSIONS ------
        if role in ["ADMIN", "HR"]:
            # Full access
            pass
        elif role == "MANAGER":
            if not logged_in_emp or target.department_id != logged_in_emp.department_id:
                raise PermissionDenied
        else:  # EMPLOYEE
            if not logged_in_emp or target.user_id != user.id:
                raise PermissionDenied

    # Profile model links to USER (employee.user)
    profile, _ = EmployeeProfile.objects.get_or_create(employee=target.user)

    return render(request, "employees/profile_view.html", {
        "emp": target,
        "profile": profile,
    })


# =============================================
# 🔥 HR PROFILE APPROVAL PANEL
# =============================================
@login_required
def pending_profiles(request):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    pending = EmployeeProfile.objects.filter(
    verified=False,
    employee__role="EMPLOYEE"   # 🔥 show employee profiles only
)

    return render(request, "employees/pending_profiles.html", {"profiles": pending})


@login_required
def approve_profile(request, profile_id):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    profile = EmployeeProfile.objects.get(id=profile_id)
    profile.verified = True
    profile.save()
    messages.success(request, "Profile approved successfully.")
    return redirect("/employees/pending-profiles/")



@login_required
def edit_employee(request, emp_id):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    emp = Employee.objects.get(id=emp_id)
    if request.method == "POST":
        form = EmployeeCreateForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated successfully.")
            return redirect("employees:employee_list")
    else:
        form = EmployeeCreateForm(instance=emp)

    return render(request, "employees/edit.html", {"form": form, "emp": emp})




@login_required
def delete_employee(request, emp_id):
    if request.user.role not in ["ADMIN", "HR"]:
        raise PermissionDenied

    emp = Employee.objects.get(id=emp_id)
    emp.user.delete()   # Deletes User + Employee + Profile because FK CASCADE
    messages.success(request, "Employee deleted successfully.")
    return redirect("employees:employee_list")
