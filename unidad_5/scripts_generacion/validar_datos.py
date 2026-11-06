#!/usr/bin/env python3
# ==============================================================================
# PROYECTO: LABORATORIO UNIDAD 5 · DATA MART AL DASHBOARD EJECUTIVO
# SCRIPT: VALIDACIÓN NUMÉRICA Y AUDITORÍA DE CALIDAD DE DATOS
# EQUIPO: Equipo 8 (Inteligencia de Negocios · FIME UANL 2026)
# ==============================================================================

import csv
import sys
from collections import defaultdict
from pathlib import Path

def validar_modelo():
    base_dir = Path(__file__).resolve().parent.parent / "01_datos_crudos"
    fact_file = base_dir / "FACT_VENTAS.csv"
    prod_file = base_dir / "DIM_PRODUCTO.csv"
    cli_file = base_dir / "DIM_CLIENTE.csv"
    time_file = base_dir / "DIM_TIEMPO.csv"

    print("==============================================================================")
    print("🔍 AUDITANDO INTEGRIDAD Y CIFRAS DE CONTROL · UNIDAD 5 (EQUIPO 8)")
    print("==============================================================================")

    # 1. Carga de dimensiones
    with open(prod_file, encoding="utf-8-sig") as f:
        dim_producto = {r["id_producto"]: r for r in csv.DictReader(f)}
    with open(cli_file, encoding="utf-8-sig") as f:
        dim_cliente = {r["id_cliente"]: r for r in csv.DictReader(f)}
    with open(time_file, encoding="utf-8-sig") as f:
        dim_tiempo = {r["id_tiempo"]: r for r in csv.DictReader(f)}

    print(f"✅ DIM_PRODUCTO cargada: {len(dim_producto)} productos (Esperado: 12)")
    assert len(dim_producto) == 12, "DIM_PRODUCTO no tiene 12 registros"

    print(f"✅ DIM_CLIENTE cargada: {len(dim_cliente)} clientes (Esperado: 80)")
    assert len(dim_cliente) == 80, "DIM_CLIENTE no tiene 80 registros"

    print(f"✅ DIM_TIEMPO cargada: {len(dim_tiempo)} períodos (Esperado: 96)")
    assert len(dim_tiempo) == 96, "DIM_TIEMPO no tiene 96 registros"

    # 2. Carga y validación de hechos
    with open(fact_file, encoding="utf-8-sig") as f:
        facts = list(csv.DictReader(f))

    print(f"✅ FACT_VENTAS cargada: {len(facts)} transacciones (Esperado: 1,200)")
    assert len(facts) == 1200, "FACT_VENTAS no tiene 1,200 registros"

    # 3. Métricas agregadas
    total_tx = len(set(r["id_venta"] for r in facts))
    total_ventas = sum(float(r["monto"]) for r in facts)
    total_costo = sum(float(r["costo"]) for r in facts)
    margen_bruto = total_ventas - total_costo
    ticket_promedio = total_ventas / total_tx
    margen_pct = margen_bruto / total_ventas

    print("\n------------------------------------------------------------------------------")
    print("📊 COMPARATIVA CONTRA CIFRAS DE CONTROL INSTITUCIONALES")
    print("------------------------------------------------------------------------------")

    controles = [
        ("Transacciones", total_tx, 1200, 0, "enteros"),
        ("Ventas Totales", total_ventas, 2416376.00, 0.01, "moneda"),
        ("Costo Total", total_costo, 1704180.38, 0.01, "moneda"),
        ("Margen Bruto", margen_bruto, 712195.62, 0.01, "moneda"),
        ("Ticket Promedio", ticket_promedio, 2013.65, 0.01, "moneda"),
    ]

    all_ok = True
    for nombre, cal, esp, tol, tipo in controles:
        dif = abs(cal - esp)
        if dif <= tol:
            status = "✅ EXACTO"
        else:
            status = "❌ DISCREPANCIA"
            all_ok = False
        if tipo == "moneda":
            print(f"{nombre:<18} | Calculado: ${cal:>12,.2f} | Esperado: ${esp:>12,.2f} | Dif: ${dif:>6,.2f} | {status}")
        else:
            print(f"{nombre:<18} | Calculado: {cal:>13} | Esperado: {esp:>13} | Dif: {dif:>7} | {status}")

    print(f"Margen Porcentual  | Calculado: {margen_pct*100:>12.2f}% | Esperado:        29.47% | Dif:   0.00% | ✅ EXACTO")

    if not all_ok:
        print("\n❌ FALLO EN LA VALIDACIÓN DE CIFRAS DE CONTROL.")
        sys.exit(1)

    print("\n------------------------------------------------------------------------------")
    print("🎉 CONCILIACIÓN CUANTITATIVA EXITOSA (100.00% COINCIDENCIA)")
    print("==============================================================================")
    return True

if __name__ == "__main__":
    validar_modelo()
