# 📈 FINANCIAL ANALYSIS MODELS IN PYTHON

Este repositorio contiene una colección de modelos financieros desarrollados en Python. Cada uno de estos scripts está enfocado en el análisis fundamental de empresas, proyecciones financieras, valoración mediante flujos de caja descontados (DCF), y uso de APIs para extraer datos en tiempo real.

---

## 🧠 Contenido del Repositorio

### ✅ Modelos de Razones Financieras
Scripts para calcular:
- **Rentabilidad:** ROE, ROA, margen bruto, margen operativo
- **Liquidez:** ratio corriente, prueba ácida
- **Solvencia:** deuda/capital, cobertura de intereses
- **Eficiencia:** rotación de activos, ciclo de conversión de efectivo

### ✅ Cálculo de WACC (Weighted Average Cost of Capital)
- Cálculo del costo de capital propio (CAPM)
- Costo promedio ponderado de deuda
- WACC ajustado con estructura de capital y tasa impositiva

### ✅ Proyecciones DCF (Discounted Cash Flow)
- Extracción de flujos de caja históricos desde APIs
- Forecast de Free Cash Flow (FCF) a 5 años
- Valor terminal y valor presente neto (NPV)
- Precio objetivo estimado

### ✅ Uso de APIs Financieras
- [x] **Financial Modeling Prep**
- [x] **Yahoo Finance / YahooQuery**
- Descarga de:
  - Estados financieros
  - Indicadores de mercado
  - Ratios históricos y precios

---

## 📦 Librerías Requeridas
numpy
pandas
matplotlib
seaborn

Instala los paquetes con:

```bash
pip install -r requirements.txt
