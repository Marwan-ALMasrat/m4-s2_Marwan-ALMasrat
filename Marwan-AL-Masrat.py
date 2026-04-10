import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sqlalchemy import create_engine
from brokenaxes import brokenaxes

def connect_db():
    engine = create_engine(
        "postgresql+psycopg://postgres:postgres@localhost:5433/amman_market"
    )
    return engine

# ── Data Extraction & Cleaning ────────────────────────────
def extract_data(engine):
    customers = pd.read_sql("SELECT * FROM customers", engine)
    products = pd.read_sql("SELECT * FROM products", engine)
    orders = pd.read_sql("SELECT * FROM orders WHERE status != 'cancelled'", engine)
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    order_items = pd.read_sql("SELECT * FROM order_items WHERE quantity <= 100", engine)
    
    return {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items
    }







# KPI 1: Monthly Revenue (Original)
plt.figure(figsize=(12,5))
x = [str(p) for p in kpi_results['monthly_revenue'].index]
y = kpi_results['monthly_revenue'].values
plt.plot(x,y,marker='o',color=COLORS[0])
plt.fill_between(x,y,alpha=0.1,color=COLORS[0])
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (JOD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/kpi1_monthly_revenue.png",dpi=150)
plt.close()





# KPI 1: Monthly Revenue (Combo Chart - Optimized for Publication)
plt.figure(figsize=(14, 6)) 

x = [str(p) for p in kpi_results['monthly_revenue'].index]
y = kpi_results['monthly_revenue'].values

plt.bar(x, y, color=COLORS[0], alpha=0.3, label='Monthly Volume', zorder=2)
plt.plot(x, y, marker='o', color=COLORS[0], linewidth=3, markersize=8, label='Revenue Trend', zorder=3)
plt.fill_between(x, y, alpha=0.05, color=COLORS[0], zorder=1)

ymax, ymin = max(y), min(y)
xpos_max, xpos_min = x[list(y).index(ymax)], x[list(y).index(ymin)]

plt.annotate(f'Peak: {ymax:,.0f} JOD', xy=(xpos_max, ymax), xytext=(0, 12),
             textcoords='offset points', ha='center', fontweight='bold', color='green')
plt.annotate(f'Low: {ymin:,.0f} JOD', xy=(xpos_min, ymin), xytext=(0, -20),
             textcoords='offset points', ha='center', fontweight='bold', color='red')

avg_revenue = sum(y) / len(y)
plt.axhline(avg_revenue, color='gray', linestyle='--', alpha=0.6, label=f'Avg: {avg_revenue:,.0f}', zorder=4)

plt.title("Monthly Revenue Performance & Trend (JOD)", fontsize=14, pad=20)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Revenue (JOD)", fontsize=12)
plt.xticks(rotation=90) 
plt.grid(axis='y', linestyle=':', alpha=0.4, zorder=0)
plt.legend(loc='upper left')

plt.tight_layout()
plt.savefig("output/kpi1_monthly_revenue_combo.png",dpi=150, bbox_inches='tight') 
plt.show()


