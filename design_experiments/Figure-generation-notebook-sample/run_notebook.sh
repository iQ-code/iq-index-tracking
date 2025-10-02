#!/bin/bash
# Script para ejecutar el notebook y generar los gráficos automáticamente

# Activar entorno virtual
source ../../venv/bin/activate

# Ejecutar notebook (los gráficos se generan con plt.savefig dentro del notebook)
echo "Ejecutando notebook y generando gráficos..."
jupyter nbconvert --to notebook --execute X-Figures-for-iQ-Index-Tracking-sales-all-included.ipynb --output executed_notebook.ipynb

echo "✓ Gráficos generados:"
echo "  - plot_portfolio_100.png"
echo "  - plot_portfolio_200.png"
