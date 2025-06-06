import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================
# 1. Rutas de los archivos 
# =============================
income_statement_path = r"C:\Users\ricar\OneDrive\Escritorio\ESTADOS FINANCIEROS GRUMA\incomeStatement-GRUMAB.MX-annual.csv"
cashflow_statement_path = r"C:\Users\ricar\OneDrive\Escritorio\ESTADOS FINANCIEROS GRUMA\cashflowStatement-GRUMAB.MX-annual.csv"
balance_sheet_path = r"C:\Users\ricar\OneDrive\Escritorio\ESTADOS FINANCIEROS GRUMA\balanceSheetStatement-GRUMAB.MX-annual.csv"

# =============================
# 2. Lectura de DataFrames y limpieza de columnas
# =============================
df_income = pd.read_csv(income_statement_path)
df_cashflow = pd.read_csv(cashflow_statement_path)
df_balance = pd.read_csv(balance_sheet_path)

df_income.columns = df_income.columns.str.strip()
df_cashflow.columns = df_cashflow.columns.str.strip()
df_balance.columns = df_balance.columns.str.strip()

# =============================
# 3. Cálculo de Ratios (ejemplo)
# =============================
# a) Margen Operativo = operatingIncome / revenue
if 'operatingIncome' in df_income.columns and 'revenue' in df_income.columns:
    df_income['operatingMargin'] = df_income['operatingIncome'] / df_income['revenue']
    print("\nMargen Operativo (últimos registros):")
    print(df_income[['date', 'revenue', 'operatingIncome', 'operatingMargin']].tail())
else:
    print("\nNo se pudo calcular el Margen Operativo. Verifica 'operatingIncome' y 'revenue'.")

# b) ROE = netIncome / totalEquity (usando el último año)
if 'netIncome' in df_income.columns and 'totalEquity' in df_balance.columns:
    net_income = df_income.iloc[-1]['netIncome']
    total_equity = df_balance.iloc[-1]['totalEquity']
    roe = net_income / total_equity
    print(f"\nROE (último año): {roe:.2%}")
else:
    print("\nNo se pudo calcular el ROE. Verifica 'netIncome' y 'totalEquity'.")

# =============================
# 4. Extraer FCF histórico y preparar datos
# =============================
if 'date' not in df_cashflow.columns or 'freeCashFlow' not in df_cashflow.columns:
    print("\nNo se encontraron las columnas 'date' o 'freeCashFlow' en el Cash Flow Statement.")
else:
    # Convertir la columna 'date' a tipo datetime y extraer el año
    df_cashflow['date'] = pd.to_datetime(df_cashflow['date'], errors='coerce')
    df_cashflow['year'] = df_cashflow['date'].dt.year
    
    # Ordenar por año (de menor a mayor)
    df_cashflow = df_cashflow.sort_values(by='year')
    
    # Filtrar filas donde 'freeCashFlow' no sea NaN
    df_cashflow = df_cashflow.dropna(subset=['freeCashFlow'])
    
    # Agrupar por año (en caso de que haya varias filas por año) y tomar el último valor
    # (o podrías sumar, promediar, etc., según tu criterio)
    df_fcf_yearly = df_cashflow.groupby('year', as_index=False)['freeCashFlow'].last()
    
    # Años históricos y FCF (en forma de listas)
    historical_years = df_fcf_yearly['year'].values
    historical_fcf = df_fcf_yearly['freeCashFlow'].values
    
    print("\nFCF Histórico por Año:")
    print(df_fcf_yearly)
    
    # Tomar el último valor histórico de FCF para proyectar
    last_fcf = historical_fcf[-1]
    
    # =============================
    # 5. Forecast DCF (próximos 5 años)
    # =============================
    forecast_years = 5         # Años a proyectar
    growth_rate = 0.04         # Tasa de crecimiento anual (4%)
    discount_rate = 0.08       # Tasa de descuento (8%)
    
    # Proyectar el FCF para los próximos años (sin descontar)
    forecast_fcf = [last_fcf * (1 + growth_rate)**i for i in range(1, forecast_years + 1)]
    
    # Descontar cada flujo
    discounted_fcf = [fcf / ((1 + discount_rate)**i) for i, fcf in enumerate(forecast_fcf, start=1)]
    
    # Calcular el Terminal Value para el último año proyectado
    terminal_value = forecast_fcf[-1] * (1 + growth_rate) / (discount_rate - growth_rate)
    terminal_value_discounted = terminal_value / ((1 + discount_rate)**forecast_years)
    
    # Valor DCF total (suma de flujos descontados + terminal value descontado)
    dcf_value = sum(discounted_fcf) + terminal_value_discounted
    
    print(f"\nProyección de FCF (años 1 a {forecast_years}): {forecast_fcf}")
    print(f"Flujos descontados: {discounted_fcf}")
    print(f"Terminal Value (no descontado): {terminal_value:,.2f}")
    print(f"Terminal Value Descontado: {terminal_value_discounted:,.2f}")
    print(f"Valor DCF estimado: {dcf_value:,.2f}")
    
    # =============================
    # 6. Generar años futuros y valores acumulados (si deseas)
    # =============================
    # Año final histórico
    last_hist_year = historical_years[-1]
    projected_years = np.arange(last_hist_year + 1, last_hist_year + forecast_years + 1)
    
    # (Opcional) Cálculo de un DCF acumulado año a año
    #   - discounted_fcf[i] es el flujo descontado en el año i+1
    #   - en el último año se suma el terminal_value_discounted
    projected_dcf_cumulative = []
    cumulative = 0
    for i, dfc in enumerate(discounted_fcf):
        cumulative += dfc
        if i == forecast_years - 1:
            cumulative += terminal_value_discounted
        projected_dcf_cumulative.append(cumulative)
    
    # =============================
    # 7. Gráfica: Barras (histórico) + Línea (forecast)
    # =============================
    plt.figure(figsize=(12, 6))
    
    plt.plot(historical_years, historical_fcf,'ro--', color='steelblue', label='FCF Histórico')
    
    plt.plot(projected_years, discounted_fcf, 'ro--', label='FCF Descontado (Forecast)')
    
    #  Etiquetar valores en la gráfica
    for x, y in zip(projected_years, discounted_fcf):
        plt.text(x, y, f"{y:,.0f}", ha='center', va='top', fontsize=9, rotation=45)
        
        #  Etiquetar valores en la gráfica
        for x, y in zip(historical_years, historical_fcf):
            plt.text(x, y, f"{y:,.0f}", ha='center', va='top', fontsize=9, rotation=45)
    
    # Personalizar ejes y título
    plt.title("FREE CASH FLOW: HISTORICAL VS FORECAST (SIN ARCHIVO DCF)", fontsize=14, fontweight='bold')
    plt.xlabel("AÑO")
    plt.ylabel("FREE CASH FLOW")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
