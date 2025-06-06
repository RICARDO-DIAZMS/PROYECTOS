# Datos para el cálculo del FCF y WACC
valor_equity_usd = 35746.78  # en millones de USD
valor_deuda_usd = 1896.6  # en millones de USD
costo_deuda = 6.32 / 100  # en porcentaje
costo_equity = 6.44 / 100  # en porcentaje
tasa_impuesto = 0.30  # tasa de impuesto
ebit_usd = 1006
depreciacion_amortizacion_usd=224029
capex_usd=183539
variacion_nwc_usd=-104652

# Calcular FCF
fcf_usd = (ebit_usd * (1 - tasa_impuesto)) + depreciacion_amortizacion_usd - capex_usd - variacion_nwc_usd

# Calcular WACC
total_valor = valor_equity_usd + valor_deuda_usd
peso_equity = valor_equity_usd / total_valor
peso_deuda = valor_deuda_usd / total_valor
wacc = (peso_equity * costo_equity) + (peso_deuda * costo_deuda * (1 - tasa_impuesto))

fcf_usd, wacc

print(f"\WACC CALCULADA AL REPORTE ANAL 2023 ES {wacc:.5f}")


print(f"\EL FREE TO CASH FLOW CALCULADA AL REPORTE ANAL 2023 ES {fcf_usd:.2f} MILLONES DE USD")