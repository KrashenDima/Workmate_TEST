import pytest
import os
from typing import List, Dict
from tempfile import NamedTemporaryFile

from core.csv_reader import (normalize_column_name, 
                             edit_column_names_list,
                             read_csv_file,
                             read_csv_files)

# Tests for normalize_column_name
@pytest.mark.parametrize("input_name, expected", [
    ("rate", "rate"),
    ("Hourly_Rate", "rate"),
    ("SALARY", "rate"),
    ("name", "name"),
    ("  rate  ", "rate"),
    ("department", "department"),
])
def test_normalize_column_name(input_name, expected):
    assert normalize_column_name(input_name) == expected

# Tests for edit_column_names_list
def test_edit_column_names_list():
    input_columns = ["name", "Hourly_Rate", "department", "SALARY"]
    expected = ["name", "rate", "department", "rate"]
    assert edit_column_names_list(input_columns) == expected

@pytest.fixture
def sample_csv_file():
    content = """id,email,name,department,hours_worked,hourly_rate
    1,alice@example.com,Alice Johnson,Marketing,160,50
    2,bob@example.com,Bob Smith,Design,150,40"""
    
    with NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def empty_csv_file():
    with NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write("")
        f.flush()
        yield f.name
    os.unlink(f.name)

@pytest.fixture
def malformed_csv_file():
    content = """id,email,name,department,hours_worked,hourly_rate
    1,alice@example.com,Alice Johnson,Marketing
    2,bob@example.com,Bob Smith,Design,150,40"""
    
    with NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(content)
        f.flush()
        yield f.name
    os.unlink(f.name)

# Tests for read_csv_file
def test_read_csv_file_success(sample_csv_file):
    result = read_csv_file(sample_csv_file)
    expected = [
        {"id": "1", "email": "alice@example.com", 
         "name": "Alice Johnson", "department": 
         "Marketing", "hours_worked": 160, "rate": 50},

        {"id": "2", "email": "bob@example.com", 
         "name": "Bob Smith", "department": 
         "Design", "hours_worked": 150, "rate": 40}
    ]
    assert result == expected

def test_read_csv_file_empty(empty_csv_file):
    assert read_csv_file(empty_csv_file) == []

def test_read_csv_file_malformed(malformed_csv_file, capsys):
    result = read_csv_file(malformed_csv_file)
    captured = capsys.readouterr()
    
    # Should only process valid rows
    assert len(result) == 1
    assert "Warning: Row has" in captured.out

def test_read_csv_file_not_found(capsys):
    result = read_csv_file("nonexistent_file.csv")
    captured = capsys.readouterr()
    assert result == []
    assert "Error: File not found" in captured.out

# Tests for read_csv_files
def test_read_csv_files(sample_csv_file, tmp_path):
    # Create second test file
    second_file = tmp_path / "second.csv"
    second_file.write_text("""department,id,email,name,hours_worked,rate
                           HR,101,grace@example.com,Grace Lee,160,45""")
    
    result = read_csv_files([sample_csv_file, str(second_file)])
    assert len(result) == 3
    assert any(r["name"] == "Grace Lee" for r in result)

def test_read_csv_files_empty_list():
    assert read_csv_files([]) == []