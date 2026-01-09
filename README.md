# Stochastic Financial Simulation Engine

![Java](https://img.shields.io/badge/Java-21-007396?style=flat-square&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Maven](https://img.shields.io/badge/Build-Maven-C71A36?style=flat-square&logo=apachemaven&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-gray?style=flat-square)
![Status](https://img.shields.io/badge/Status-Stable-green?style=flat-square)

## Descripción Ejecutiva

Este sistema es un motor computacional de alto rendimiento diseñado para la modelación, simulación y valuación de instrumentos financieros derivados bajo incertidumbre. El proyecto aborda la discrepancia entre los modelos teóricos tradicionales (Black-Scholes) y la realidad empírica de los mercados financieros, caracterizada por colas pesadas y eventos extremos ("Cisnes Negros").

La solución implementa una arquitectura híbrida: un núcleo de cálculo numérico en **Java** para la ejecución masiva de simulaciones de Monte Carlo, y una capa de análisis de datos en **Python** para la visualización de convergencia y distribución de probabilidad. El sistema permite contrastar el comportamiento de activos bajo Movimiento Browniano Geométrico (GBM) frente a Difusión por Saltos de Merton (Merton Jump Diffusion).

## Fundamentos Matemáticos

El núcleo del motor implementa la discretización numérica de Ecuaciones Diferenciales Estocásticas (SDE).

### 1. Dinámica del Activo (SDEs)

**Modelo Base: Movimiento Browniano Geométrico (GBM)**

$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

**Modelo de Riesgo: Difusión por Saltos de Merton (MJD)**
Incorpora un proceso de Poisson para modelar shocks repentinos de mercado:

$$dS_t = (\mu - \lambda k) S_t dt + \sigma S_t dW_t + (J - 1) S_t dN_t$$

Donde:
* $W_t$: Proceso de Wiener estándar (ruido gaussiano).
* $N_t$: Proceso de Poisson con intensidad $\lambda$.
* $J$: Variable aleatoria que representa la magnitud del salto (log-normal).

### 2. Valuación y Riesgo (Pricing & Greeks)

El precio justo de la opción Call Europea se estima descontando la esperanza matemática del Payoff bajo la medida neutral al riesgo:

$$V_0 = e^{-rT} \mathbb{E}^\mathbb{Q} [\max(S_T - K, 0)]$$

La sensibilidad al riesgo de mercado (**Delta**) se calcula mediante el Método de Diferencias Finitas Centrales:

$$\Delta = \frac{\partial V}{\partial S} \approx \frac{V(S_0 + \epsilon) - V(S_0 - \epsilon)}{2\epsilon}$$

## Objetivos Técnicos

1.  **Arquitectura Orientada a Objetos (OOP):** Implementación de polimorfismo mediante la interfaz `StochasticProcess`, permitiendo la inyección de distintos modelos matemáticos (GBM, Merton, Heston) sin alterar el motor de simulación.
2.  **Inmutabilidad y Thread-Safety:** Uso de Java Records (`SimulationConfig`) para garantizar la integridad de los parámetros de simulación a través del ciclo de vida de la ejecución.
3.  **Interoperabilidad:** Diseño de un pipeline de datos desacoplado donde Java genera datos crudos (CSV) y Python consume estos artefactos para análisis estadístico, facilitando la integración con stacks de Data Science.
4.  **Gestión de Riesgo Computacional:** Implementación de semillas deterministas (`RandomGenerator`) para asegurar la reproducibilidad exacta de los escenarios estocásticos (Auditability).

## Arquitectura del Sistema

```mermaid
graph LR
    A[Configuration Input] -->|Inject| B(Monte Carlo Engine)
    subgraph Core Java Layer
    B --> C{Stochastic Process}
    C -->|Normal Market| D[Geometric Brownian Motion]
    C -->|Fat Tails| E[Merton Jump Diffusion]
    D --> F[Path Generation]
    E --> F
    F --> G[Option Pricer]
    G -->|Finite Difference| H[Delta Calculation]
    end
    F -->|Raw Data export| I[(CSV Files)]
    I --> J[Python Analysis Layer]
    J --> K[Convergence Plot]
    J --> L[Probability Density Viz]