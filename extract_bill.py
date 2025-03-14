from bs4 import BeautifulSoup, element
import csv
import os
import re

extracted_info: list[list[str]] = [['ordered_time', 'vendor', 'total_prices', 'item_detail']]

# Load the local HTML file
with open('Foodpanda.html', 'r', encoding='utf-8') as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, 'html.parser')

# Extract all elements with class 'order-item-container'
orders = soup.find_all(class_='order-item-container')
for order in orders:
    vendor = order.find_next(attrs={"data-testid": "order-cart__vendor-name"}).get_text()
    ordered_time = order.find_next(attrs={"data-testid": "past-order-subtitle"}).get_text()[4:]
    for index in range(len(ordered_time)):
        if ordered_time[index] == '日':
            ordered_time = ordered_time[:index+1]
            break
    total_prices = order.find_next(class_=lambda x: x and 'item-price' in x).get_text()[2:]
    items = order.find_all(class_=lambda x: x and 'item-description' in x)
    item_detail = ''
    for item in items: item_detail += item.get_text()

    extracted_info.append([ordered_time, vendor, total_prices, item_detail])

# Find the largest number in the name of existing CSV files
csv_files = [f for f in os.listdir('.') if re.match(r'bill_\d+\.csv', f)]
if csv_files:
    largest_number = max(int(re.search(r'\d+', f).group()) for f in csv_files)
else:
    largest_number = 0

# Increment the largest number to create a new file name
csv_file_path = f'bill_{largest_number + 1}.csv'
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(extracted_info)

print(f"Data has been saved to {csv_file_path}")