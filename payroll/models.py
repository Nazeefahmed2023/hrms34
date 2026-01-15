from django.db import models
from employees.models import Employee

class Payroll(models.Model):
    MONTH_CHOICES = [
        (1, "January"), (2, "February"), (3, "March"), (4, "April"),
        (5, "May"), (6, "June"), (7, "July"), (8, "August"),
        (9, "September"), (10, "October"), (11, "November"), (12, "December")
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()

    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    working_days = models.IntegerField(default=30)
    present_days = models.IntegerField(default=0)
    absent_days = models.IntegerField(default=0)
    lop_days = models.IntegerField(default=0)

    lop_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pf = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'month', 'year')

    def __str__(self):
        return f"{self.employee} — {self.month}/{self.year}"
