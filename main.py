import argparse

from core.csv_reader import read_csv_files
from core.reports_generator import generate_payout_report
from core.reports_writer import write_payout_report_to_json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_files', nargs='+', help='List of csv files')
    parser.add_argument('--report', help='Report name')
    args = parser.parse_args()
    
    
    record = read_csv_files(args.csv_files)
    report = generate_payout_report(record)
    write_payout_report_to_json(report, args.report)

if __name__ == '__main__':
    main()