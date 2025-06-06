#! pip install matplotlib
#! pip install pandas
# pip install requests  # Use ! to run pip install as a shell command in Colab
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

api_key = "hLlPuUcb6EQmqNxkGqWb7GmnvAesXwPh"
company = "DIS"
years = 5
def get_historical_fcf(api_key, company, years):
    response = requests.get(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{company}?limit={years}&apikey={api_key}")
    data = response.json()
    return [item['freeCashFlow'] for item in data][::-1]

def calculate_liquidity_ratio(current_assets, current_liabilities):
    return current_assets / current_liabilities

def calculate_roe(net_income, shareholder_equity):
    return net_income / shareholder_equity

def calculate_roa(net_income, total_assets):
    return net_income / total_assets

def calculate_capm(risk_free_rate, beta, market_return):
    return risk_free_rate + beta * (market_return - risk_free_rate)

def estimate_fcf_growth_rate(historical_fcf):
    growth_rates = [historical_fcf[i] / historical_fcf[i-1] - 1 for i in range(1, len(historical_fcf))]
    return np.mean(growth_rates)

def project_fcf(historical_fcf, growth_rate, years=5):
    last_fcf = historical_fcf[-1]
    return [last_fcf * ((1 + growth_rate) ** i) for i in range(1, years + 1)]

def calculate_wacc(cost_of_equity, cost_of_debt, equity, debt, tax_rate):
    return (equity / (equity + debt)) * cost_of_equity + (debt / (equity + debt)) * cost_of_debt * (1 - tax_rate)

def calculate_present_value(future_fcf, discount_rate):
    return sum([fcf / ((1 + discount_rate) ** i) for i, fcf in enumerate(future_fcf, 1)])

def calculate_terminal_value(last_fcf, growth_rate, discount_rate):
    return last_fcf * (1 + growth_rate) / (discount_rate - growth_rate)

balance_sheet = requests.get(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?limit={years}&apikey={api_key}")
balance_sheet = balance_sheet.json()

goodwill_and_intangible_assets = balance_sheet[0]["goodwillAndIntangibleAssets"]
total_assets = balance_sheet[0]["totalAssets"]
pct_intangible = goodwill_and_intangible_assets / total_assets
print(f"Pct : {pct_intangible * 100:.2f}")

total_liabilities = balance_sheet[0]["totalLiabilities"]
total_stockholders_equity = balance_sheet[0]["totalStockholdersEquity"]
debt_to_equity_ratio = total_liabilities / total_stockholders_equity
print(f"Debt to Equity Ratio of {company}: {debt_to_equity_ratio * 100:.2f}%")

historical_fcf = get_historical_fcf(api_key, company, years)
growth_rate = estimate_fcf_growth_rate(historical_fcf)
projected_fcf = project_fcf(historical_fcf, growth_rate)

cost_of_equity = 0.1
cost_of_debt = 0.05
equity = total_stockholders_equity
debt = total_liabilities
tax_rate = 0.25

wacc = calculate_wacc(cost_of_equity, cost_of_debt, equity, debt, tax_rate)
present_value = calculate_present_value(projected_fcf, wacc)
terminal_value = calculate_terminal_value(projected_fcf[-1], growth_rate, wacc)

print(f"Projected FCF: {projected_fcf}")
print(f"WACC: {wacc}")
print(f"Present Value of FCF: {present_value}")
print(f"Terminal Value: {terminal_value}")
