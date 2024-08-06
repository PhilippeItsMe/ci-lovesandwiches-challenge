import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data ():
    """
    Get sales figures input from the user
    """
    while True:
        print ("Please enter your sales data from the last market.")
        print ("Data should be six numbers separated by commas.")
        print ("Example : 10,20,30,40,50,60\n")

        data_str = input ("Enter your data here: \n")
        
        # Transform the sting on a list [] of data
        sales_data = data_str.split (',')
        validate_data(sales_data)

        if validate_data (sales_data):
            print ("Data is valid \n")
            break

    return (sales_data)

def validate_data (values):
    """
    Validate if there a 6 values inside the list and if the values are integers.
    """
    try:
        [int(value) for value in values] #Creation of a list with all the value in values without error message
        if len(values) != 6:
            raise ValueError (
                f"Exactly 6 values are required" #Definition of the value error message
            )
    except ValueError as e: # Encapluse the value error message in e
        print (f"Invalid data: {e}, please try again.\n")
        return False

    return True 

def calculate_surplus_data (sales_row):
    """
    Calulate the surplus by comparing the sales and the stock 
    """
    print ('Calulating the surplus... \n')
    stock = SHEET.worksheet ("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row): #Zip method allow to work on 2 lists on the same time
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return (surplus_data)

def update_worksheet(data, worksheet):
    """
    Upload data in the love sandwiches worksheet
    """
    print (f"Updating {worksheet} worksheet... \n")
    surplus_worksheet = SHEET.worksheet(worksheet)
    surplus_worksheet.append_row(data)
    print (f"Worksheet {worksheet} updated successfully.\n")

def get_last_5_entries_sales():
    """
    Calculate the wished stock for the next market, the average of the last 5 market + 10% + rounder number
    """
    sales = SHEET.worksheet('sales')
    #column = sales.col_values(3) #dont start at 0
    #print (column)

    columns = []
    for ind in range(1,7):
            column = sales.col_values(ind)
            columns.append (column[-5:]) #the 5 last elements
    return (columns)

def calculate_stock_data (data):
    """
    Calculate the advised stock data
    """
    print ("Calculating the next stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append (round(stock_num))

    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,'sales')
    surplus = calculate_surplus_data (sales_data)
    update_worksheet(surplus, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data (sales_columns)
    update_worksheet(stock_data, 'stock')

print ('Welcome to the Love Sandwiches Data Automation')
main()
