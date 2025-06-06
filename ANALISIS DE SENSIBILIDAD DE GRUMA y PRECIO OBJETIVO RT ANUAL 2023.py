import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def calcular_valoracion_dcf(wacc, crecimiento_ingresos, crecimiento_fcf, ebitda_2023, impuesto_tasa, capex_sobre_ebitda, acciones_en_circulacion, tipo_cambio, horizonte=5):
    """
    Calcula la valoración de una acción utilizando el método de Descuento de Flujos de Caja (DCF).
    """
    # Estimación del flujo de caja libre (FCF) inicial
    fcf_base = ebitda_2023 * (1 - impuesto_tasa) - (ebitda_2023 * capex_sobre_ebitda)
    
    # Proyección de flujos de caja libre
    fcfs = [fcf_base * (1 + crecimiento_ingresos) ** i for i in range(1, horizonte + 1)]
    
    # Cálculo del valor terminal con manejo de error
    if wacc > crecimiento_fcf:
        valor_terminal = fcfs[-1] * (1 + crecimiento_fcf) / (wacc - crecimiento_fcf)
    else:
        valor_terminal = np.nan  # Evita valores infinitos en caso de WACC <= crecimiento_fcf
    
    # Descontamos los flujos de caja al presente
    valor_presente_fcfs = [fcf / (1 + wacc) ** (i + 1) for i, fcf in enumerate(fcfs)]
    valor_presente_terminal = valor_terminal / (1 + wacc) ** horizonte if not np.isnan(valor_terminal) else 0
    
    # Valor de la empresa y de la acción
    valor_empresa = sum(valor_presente_fcfs) + valor_presente_terminal
    valor_accion = (valor_empresa * tipo_cambio) / acciones_en_circulacion
    
    return valor_accion

# Parámetros base
wacc = 0.11  # 11%
crecimiento_ingresos = 0.10  # 10%
crecimiento_fcf = 0.07  # 7%
ebitda_2023 = 1006  # EBITDA en millones de dólares
impuesto_tasa = 0.3  # 30% de impuestos
capex_sobre_ebitda = 0.21  # Basado en capex de 211M sobre EBITDA de 1006M
acciones_en_circulacion = 435.6  # Millones de acciones
tipo_cambio = 20.4  # USD/MXN

# Cálculo del precio objetivo con DCF
precio_objetivo = calcular_valoracion_dcf(wacc, crecimiento_ingresos, crecimiento_fcf, ebitda_2023,
                                          impuesto_tasa, capex_sobre_ebitda, acciones_en_circulacion, tipo_cambio)

# Análisis de sensibilidad
crecimiento_fcf_range = np.linspace(0.05, 0.09, 5)  # 5% a 9%
wacc_range = np.linspace(0.09, 0.13, 5)  # 9% a 13%
precios_objetivo = np.empty((len(crecimiento_fcf_range), len(wacc_range)))

for i, crecimiento_fcf in enumerate(crecimiento_fcf_range):
    for j, wacc_sens in enumerate(wacc_range):
        precios_objetivo[i, j] = calcular_valoracion_dcf(wacc_sens, crecimiento_ingresos, crecimiento_fcf, ebitda_2023,
                                                          impuesto_tasa, capex_sobre_ebitda, acciones_en_circulacion, tipo_cambio)

# Reemplazar valores infinitos por NaN en la matriz de sensibilidad
precios_objetivo[np.isinf(precios_objetivo)] = np.nan

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
print(f"Precio Objetivo de la Acción: {precio_objetivo:.2f} MXN")
print("Matriz de Precios Objetivo (Sensibilidad):")
print(pd.DataFrame(precios_objetivo, index=[f"g={g*100:.1f}%" for g in crecimiento_fcf_range],
                    columns=[f"WACC={w*100:.1f}%" for w in wacc_range]))
