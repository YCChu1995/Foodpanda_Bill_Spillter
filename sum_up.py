import csv
import os, re

# Function to convert string with commas to integer
def convert_str_to_int(s):
    if ',' in s: print(s)
    if '.' in s: print(s)
    return int(s.replace(',', ''))

csv_files = [f for f in os.listdir('.') if re.match(r'bill_\d+\.csv', f)]
if csv_files:
    largest_number = max(int(re.search(r'\d+', f).group()) for f in csv_files)

# Load the CSV file
file_path = f'bill_{largest_number}.csv'
with open(file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    # Convert the CSV data to a list of rows
    data = list(csv_reader)
    

# Display the first few rows of the data
total_price: int = 0
for row in data[1:]:
    total_price += convert_str_to_int(row[2])
print(f'{round(total_price/2, 2)} in {len(data[1:])} spendings')
