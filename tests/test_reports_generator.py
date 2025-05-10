import pytest
from typing import List, Dict

from core.reports_generator import (get_unique_departments,
                                    calculate_employee_payout,
                                    generate_department_report,
                                    generate_payout_report)

# Tests for get_unique_departments
def test_get_unique_departments():
    # Test with empty list
    assert get_unique_departments([]) == []
    
    # Test with one department
    employees = [{'department': 'HR'}, {'department': 'HR'}]
    assert get_unique_departments(employees) == ['HR']
    
    # Test with several departments
    employees = [
        {'department': 'HR'},
        {'department': 'IT'},
        {'department': 'HR'},
        {'department': 'Finance'}
    ]
    result = get_unique_departments(employees)
    assert len(result) == 3
    assert set(result) == {'HR', 'IT', 'Finance'}
    
    # Test with different order of departments
    employees = [
        {'department': 'IT'},
        {'department': 'HR'},
        {'department': 'Finance'}
    ]
    assert sorted(get_unique_departments(employees)) == ['Finance', 'HR', 'IT']

# Tests for calculate_employee_payout
def test_calculate_employee_payout():
    # Simple test
    employee = {'name': 'John', 'hours_worked': 40, 'rate': 25}
    expected = {
        'name': 'John',
        'hours': 40,
        'rate': 25,
        'payout': 1000
    }
    assert calculate_employee_payout(employee) == expected
    
    # Test with hours = 0
    employee = {'name': 'Jane', 'hours_worked': 0, 'rate': 30}
    assert calculate_employee_payout(employee)['payout'] == 0
    
    # Test with negative hours (expect incorrect behavior)
    employee = {'name': 'Bob', 'hours_worked': -10, 'rate': 20}
    assert calculate_employee_payout(employee)['payout'] == -200

# Test for generate_department_report
def test_generate_department_report():
    # Test with empty list of employees
    assert generate_department_report([]) == {
        'employees': [],
        'total_hours': 0,
        'total_payout': 0
    }
    
    # Test with one employee
    employees = [{'name': 'John', 'hours_worked': 40, 'rate': 25}]
    result = generate_department_report(employees)
    assert result['total_hours'] == 40
    assert result['total_payout'] == 1000
    assert len(result['employees']) == 1
    assert result['employees'][0]['payout'] == 1000
    assert result['employees'][0]['total_hours'] == 40
    assert result['employees'][0]['total_payout'] == 1000
    
    # Test with several employees
    employees = [
        {'name': 'John', 'hours_worked': 40, 'rate': 25},
        {'name': 'Jane', 'hours_worked': 30, 'rate': 30}
    ]
    result = generate_department_report(employees)
    assert result['total_hours'] == 70
    assert result['total_payout'] == 1900
    assert len(result['employees']) == 2
    assert result['employees'][0]['total_hours'] == 40
    assert result['employees'][0]['total_payout'] == 1000
    assert result['employees'][1]['total_hours'] == 70
    assert result['employees'][1]['total_payout'] == 1900

# Test for generate_payout_report
def test_generate_payout_report():
    # Test with empty list
    assert generate_payout_report([]) == {}
    
    # Test with one department
    employees = [
        {'department': 'HR', 'name': 'John', 'hours_worked': 40, 'rate': 25},
        {'department': 'HR', 'name': 'Jane', 'hours_worked': 30, 'rate': 30}
    ]
    result = generate_payout_report(employees)
    assert 'HR' in result
    assert result['HR']['total_hours'] == 70
    assert result['HR']['total_payout'] == 1900
    assert len(result['HR']['employees']) == 2
    
    # Test with several departments
    employees = [
        {'department': 'HR', 'name': 'John', 'hours_worked': 40, 'rate': 25},
        {'department': 'IT', 'name': 'Mike', 'hours_worked': 35, 'rate': 40},
        {'department': 'HR', 'name': 'Jane', 'hours_worked': 30, 'rate': 30}
    ]
    result = generate_payout_report(employees)
    assert set(result.keys()) == {'HR', 'IT'}
    assert result['HR']['total_hours'] == 70
    assert result['HR']['total_payout'] == 1900
    assert result['IT']['total_hours'] == 35
    assert result['IT']['total_payout'] == 1400
    assert len(result['HR']['employees']) == 2
    assert len(result['IT']['employees']) == 1