from typing import List, Dict


def normalize_column_name(column_name: str) -> str:
    """Normalize column name to standard 'rate'."""
    PAYMENT_COLUMNS = {'rate', 'hourly_rate', 'salary'}
    return 'rate' if column_name.strip().lower() in PAYMENT_COLUMNS else column_name


def edit_column_names_list(columns: List[str]) -> List[str]:
    """Standardize column names in the list."""
    return [normalize_column_name(column) for column in columns]


def read_csv_file(file_path: str) -> List[Dict]:
    """Read and parse CSV file into a list of dictionaries."""
    records = []

    try:
        with open(file_path, encoding='utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]
            
            if not lines:
                return records

            column_names = edit_column_names_list(lines[0].split(','))
            
            for line in lines[1:]:
                values = line.split(',')
                if len(values) != len(column_names):
                    print(f"Warning: Row has {len(values)} values but expected {len(column_names)}")
                    continue
                
                record = dict(zip(column_names, values))
                # Convert specific fields to integers
                record['hours_worked'] = int(record.get('hours_worked', 0))
                record['rate'] = int(record.get('rate', 0))

                records.append(record)

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

    return records


def read_csv_files(file_paths: List[str]) -> List[Dict]:
    all_data = []
    for path in file_paths:
        file_data = read_csv_file(path)
        all_data.extend(file_data)
    return all_data
