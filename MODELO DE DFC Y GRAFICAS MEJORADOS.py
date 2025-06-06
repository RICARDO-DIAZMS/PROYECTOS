#! pip install matplotlib
#! pip install pandas
# pip install requests  # Use ! to run pip install as a shell command in Colab
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

api_key = "hLlPuUcb6EQmqNxkGqWb7GmnvAesXwPh"
company = "DIS"
years = 5
competitors = ["NFLX", "WBD", "PARA"]

def get_financial_data(endpoint, symbol, api_key, years):
    url = f"https://financialmodelingprep.com/api/v3/{endpoint}/{symbol}?limit={years}&apikey={api_key}"
    response = requests.get(url)
    return response.json()

# Obtener estados financieros
income_statement = get_financial_data("income-statement", company, api_key, years)
balance_sheet = get_financial_data("balance-sheet-statement", company, api_key, years)
cash_flow = get_financial_data("cash-flow-statement", company, api_key, years)

# Extraer datos necesarios
revenue = [item["revenue"] for item in income_statement]
net_income = [item["netIncome"] for item in income_statement]
ebit = [item["operatingIncome"] for item in income_statement]
ebitda = [item["ebitda"] for item in income_statement]
total_assets = [item["totalAssets"] for item in balance_sheet]
total_liabilities = [item["totalLiabilities"] for item in balance_sheet]
shareholders_equity = [item["totalStockholdersEquity"] for item in balance_sheet]
free_cash_flow = [item["freeCashFlow"] for item in cash_flow]

# Cálculo de márgenes financieros
net_profit_margin = [ni / rev for ni, rev in zip(net_income, revenue)]
ebit_margin = [e / rev for e, rev in zip(ebit, revenue)]
ebitda_margin = [e / rev for e, rev in zip(ebitda, revenue)]

# Cálculo de ROIC
nopat = [e * 0.75 for e in ebit]  # Asumiendo tasa impositiva del 25%
invested_capital = [ta - tl for ta, tl in zip(total_assets, total_liabilities)]
roic = [n / ic for n, ic in zip(nopat, invested_capital)]

def calculate_cagr(initial_value, final_value, periods):
    return (final_value / initial_value) ** (1 / periods) - 1

revenue_cagr = calculate_cagr(revenue[-1], revenue[0], years)
net_income_cagr = calculate_cagr(net_income[-1], net_income[0], years)

# Benchmarking con competidores
benchmark_data = {}
for competitor in competitors:
    comp_income_statement = get_financial_data("income-statement", competitor, api_key, years)
    comp_revenue = [item["revenue"] for item in comp_income_statement]
    comp_net_income = [item["netIncome"] for item in comp_income_statement]
    comp_net_profit_margin = [ni / rev for ni, rev in zip(comp_net_income, comp_revenue)]
    benchmark_data[competitor] = comp_net_profit_margin

# Proyección de FCF con escenarios
growth_rates = {"optimista": 0.10, "base": 0.05, "pesimista": 0.02}
projected_fcf = {}
for scenario, rate in growth_rates.items():
    projected_fcf[scenario] = [free_cash_flow[-1] * (1 + rate) ** i for i in range(1, 6)]

# Cálculo de valor presente neto de FCF proyectado
wacc = 0.08  # Supuesto WACC del 8%
npv_fcf = {}
for scenario, fcfs in projected_fcf.items():
    npv_fcf[scenario] = sum([fcf / (1 + wacc) ** (i + 1) for i, fcf in enumerate(fcfs)])

# Gráficos
years_range = list(range(1, years + 1))

plt.figure(figsize=(10, 6))
plt.plot(years_range, net_profit_margin, label="Margen de Utilidad Neta")
plt.plot(years_range, ebit_margin, label="Margen EBIT")
plt.plot(years_range, ebitda_margin, label="Margen EBITDA")
plt.xlabel("Años")
plt.ylabel("Margen")
plt.title("Márgenes Financieros Históricos")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(years_range, roic, label="ROIC", color='purple')
plt.xlabel("Años")
plt.ylabel("ROIC")
plt.title("ROIC Histórico")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
for comp, data in benchmark_data.items():
    plt.plot(years_range, data, label=f"{comp} Margen de Utilidad Neta")
plt.plot(years_range, net_profit_margin, label=f"{company} Margen de Utilidad Neta", linestyle="--")
plt.xlabel("Años")
plt.ylabel("Margen")
plt.title("Comparación de Margen de Utilidad Neta")
plt.legend()
plt.grid(True)
plt.show()
