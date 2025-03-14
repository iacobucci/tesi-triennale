ecs_qb_t =  [0.026, 0.508, 0.990, 1.472, 1.953, 2.435, 2.917, 3.398, 3.880, 4.362, 4.844]
ecs_qb_q = [1, 38, 101, 30, 1, 4, 2, 2, 2, 8, 10, 3]

ecs_ar_t =  [ 0.030, 0.543, 1.056, 1.569, 2.083, 2.596, 3.109, 3.622, 4.135, 4.648, 5.161 ]
ecs_ar_q =  [1, 71, 86, 9, 4, 4, 7, 8, 3, 5, 2]

lf_qb_t = [ 0.040, 0.185, 0.329, 0.474, 0.618, 0.763, 0.907, 1.052, 1.196, 1.341, 1.485 ]
lf_qb_q = [ 1, 142, 8, 2, 3, 7, 17, 14, 3, 1, 2 ]

lf_ar_t = [ 0.043, 0.348, 0.653, 0.958, 1.263, 1.568, 1.873, 2.178, 2.483, 2.788, 3.093 ]
lf_ar_q =  [ 1, 149, 0, 0, 0, 0, 0, 0, 0, 18, 32 ]

lc_qb_t=  [ 0.048, 0.156, 0.264, 0.372, 0.480, 0.588, 0.697, 0.805, 0.913, 1.021, 1.129 ]
lc_qb_q =  [ 1, 138, 9, 0, 5, 8, 4, 5, 12, 15, 3 ]

lc_ar_t = [ 0.041, 0.127, 0.212, 0.298, 0.384, 0.469, 0.555, 0.641, 0.727, 0.812, 0.898 ]
lc_ar_q =  [ 1, 140, 8, 0, 10, 9, 13, 0, 1, 9, 9 ]

def avg_time(t, q):
	return sum([t[i] * q[i] for i in range(len(t))]) / sum(q)

print("Average time for ECS query builder: ", avg_time(ecs_qb_t, ecs_qb_q))
print("Average time for ECS active record: ", avg_time(ecs_ar_t, ecs_ar_q))
print("Average time for Lambda a freddo query builder: ", avg_time(lf_qb_t, lf_qb_q))
print("Average time for Lambda a freddo active record: ", avg_time(lf_ar_t, lf_ar_q))
print("Average time for Lambda a caldo query builder: ", avg_time(lc_qb_t, lc_qb_q))
print("Average time for Lambda a caldo active record: ", avg_time(lc_ar_t, lc_ar_q))

import numpy as np
import pandas as pd
import scipy.stats as stats

# Funzione per espandere gli array di tempo in base alle frequenze
def expand_data(times, quantities):
    expanded = []
    for t, q in zip(times, quantities):
        expanded.extend([t] * q)
    return np.array(expanded)

# Espansione dei dati
ecs_qb_expanded = expand_data(ecs_qb_t, ecs_qb_q)
ecs_ar_expanded = expand_data(ecs_ar_t, ecs_ar_q)
lf_qb_expanded = expand_data(lf_qb_t, lf_qb_q)
lf_ar_expanded = expand_data(lf_ar_t, lf_ar_q)
lc_qb_expanded = expand_data(lc_qb_t, lc_qb_q)
lc_ar_expanded = expand_data(lc_ar_t, lc_ar_q)

# Funzione per calcolare varie statistiche
def calculate_stats(data, name):
    if len(data) == 0:
        return f"No data for {name}"
    
    # Media (che hai già calcolato)
    mean = np.mean(data)
    
    # Mediana
    median = np.median(data)
    
    # Deviazione standard
    std_dev = np.std(data)
    
    # Percentili
    p25 = np.percentile(data, 25)  # 1° quartile
    p75 = np.percentile(data, 75)  # 3° quartile
    p90 = np.percentile(data, 90)  # 90° percentile
    p95 = np.percentile(data, 95)  # 95° percentile
    p99 = np.percentile(data, 99)  # 99° percentile
    
    # Moda
    mode = stats.mode(data, keepdims=False).mode
    
    # IQR (Intervallo interquartile)
    iqr = p75 - p25
    
    # Coefficiente di variazione
    cv = std_dev / mean if mean != 0 else float('nan')
    
    # Media geometrica
    geo_mean = stats.gmean(data) if all(d > 0 for d in data) else float('nan')
    
    # Media armonica
    harm_mean = stats.hmean(data) if all(d > 0 for d in data) else float('nan')
    
    print(f"\nStatistiche per {name}:")
    print(f"Media: {mean:.6f}")
    print(f"Mediana: {median:.6f}")
    print(f"Deviazione standard: {std_dev:.6f}")
    print(f"Coefficiente di variazione: {cv:.6f}")
    print(f"25° percentile (Q1): {p25:.6f}")
    print(f"75° percentile (Q3): {p75:.6f}")
    print(f"90° percentile: {p90:.6f}")
    print(f"95° percentile: {p95:.6f}")
    print(f"99° percentile: {p99:.6f}")
    print(f"Moda: {mode:.6f}")
    print(f"IQR: {iqr:.6f}")
    print(f"Media geometrica: {geo_mean:.6f}")
    print(f"Media armonica: {harm_mean:.6f}")
    
    return data

# Calcola statistiche per ciascun set di dati
calculate_stats(ecs_qb_expanded, "ECS Query Builder")
calculate_stats(ecs_ar_expanded, "ECS Active Record")
calculate_stats(lf_qb_expanded, "Lambda a freddo Query Builder")
calculate_stats(lf_ar_expanded, "Lambda a freddo Active Record")
calculate_stats(lc_qb_expanded, "Lambda a caldo Query Builder")
calculate_stats(lc_ar_expanded, "Lambda a caldo Active Record")

# Per visualizzare la distribuzione dei dati (opzionale)
import matplotlib.pyplot as plt

# Funzione per creare boxplot
def create_boxplots():
    data = [ecs_qb_expanded, ecs_ar_expanded, lf_qb_expanded, 
            lf_ar_expanded, lc_qb_expanded, lc_ar_expanded]
    labels = ['ECS QB', 'ECS AR', 'Lambda freddo QB', 
              'Lambda freddo AR', 'Lambda caldo QB', 'Lambda caldo AR']
    
    plt.figure(figsize=(12, 6))
    plt.boxplot(data, labels=labels)
    plt.title('Confronto dei tempi di esecuzione')
    plt.ylabel('Tempo (s)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Decommentare per visualizzare i boxplot
# create_boxplots()