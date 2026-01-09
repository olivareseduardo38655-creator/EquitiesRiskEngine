# Equities Risk Engine

![Java](https://img.shields.io/badge/Java-21-007396?style=flat-square&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Maven](https://img.shields.io/badge/Build-Maven-C71A36?style=flat-square&logo=apachemaven&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-gray?style=flat-square)
![Status](https://img.shields.io/badge/Status-MVP-green?style=flat-square)

## Descripción Ejecutiva

Este sistema es un motor computacional de alto rendimiento diseñado para la modelación, simulación y valuación de instrumentos financieros derivados bajo incertidumbre. El proyecto se centra en la estimación precisa de métricas de riesgo de cola (Tail Risk) como el **Value at Risk (VaR)** y **Expected Shortfall (ES)**.

La solución implementa una arquitectura híbrida: un núcleo de cálculo numérico en **Java 21** para la ejecución masiva de simulaciones de Monte Carlo, y una capa de validación estadística en **Python** para analizar la normalidad de los retornos y la convergencia de las simulaciones. El sistema utiliza modelos estándar de industria como **Black-Scholes-Merton** y **Movimiento Browniano Geométrico (GBM)**.

## Fundamentos Matemáticos

El núcleo del motor implementa la discretización numérica de Ecuaciones Diferenciales Estocásticas (SDE).

### 1. Dinámica del Activo (SDE)

**Modelo Base: Movimiento Browniano Geométrico (GBM)**
Se asume que el activo sigue un proceso estocástico log-normal:

$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

Para la simulación, utilizamos la solución exacta bajo la medida neutral al riesgo:

$$S_T = S_0 \exp\left( \left( r - \frac{1}{2}\sigma^2 \right)T + \sigma \sqrt{T} Z \right)$$

Donde:
* $W_t$: Proceso de Wiener estándar.
* $Z$: Variable aleatoria normal estándar $N(0,1)$.

### 2. Valuación (Pricing)

El precio justo de la opción Call Europea se calcula mediante la fórmula cerrada de Black-Scholes:

$$C(S, t) = S_0 N(d_1) - K e^{-rT} N(d_2)$$

Donde $N(\cdot)$ es la función de distribución acumulada normal.

### 3. Métricas de Riesgo (Risk Measures)

El sistema calcula el riesgo de pérdida extrema basándose en la distribución empírica de P&L generada por la simulación:

**Expected Shortfall (ES):**
$$ES_{\alpha} = E[ L \mid L \ge VaR_{\alpha} ]$$

## Objetivos Técnicos

1.  **Arquitectura Limpia (Clean Architecture):** Desacoplamiento estricto entre la lógica de dominio (`EuropeanOption`, `MarketSnapshot`) y los motores matemáticos, permitiendo pruebas unitarias aisladas.
2.  **Inmutabilidad y Thread-Safety:** Uso extensivo de **Java Records** para garantizar la integridad de los datos financieros a través del pipeline de ejecución.
3.  **Interoperabilidad:** Diseño de un flujo ETL donde Java genera artefactos de datos (CSV) y Python consume estos resultados para auditoría estadística (Pruebas de Shapiro-Wilk y visualización).
4.  **Rendimiento Numérico:** Implementación optimizada utilizando `Apache Commons Math` para cálculos de precisión y generación de números pseudoaleatorios (Mersenne Twister).

## Arquitectura del Sistema

```mermaid
graph LR
    A[Input Config] -->|Inject| B(Monte Carlo Engine)
    subgraph Core Java Layer
    B --> C{Simulation Kernel}
    C -->|Generate Paths| D[GBM Process]
    D --> E[Pricing Engine]
    E -->|Mark-to-Market| F[PnL Distribution]
    F --> G[Risk Metrics Calculator]
    end
    F -->|Raw Data Export| H[(CSV Files)]
    H --> I[Python Validation Layer]
    I --> J[Distribution Plot]
    I --> K[VaR/ES Analysis]
