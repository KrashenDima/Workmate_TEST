import json
from typing import Dict

def write_payout_report_to_json(report: Dict[str, Dict], filename: str) -> None:
    with open(f"{filename}.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)


def write_payout_report_to_txt(report: Dict[str, Dict], filename: str) -> None:
    
    # Find the longest name for formatting
    all_names = [
        emp['name'] 
        for dept in report.values() 
        for emp in dept['employees']
    ]
    max_name = max(len(name) for name in all_names) if all_names else 0

    with open(f'{filename}.txt', 'w', encoding='utf-8') as file:
         # Write header
        file.write(f"{'name':>20}{'hours':>{max_name+6}}  rate  payout\n")

        # Write department sections
        for dept, dept_data in report.items():
            file.write(f"{dept}\n")

            for emp in dept_data['employees']:
                file.write(f"--------------- {emp['name']}"
                           f"{emp['hours']:>{max_name-len(emp['name'])+8}}"
                           f"    {emp['rate']}    ${emp['payout']}\n")
                
            file.write(f"{dept_data['total_hours']:>{24+max_name}}"
                       f"          ${dept_data['total_payout']}\n")