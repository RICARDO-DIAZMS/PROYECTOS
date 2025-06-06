import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def fetch_financial_data(ticker):
    stock = yf.Ticker(ticker)
    income_statement = stock.financials
    cash_flow = stock.cashflow
    balance_sheet = stock.balance_sheet
    info = stock.info
    return income_statement, cash_flow, balance_sheet, info

def prepare_data(cash_flow, income_statement, balance_sheet):
    cash_flow = cash_flow.transpose()
    latest_free_cash_flow = cash_flow['Free Cash Flow'].iloc[0]

    latest_net_income = income_statement.loc['Net Income'].iloc[0]
    previous_net_income = income_statement.loc['Net Income'].iloc[1]
    net_income_growth_rate = (latest_net_income - previous_net_income) / previous_net_income

    latest_revenue = income_statement.loc['Total Revenue'].iloc[0]
    previous_revenue = income_statement.loc['Total Revenue'].iloc[1]
    revenue_growth_rate = (latest_revenue - previous_revenue) / previous_revenue
    
    latest_assets = balance_sheet.loc['Total Assets'].iloc[0]
    latest_liabilities = balance_sheet.loc['Total Debt'].iloc[0]
    equity = latest_assets - latest_liabilities
    
    return latest_free_cash_flow, net_income_growth_rate, revenue_growth_rate, equity, latest_assets, latest_liabilities

def calculate_dcf(free_cash_flow, discount_rate, growth_rate, years=5):
    cash_flows = []
    future_cash_flows = []
    
    for year in range(1, years + 1):
        future_cash_flow = free_cash_flow * ((1 + growth_rate) ** year)  
        discounted_cash_flow = future_cash_flow / ((1 + discount_rate) ** year)  
        cash_flows.append(discounted_cash_flow)
        future_cash_flows.append(future_cash_flow)

    dcf_value = sum(cash_flows)
    return dcf_value, cash_flows, future_cash_flows

def forecast_future_price(dcf_value, shares_issued, pe_ratio):
    future_price = (dcf_value / shares_issued) * pe_ratio
    return future_price

def calculate_pe_ratio(income_statement, shares_issued):
    latest_net_income = income_statement.loc['Net Income'].iloc[0]  
    pe_ratio = latest_net_income / shares_issued
    return pe_ratio

def calculate_future_stock_prices(latest_price, growth_rate, years):
    future_prices = []
    for year in range(1, years + 1):
        future_price = latest_price * ((1 + growth_rate) ** year)  
        future_prices.append(future_price)
    return future_prices

def analyze_financials(income_statement, cash_flow, balance_sheet, discount_rate=0.1, ebitda_multiple=10, market_cap=None):
    total_revenue = income_statement.loc['Total Revenue']
    total_expenses = income_statement.loc['Total Expenses']
    net_income = income_statement.loc['Net Income']
    free_cash_flow = cash_flow.loc['Free Cash Flow']
    ebitda = income_statement.loc['EBITDA']
    interest_expense = income_statement.loc['Interest Expense']
    ebit = income_statement.loc['EBIT']
    total_debt = balance_sheet.loc['Total Debt']
    total_assets = balance_sheet.loc['Total Assets']
    total_liabilities = balance_sheet.loc['Total Debt']
    shareholder_equity = total_assets - total_liabilities

    # EBITDA Multiples Valuation
    latest_ebitda = ebitda.iloc[0]
    enterprise_value = latest_ebitda * ebitda_multiple
    print(f"EBITDA-based valuation suggests an enterprise value of: ${enterprise_value:,.2f}")

    # Gross Profit and Margins
    gross_profit = income_statement.loc['Gross Profit']
    gross_margin = (gross_profit / total_revenue) * 100
    print(f"Gross Profit Margin: {gross_margin.iloc[0]:.2f}%")

    # EBIT Margin
    ebit_margin = (ebit / total_revenue) * 100
    print(f"EBIT Margin: {ebit_margin.iloc[0]:.2f}%")

    # Interest Coverage Ratio
    if interest_expense.iloc[0] > 0:
        interest_coverage = ebit.iloc[0] / interest_expense.iloc[0]
        print(f"Interest Coverage Ratio: {interest_coverage:.2f}")
    else:
        print("No interest expenses for the period.")

    # Price to Earnings (P/E) Ratio
    if market_cap and net_income.iloc[0] > 0:
        pe_ratio = market_cap / net_income.iloc[0]
        print(f"Price to Earnings (P/E) Ratio: {pe_ratio:.2f}")
    else:
        print("Market capitalization or net income unavailable for P/E calculation.")

    # Debt Ratios and Return on Assets (ROA)
    debt_to_equity = total_debt.iloc[0] / shareholder_equity
    print(f"Debt to Equity Ratio: {debt_to_equity}")

    roe = (net_income.iloc[0] / shareholder_equity) * 100
    print(f"Return on Equity (ROE): {roe}%")

    roa = (net_income.iloc[0] / total_assets.iloc[0]) * 100
    print(f"Return on Assets (ROA): {roa}%")

    # Return on Invested Capital (ROIC)
    roic = (net_income.iloc[0] - interest_expense.iloc[0]) / (total_assets.iloc[0] - total_liabilities.iloc[0])
    print(f"Return on Invested Capital (ROIC): {roic:.2f}%")

    # Checking for positive free cash flow and net income
    if (net_income > 0).all() and (free_cash_flow > 0).all():
        print("The company has positive net income and free cash flow. Analyzing deeper metrics...")
        
        growth_rate = 0.05
        projected_cash_flows = []
        for year in range(1, 6):
            projected_cash_flow = free_cash_flow.iloc[0] * ((1 + growth_rate) ** year)
            discounted_cash_flow = projected_cash_flow / ((1 + discount_rate) ** year)
            projected_cash_flows.append(discounted_cash_flow)
        
        terminal_value = (projected_cash_flows[-1] * (1 + growth_rate)) / (discount_rate - growth_rate)
        total_dcf_value = np.sum(projected_cash_flows) + terminal_value
        
        print(f"DCF-based valuation suggests a value of: ${total_dcf_value:,.2f}")
        
        return True
    else:
        print("The financials are mixed. Further analysis needed.")
        return False

def plot_results(years_range, future_cash_flows, dcf_value, latest_free_cash_flow, future_stock_prices, latest_price, asset_ticker):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))  

    ax1.plot(years_range, future_stock_prices, marker='o', label='Predicted Future Stock Price', color='purple', linewidth=2)
    ax1.axhline(y=latest_price, color='blue', linestyle='--', label=f'Current Stock Price {round(latest_price, 2)}', linewidth=2)
    ax1.set_title(f'{asset_ticker} Stock Price and Future Price Projection', fontsize=16)
    ax1.set_xlabel('Years', fontsize=14)
    ax1.set_ylabel('Stock Price ($)', fontsize=14)
    ax1.set_xticks(years_range)
    ax1.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()
    ax1.set_ylim(bottom=0)

    ax2.plot(years_range, future_cash_flows, marker='o', label='Future Cash Flows', color='blue', linewidth=2)
    ax2.axhline(y=dcf_value, color='red', linestyle='--', label=f'DCF Value {round(dcf_value, 2):,.2f}')
    ax2.set_title(f'DCF Analysis', fontsize=16)
    ax2.set_xlabel('Years', fontsize=14)
    ax2.set_ylabel('Value ($)', fontsize=14)
    ax2.set_xticks(years_range)
    ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()
    ax2.set_ylim(bottom=0)

    ax3.bar(years_range, future_cash_flows, label='Future Cash Flows', color='orange', alpha=0.7)
    ax3.axhline(y=latest_free_cash_flow, color='green', linestyle='--', label=f'Current Free Cash Flow {latest_free_cash_flow:,.2f}', linewidth=2)
    ax3.set_title(f'Free Cash Flow Analysis', fontsize=16)
    ax3.set_xlabel('Years', fontsize=14)
    ax3.set_ylabel('Free Cash Flow ($)', fontsize=14)
    ax3.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.legend()
    ax3.set_ylim(bottom=0)

    plt.tight_layout()
    plt.show()




def main():
    asset_ticker = 'NVIDA'
    income_statement, cash_flow, balance_sheet, info = fetch_financial_data(asset_ticker)

    latest_free_cash_flow, net_income_growth_rate, revenue_growth_rate, equity, latest_assets, latest_liabilities = prepare_data(cash_flow, income_statement, balance_sheet)

    discount_rate = 0.1  
    dcf_value, future_cash_flows, _ = calculate_dcf(latest_free_cash_flow, discount_rate, revenue_growth_rate, years=5)

    latest_price = info['currentPrice']
    pe_ratio = calculate_pe_ratio(income_statement, info['sharesOutstanding'])
    future_stock_prices = calculate_future_stock_prices(latest_price, revenue_growth_rate, years=5)
    
    years_range = np.arange(1, 6)
    
    analyze_financials(income_statement, cash_flow, balance_sheet, discount_rate=0.1, ebitda_multiple=10, market_cap=info['marketCap'])
    plot_results(years_range, future_cash_flows, dcf_value, latest_free_cash_flow, future_stock_prices, latest_price, asset_ticker)

if __name__ == "__main__":
    main()