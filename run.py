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

        data_str = input ("Enter your data here: ")
        
        # Transform the sting on a list [] of data
        sales_data = data_str.split (',')
        validate_data(sales_data)

        if validate_data (sales_data):
            print ("Data is valid")
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

def update_sales_worksheet(data):
    """
    Upload sales data in the sales worksheet
    """
    print ("Updating sales worksheet... \n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print ("Sales worksheet updated successfully.\n")

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

def update_surplus_worksheet(surplus):
    """
    Upload surplus data in the sales worksheet
    """
    print ("Updating surplus worksheet... \n")
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(surplus)
    print ("Surplus worksheet updated successfully.\n")


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    surplus = calculate_surplus_data (sales_data)
    update_surplus_worksheet(surplus)

print ('Welcome to the Love Sandwiches Data Automation')
main()