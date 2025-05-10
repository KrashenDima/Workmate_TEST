from typing import List, Dict


def get_unique_departments(employees: List[Dict]) -> List[str]:
    return list({emp['department'] for emp in employees})


def calculate_employee_payout(employee: Dict) -> Dict:
    """Calculate payout for a single employee."""
    payout = employee['hours_worked'] * employee['rate']
    return {
        'name': employee['name'],
        'hours': employee['hours_worked'],
        'rate': employee['rate'],
        'payout': payout
    }


def generate_department_report(employees: List[Dict]) -> Dict:
    """Generate report for a single department."""
    department_employees = []
    running_hours = 0
    running_payout = 0
    
    for emp in employees:
        emp_info = calculate_employee_payout(emp)
        running_hours += emp['hours_worked']
        running_payout += emp_info['payout']
        
        emp_info.update({
            'total_hours': running_hours,
            'total_payout': running_payout
        })
        department_employees.append(emp_info)
    
    return {
        'employees': department_employees,
        'total_hours': running_hours,
        'total_payout': running_payout
    }


def generate_payout_report(employees: List[Dict]) -> Dict[str, Dict]:
    """Generate complete payout report organized by departments.
    
    Returns:
        Dictionary with department names as keys and department reports as values.
    """
    departments = get_unique_departments(employees)
    report = {}
    
    for dept in departments:
        dept_employees = [emp for emp in employees if emp['department'] == dept]
        report[dept] = generate_department_report(dept_employees)
    
    return report
