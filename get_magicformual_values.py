import yfinance as yf
import pandas as pd

def get_financial_data(stock_symbol):
    # Download stock information
    stock = yf.Ticker(stock_symbol)
    
    # Get the market capitalization
    market_cap = stock.info.get('marketCap', 'N/A')
    
    # Get financials (EBIT)
    financials = stock.financials
    #print(financials)
    income = stock.income_stmt
    #print(income.loc['EBIT'])
    ebit = income.loc['EBIT'].iloc[0] if 'EBIT' in income.index else 0
    #print(ebit)
    # Get balance sheet (Current Assets, Current Liabilities, Long Term Debt)
    balance_sheet = stock.balance_sheet
    #print(balance_sheet)
    
    #print(balance_sheet.loc['Current Assets'])
    current_assets = balance_sheet.loc['Current Assets'].iloc[0] if 'Total Current Assets' in balance_sheet.index else 0
    #print(current_assets)
    current_liabilities = balance_sheet.loc['Current Liabilities'].iloc[0] if 'Total Current Liabilities' in balance_sheet.index else 0
    #print(current_liabilities)
    long_term_debt = balance_sheet.loc['Long Term Debt'].iloc[0] if 'Long Term Debt' in balance_sheet.index else 0
    #print(long_term_debt)
    # Get short-term debt (Current Debt)
    short_term_debt = balance_sheet.loc['Current Debt'].iloc[0] if 'Short Long Term Debt' in balance_sheet.index else 0
    #print(short_term_debt)
    # Get cash and cash equivalents
    cash_and_equivalents = balance_sheet.loc['Cash And Cash Equivalents'].iloc[0] if 'Cash And Cash Equivalents' in balance_sheet.index else 0
    #print(cash_and_equivalents)
    # Get total assets and accumulated depreciation for fixed assets calculation
    total_assets = balance_sheet.loc['Total Assets'].iloc[0] if 'Total Assets' in balance_sheet.index else 0
    #print(total_assets)
    accumulated_depreciation = stock.cashflow.loc['Depreciation'].iloc[0] if 'Depreciation' in stock.cashflow.index else 0
    #print(accumulated_depreciation)
    # Calculate Enterprise Value (EV)
    total_debt = long_term_debt + short_term_debt
    if market_cap != 'N/A' and total_debt != 'N/A' and cash_and_equivalents != 'N/A':
        enterprise_value = market_cap + total_debt - cash_and_equivalents
    else:
        enterprise_value = 'N/A'
    #print(enterprise_value)
    # Calculate Net Working Capital (NWC)
    if current_assets != 'N/A' and current_liabilities != 'N/A':
        net_working_capital = current_assets - current_liabilities
    else:
        net_working_capital = 'N/A'
    #print(net_working_capital)
    # Calculate Net Fixed Assets (NFA)
    if total_assets != 'N/A' and current_assets != 'N/A' and accumulated_depreciation != 'N/A':
        net_fixed_assets = total_assets - current_assets - accumulated_depreciation
    else:
        net_fixed_assets = 'N/A'
    #print(net_fixed_assets)
    # Calculate EBIT to Enterprise Value
    if ebit != 'N/A' and enterprise_value != 'N/A':
        ebit_to_ev = round(ebit / enterprise_value, 6)
    else:
        ebit_to_ev = 'N/A'
    #print(ebit_to_ev)
    # Calculate EBIT to (Net Working Capital + Net Fixed Assets)
    if ebit != 'N/A' and net_working_capital != 'N/A' and net_fixed_assets != 'N/A':
        if (net_working_capital + net_fixed_assets) == 0:
            ebit_to_nwc_nfa = 0
        else:
            ebit_to_nwc_nfa = round(ebit / (net_working_capital + net_fixed_assets), 6)
    else:
        ebit_to_nwc_nfa = 'N/A'
    #print(ebit_to_nwc_nfa)
    return {
        'stock_symbol': stock_symbol,
        'market_cap': market_cap,
        'ebit': ebit,
        'enterprise_value': enterprise_value,
        'ebit_to_ev': ebit_to_ev,
        'ebit_to_nwc_nfa': ebit_to_nwc_nfa,
        'net_working_capital': net_working_capital,
        'net_fixed_assets': net_fixed_assets
    }

def get_financial_data_for_stocks(stock_list):
    
    # Create a list to store the results for each stock
    stock_data = []
    
    # Loop through the list of stock symbols
    count = 0
    for symbol in stock_list:
        count = count + 1
        print(count)
        data = get_financial_data(symbol)
        stock_data.append(data)
        if count == 20: 
            exit 

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(stock_data)
    
    return df

def get_sp500_stocks():
    # URL for the Wikipedia page containing the S&P 500 list
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    # Use pandas to read the table from the Wikipedia page
    sp500_table = pd.read_html(url)[0]

    # Display the first few rows of the dataframe
    print(sp500_table.head())

    # You can access the tickers like this
    tickers = sp500_table['Symbol'].tolist()
    return tickers
    

# List of stock symbols (you can add more symbols here)
stock_list = ['MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A']  # Add more stock symbols as needed

tickers = get_sp500_stocks()
# print(tickers)
stock_list = tickers


# Get the financial data for the list of stocks
financial_data_df = get_financial_data_for_stocks(stock_list)
financial_data_df.to_csv('financial_data.csv', index=False)

# Display the DataFrame as a table
#print(financial_data_df)