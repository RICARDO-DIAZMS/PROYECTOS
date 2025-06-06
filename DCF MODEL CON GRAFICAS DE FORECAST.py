#pip install yahooquery
import pandas as pd
import numpy as np
import datetime
import time


from yahooquery import Ticker

pd.set_option("display.max_rows",None)

symbol = "DIS"

stock = Ticker(symbol)

# AGARRAR EL HISTORICO DE LOS FLUJOS DE CAJA PARA HACER UN FORCAST

df_cash = pd.DataFrame(stock.cash_flow())
df_cash["asOfDate"]= pd.to_datetime(df_cash["asOfDate"])
df_cash.set_index("asOfDate", inplace=True)
cass_period = df_cash["periodType"].iloc[0]
df_cash = df_cash.iloc[:, 2:]
df_cash["FreeCashFlow"]

# EXTRAER LA DEUDA NETA DEL ESTADO

df_balance = pd.DataFrame(stock.balance_sheet())
df_balance["asOfDate"] = pd.to_datetime(df_balance["asOfDate"])
df_balance.set_index("asOfDate", inplace=True)

df_balance = df_balance.iloc[:, 2:]

net_debt = df_balance["NetDebt"].iloc[-1]
net_debt

# crear y convertir una Lista de funciones de la futura gestión

def column_to_list(df,column_name):
    data_list = df[column_name].tolist()
    data_list = [x for x in data_list if pd.notnull(x)]
    return data_list

historic_fcf = column_to_list(df_cash,"FreeCashFlow")
historic_fcf

# calcular la tasa de crecimiento promedio
fcf_avg_growth_rate = np.mean([(historic_fcf[i]-historic_fcf[i-1]) / historic_fcf[i-1] for i in range(1, len(historic_fcf))])
fcf_avg_growth_rate


# PROYECCIONES PARA 5 AÑOS ( SIMPLE FORECAST)

future_year = 5
future_fcf = [historic_fcf[-1]*(1+fcf_avg_growth_rate)**(i+1) for i in range(future_year)]
future_fcf

# CREACION DE GRAFICAS:

import matplotlib.pyplot as plt
# DATOS DE PRUEBA
historical_years = [2020,2021,2023,2024,2025]

forecast_years = [2025,2026,2027,2028,2029]
# COMBINAR LOS DATOS PARA PLOTTEAR:
    
all_years = historical_years + forecast_years
all_fcf = historic_fcf + future_fcf

# CREAR DATOS PARA PLOTTEAR
plt.figure(figsize=(10,6))

# PLOT DE LOS DATOS HISTORICOS
plt.plot(historical_years,historic_fcf, marker="o", linestyle="-", color = "blue", label="HISTORICAL FCF")

# PLOT DE LOS DATOS PRONOSTICADOS
plt.plot(forecast_years, future_fcf, marker="o", linestyle="--", color = "red", label="FORECAST FCF") 

# AGREGAR LA LINA VERTUCAL PARA SEPARAR EL HISTORICO CON EL PRONOSTICO
plt.axvline(x=historical_years[-1], color="gray",linestyle = ":", label="CURRENT YEAR")

# PERSONALIZAR EL PLOT

plt.title("FREE CASH FLOW: HISTORICAL VS FORECAST", fontsize=16)
plt.xlabel("YEAR", fontsize=12)
plt.ylabel("FREE CASH FLOW(IN MILLIONS)", fontsize=12)
plt.grid(True, linestyle = "--", alpha=0.7)
plt.legend()

# AJUSTAR EL EJE Y DESDE EL ORIGEN
plt.ylim(bottom=0)

# AGREGAR DATOS A LAS ETIQUETAS
for i, value in enumerate(all_fcf):
    plt.text(all_years[i], value, f"{value}", ha="center", va="bottom")
# MOSTRAR PLOT

plt.tight_layout()
plt.show()