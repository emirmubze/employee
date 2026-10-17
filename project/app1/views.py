
from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee


def dashboard(request):
    employees = Employee.objects.all()

    department = request.GET.get('department')

    if department:
        employees = employees.filter(department=department)

    departments = (
        Employee.objects.values_list('department', flat=True)
        .distinct()
        .order_by('department')
    )

    context = {
        'employees': employees,
        'total_employees': Employee.objects.count(),
        'filtered_count': employees.count(),
        'departments': departments,
        'selected_department': department,
    }

    return render(request, 'dashboard.html', context)


def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        salary = request.POST.get('salary')
        joining_date = request.POST.get('joining_date')

        Employee.objects.create(
            name=name,
            email=email,
            department=department,
            salary=salary,
            joining_date=joining_date
        )

        return redirect('dashboard')

    return render(request, 'add_employee.html')


def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.department = request.POST.get('department')
        employee.salary = request.POST.get('salary')
        employee.joining_date = request.POST.get('joining_date')

        employee.save()

        return redirect('dashboard')

    return render(request, 'edit_employee.html', {
        'employee': employee
    })


def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        employee.delete()

    return redirect('dashboard')
