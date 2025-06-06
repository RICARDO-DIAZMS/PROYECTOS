import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 1. Rutas de los archivos
# ==============================
income_statement_path = r"C:\Users\ricar\OneDrive\Escritorio\ESTADOS FINANCIEROS GRUMA\incomeStatement-GRUMAB.MX-annual.csv"
cashflow_statement_path = r"C:\Users\ricar\OneDrive\Escritorio\ESTADOS FINANCIEROS GRUMA\cashflowStatement-GRUMAB.MX-annual.csv"
balance_sheet_path = r"C:\Users\ricar\OneDrive\Escritorio\ESTADOS FINANCIEROS GRUMA\balanceSheetStatement-GRUMAB.MX-annual.csv"

# ==============================
# 2. Lectura de DataFrames y limpieza de columnas
# ==============================
df_income = pd.read_csv(income_statement_path)
df_cashflow = pd.read_csv(cashflow_statement_path)
df_balance = pd.read_csv(balance_sheet_path)

df_income.columns = df_income.columns.str.strip()
df_cashflow.columns = df_cashflow.columns.str.strip()
df_balance.columns = df_balance.columns.str.strip()

# ==============================
# 3. Cálculos de tasas clave
# ==============================
# Tasa de Crecimiento de los Ingresos (CAGR)
revenue_data = df_income[['date', 'revenue']].sort_values(by='date', ascending=True)
start_revenue = revenue_data['revenue'].iloc[0]  # Primer año
end_revenue = revenue_data['revenue'].iloc[-1]  # Último año
years = len(revenue_data) - 1  # Número de años

CAGR = ((end_revenue / start_revenue) ** (1 / years)) - 1
CAGR_percentage = CAGR * 100

# Cálculo de Margen Bruto Promedio
df_income['grossMargin'] = (df_income['revenue'] - df_income['costOfRevenue']) / df_income['revenue']
average_gross_margin = df_income['grossMargin'].mean()

# ==============================
# 4. Cálculos de Ratios Financieros
# ==============================
# Margen Bruto
margen_bruto= df_income['Gross Margin'] = (df_income['revenue'] - df_income['costOfRevenue']) / df_income['revenue'] * 100

# Margen Neto
margen_neto=df_income['Net Margin'] = df_income['netIncome'] / df_income['revenue'] * 100

# ROE (Retorno sobre el Patrimonio)
ROE=df_balance['ROE'] = df_income['netIncome'] / df_balance['totalStockholdersEquity'] * 100

# ROA (Retorno sobre los Activos)
ROA= df_balance['ROA'] = df_income['netIncome'] / df_balance['totalAssets'] * 100

# Razón Corriente
RZ_CORR= df_balance['Current Ratio'] = df_balance['totalCurrentAssets'] / df_balance['totalCurrentLiabilities']

# Deuda a Capital
deb= df_balance['Debt to Equity'] = df_balance['totalLiabilities'] / df_balance['totalStockholdersEquity'] * 100

# Cobertura de Intereses
df_income['Interest Coverage'] = df_income['operatingIncome'] / df_income['interestExpense']

# P/E (Precio sobre Utilidad) - Necesitamos el precio de la acción y EPS (esto es solo un ejemplo sin valores específicos)
# df_income['P/E'] = df_stock['Price per Share'] / df_income['EPS']

# EV/EBITDA - Necesitamos el valor de la empresa (EV) y EBITDA (esto es solo un ejemplo)
# df_income['EV/EBITDA'] = df_stock['Enterprise Value'] / df_income['EBITDA']

# IMPRESIONES DE LOS RESULTADOS DE LOS RATIOS:

print(margen_bruto)
print(margen_neto)
# 5. Proyecciones de los próximos años
# ==============================
last_revenue = revenue_data['revenue'].iloc[-1]
last_cost_of_revenue = df_income['costOfRevenue'].iloc[-1]

years_to_project = 5 # Número de años a proyectar
projected_revenues = []
projected_cost_of_revenue = []

for year in range(1, years_to_project + 1):
    projected_revenue = last_revenue * (1 + CAGR) ** year
    projected_revenues.append(projected_revenue)
    
    # Proyección del costo de ventas basado en el margen bruto
    projected_cost = projected_revenue * average_gross_margin
    projected_cost_of_revenue.append(projected_cost)

# Crear DataFrame con los resultados proyectados
projection_years = [2025, 2026, 2027,2028,2029]
projection_data = pd.DataFrame({
    'Year': projection_years,
    'Projected Revenue': projected_revenues,
    'Projected Cost of Revenue': projected_cost_of_revenue,
    'Projected Gross Profit': [rev - cost for rev, cost in zip(projected_revenues, projected_cost_of_revenue)],
    'Projected Gross Margin': average_gross_margin * 100  # Proyección de Margen Bruto
})

# ==============================
# 6. Visualización de Resultados
# ==============================
projection_data.set_index('Year', inplace=True)

# Mostrar las proyecciones
print(projection_data)

# Gráfico de las proyecciones
plt.figure(figsize=(10,6))
plt.plot(projection_data.index, projection_data['Projected Revenue'], label='Ingresos Proyectados', marker='o')
plt.plot(projection_data.index, projection_data['Projected Cost of Revenue'], label='Costo de Ventas Proyectado', marker='x')
plt.plot(projection_data.index, projection_data['Projected Gross Profit'], label='Utilidad Bruta Proyectada', marker='s')
plt.title('Proyecciones Financieras (Ingresos, Costo de Ventas y Utilidad Bruta)')
plt.xlabel('Año')
plt.ylabel('Valor en USD')
plt.legend()
plt.grid(True)
plt.show()

# Gráfico de Ratios Financieros
plt.figure(figsize=(10,6))
plt.plot(df_income['date'], df_income['Gross Margin'], label='Margen Bruto')
plt.plot(df_income['date'], df_income['Net Margin'], label='Margen Neto')
plt.title('Ratios Financieros - Margen Bruto y Neto')
plt.xlabel('Año')
plt.ylabel('Porcentaje')
plt.legend()
plt.grid(True)
plt.show()
