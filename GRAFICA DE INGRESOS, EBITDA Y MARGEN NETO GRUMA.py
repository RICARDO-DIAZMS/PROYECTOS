import matplotlib.pyplot as plt
import pandas as pd

# Datos históricos de Gruma (2020-2024)
years = [2020, 2021, 2022, 2023, 2024]
revenues = [91103.13, 94723.1, 108988.6, 111493.4, 135056.19]  # Ingresos en millones de MXN
ebitda = [13959.65, 13671.82, 14625.95, 16181.83, 26548.79]  # EBITDA en millones de MXN
net_margin = [11.01, 15.32, 0.42, 17.12, 52.09]  # Margen Neto en %

# Crear un DataFrame
data = {
    'Año': years,
    'Ingresos (miles de millones MXN)': revenues,
    'EBITDA (miles de millones MXN)': ebitda,
    'Margen Neto (%)': net_margin
}

df = pd.DataFrame(data)

# Graficar los datos
fig, axs = plt.subplots(3, 1, figsize=(10, 12))

# Gráfico de Ingresos
axs[0].plot(df['Año'], df['Ingresos (miles de millones MXN)'], marker='o', color='blue', label='Ingresos')
axs[0].set_title('Evolución de Ingresos (2020-2024)')
axs[0].set_xlabel('Año')
axs[0].set_ylabel('Ingresos (miles de millones MXN)')
axs[0].set_xticks(df['Año'])  # Establecer los años como enteros en el eje X
axs[0].grid(True)
axs[0].legend(loc='upper left')

# Gráfico de EBITDA
axs[1].plot(df['Año'], df['EBITDA (miles de millones MXN)'], marker='o', color='green', label='EBITDA')
axs[1].set_title('Evolución de EBITDA (2020-2024)')
axs[1].set_xlabel('Año')
axs[1].set_ylabel('EBITDA (miles de millones MXN)')
axs[1].set_xticks(df['Año'])  # Establecer los años como enteros en el eje X
axs[1].grid(True)
axs[1].legend(loc='upper left')

# Gráfico de Margen Neto
axs[2].plot(df['Año'], df['Margen Neto (%)'], marker='o', color='red', label='Margen Neto')
axs[2].set_title('Evolución de Margen Neto (2020-2024)')
axs[2].set_xlabel('Año')
axs[2].set_ylabel('Margen Neto (%)')
axs[2].set_xticks(df['Año'])  # Establecer los años como enteros en el eje X
axs[2].grid(True)
axs[2].legend(loc='upper left')

# Ajuste de layout para evitar solapamientos
plt.tight_layout()

# Mostrar los gráficos
plt.show()
