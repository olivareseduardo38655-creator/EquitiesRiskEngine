import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# 1. Cargar Datos del Engine Java
FILE_PATH = 'risk_simulation_results.csv' # Asegúrate de que esté en la misma carpeta o pon la ruta completa
print(f"📂 Cargando datos de: {FILE_PATH}")

try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    print("❌ Error: No se encuentra el archivo CSV. Ejecuta primero el proyecto Java.")
    exit()

# 2. Análisis Estadístico del PnL
pnl = df['PnL']
mean_pnl = np.mean(pnl)
std_pnl = np.std(pnl)
min_pnl = np.min(pnl)
max_pnl = np.max(pnl)

print("\n📊 --- RESUMEN ESTADÍSTICO (Validación Cruzada) ---")
print(f"Escenarios procesados: {len(df)}")
print(f"PnL Promedio: {mean_pnl:.4f}")
print(f"Desviación Estándar: {std_pnl:.4f}")
print(f"Peor Escenario (Min): {min_pnl:.4f}")
print(f"Mejor Escenario (Max): {max_pnl:.4f}")

# 3. Validación de Distribución (Test Shapiro-Wilk)
# Si p-value > 0.05, es probablemente Normal (Gaussian)
stat, p_value = stats.shapiro(pnl.sample(1000)) # Sampleamos porque Shapiro es sensible a n grande
print(f"\n🧪 Test de Normalidad (Shapiro-Wilk): p-value={p_value:.4f}")
if p_value > 0.05:
    print("✅ La distribución del PnL parece Normal (Consistente con Black-Scholes a corto plazo).")
else:
    print("⚠️ La distribución del PnL NO es perfectamente normal (Esperado en opciones por la curvatura/Gamma).")

# 4. Generación de Gráficos
plt.figure(figsize=(12, 6))

# Histograma de PnL
plt.subplot(1, 2, 1)
sns.histplot(pnl, kde=True, color='skyblue', bins=50)
plt.axvline(np.percentile(pnl, 5), color='red', linestyle='--', label='VaR 95%')
plt.title('Distribución de Ganancias y Pérdidas (PnL)')
plt.xlabel('PnL ($)')
plt.legend()

# Scatter Spot vs PnL (Validación de Delta)
plt.subplot(1, 2, 2)
plt.scatter(df['Simulated_Spot'], df['PnL'], alpha=0.1, color='purple', s=1)
plt.title('Perfil de Pago (Spot vs PnL)')
plt.xlabel('Spot Simulado ($)')
plt.ylabel('PnL ($)')
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
print("\n📈 Generando gráficos de validación...")
plt.show()
