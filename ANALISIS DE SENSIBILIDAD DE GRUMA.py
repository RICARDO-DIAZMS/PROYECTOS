import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Datos iniciales
wacc = 0.11  # 11%
precio_actual = 378.36  # MXN
crecimiento_ingresos = 0.08  # 8%
ventas_2023 = 6486  # en millones de dólares
ebitda_2023 = 1013  # EBITDA en millones de dólares
utilidad_neta_2023 = 531  # Utilidad neta en millones de dólares
acciones_en_circulacion = 441.231  # Millones de acciones
tipo_cambio = 20.4054  # USD/MXN

# Supuestos de flujo de caja libre (FCF) y horizonte de proyección
horizonte = 5  # años de proyección
crecimiento_fcf = 0.085  # Crecimiento esperado del flujo de caja libre después del horizonte explícito

# Estimación de flujo de caja libre (FCF)
impuesto_tasa = 0.3  # 30% de impuestos
capex_sobre_ebitda = 0.23  # Basado en capex de 233M sobre EBITDA de 1013M

fcf_base = ebitda_2023 * (1 - impuesto_tasa) - (ebitda_2023 * capex_sobre_ebitda)
fcfs = []
for i in range(1, horizonte + 1):
    fcfs.append(fcf_base * (1 + crecimiento_ingresos) ** i)

# Cálculo del valor terminal con manejo de error
if wacc > crecimiento_fcf:
    valor_terminal = fcfs[-1] * (1 + crecimiento_fcf) / (wacc - crecimiento_fcf)
else:
    valor_terminal = float('inf')  # Manejo de caso donde WACC <= crecimiento_fcf
if wacc > crecimiento_fcf:
    valor_terminal = fcfs[-1] * (1 + crecimiento_fcf) / (wacc - crecimiento_fcf)
else:
    valor_terminal = np.nan  # Reemplazar 'inf' con NaN

# Descontamos los flujos de caja al presente
valor_presente_fcfs = [fcf / (1 + wacc) ** (i + 1) for i, fcf in enumerate(fcfs)]
valor_presente_terminal = valor_terminal / (1 + wacc) ** horizonte

# Valor de la empresa y de la acción
valor_empresa = sum(valor_presente_fcfs) + valor_presente_terminal
valor_accion = (valor_empresa * tipo_cambio) / acciones_en_circulacion

# Análisis de sensibilidad
crecimiento_fcf_range = np.linspace(0.05, 0.09, 5)  # 5% a 9%
wacc_range = np.linspace(0.09, 0.13, 5)  # 9% a 13%
precios_objetivo = np.empty((len(crecimiento_fcf_range), len(wacc_range)))

for i, crecimiento_fcf in enumerate(crecimiento_fcf_range):
    for j, wacc_sens in enumerate(wacc_range):
        if wacc_sens > crecimiento_fcf:
            valor_terminal_sens = fcfs[-1] * (1 + crecimiento_fcf) / (wacc_sens - crecimiento_fcf)
        else:
            valor_terminal_sens = float('inf')
        valor_presente_terminal_sens = valor_terminal_sens / (1 + wacc_sens) ** horizonte
        valor_empresa_sens = sum(valor_presente_fcfs) + valor_presente_terminal_sens
        precios_objetivo[i, j] = (valor_empresa_sens * tipo_cambio) / acciones_en_circulacion

# Mostrar resultados de sensibilidad
plt.figure(figsize=(10, 6))
c = plt.imshow(precios_objetivo, cmap="coolwarm", origin="lower",
               extent=[wacc_range.min(), wacc_range.max(), crecimiento_fcf_range.min(), crecimiento_fcf_range.max()])
plt.colorbar(c, label="Precio Objetivo (MXN)")
plt.xlabel("WACC")
plt.ylabel("Tasa de Crecimiento Perpetuo")
plt.title("Análisis de Sensibilidad del Precio Objetivo de GRUMA")
plt.grid(True)
plt.show()

# Resultados finales
print(f"Precio Objetivo de la Acción: {valor_accion:.2f} MXN")
print("Matriz de Precios Objetivo (Sensibilidad):")
print(pd.DataFrame(precios_objetivo, index=[f"g={g*100:.1f}%" for g in crecimiento_fcf_range],
                    columns=[f"WACC={w*100:.1f}%" for w in wacc_range]))

print("Flujos de Caja Libre Proyectados:")
for i, fcf in enumerate(fcfs, start=1):
    print(f"Año {i}: {fcf:.2f}")

print(f"Valor Terminal: {valor_terminal:.2f}")
print(f"Valor Empresa: {valor_empresa:.2f}")
print(f"Valor de la Acción: {valor_accion:.2f}")
