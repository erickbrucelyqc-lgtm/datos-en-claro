"""Insight Lab: an independent example built with Streamlit."""

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


def prepare_data(source):
    data = pd.read_csv(source)
    required = {"date", "category", "amount"}
    if not required.issubset(data.columns):
        raise ValueError("El CSV necesita las columnas date, category y amount.")
    if data.empty:
        raise ValueError("El CSV no contiene registros.")
    data = data.loc[:, ["date", "category", "amount"]].copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce", utc=True)
    data["amount"] = pd.to_numeric(data["amount"], errors="coerce")
    data["category"] = data["category"].astype("string").str.strip()
    valid = (
        data["date"].notna()
        & np.isfinite(data["amount"])
        & data["category"].notna()
        & data["category"].ne("")
    )
    rejected = int((~valid).sum())
    clean = data.loc[valid].copy()
    if clean.empty:
        raise ValueError("No hay filas válidas. Revisa fechas, categorías e importes.")
    return clean, rejected


def main():
    st.set_page_config(
        page_title="Insight Lab | Erick Quio", page_icon="📊", layout="wide"
    )
    st.caption("ERICK QUIO / DATA LAB / DEMO CON DATOS SINTÉTICOS")
    st.title("De datos a decisiones.")
    st.write(
        "Carga un CSV, filtra categorías y descubre cómo se distribuyen los importes."
    )
    upload = st.sidebar.file_uploader("CSV: date, category, amount", type="csv")
    source = (
        upload if upload is not None else Path(__file__).with_name("erick_sample.csv")
    )
    try:
        data, rejected = prepare_data(source)
    except (ValueError, OSError, UnicodeError, pd.errors.ParserError) as exc:
        st.error(str(exc))
        st.stop()
    if rejected:
        st.warning(f"Se omitieron {rejected} filas con datos inválidos.")
    categories = sorted(data["category"].unique())
    selected = st.sidebar.multiselect("Categorías", categories, default=categories)
    filtered = data[data["category"].isin(selected)]
    if filtered.empty:
        st.info("Selecciona al menos una categoría para mostrar resultados.")
        st.stop()
    first, second, third = st.columns(3)
    first.metric("Importe total (USD)", f"${filtered['amount'].sum():,.2f}")
    second.metric("Registros", len(filtered))
    third.metric("Promedio por registro", f"${filtered['amount'].mean():,.2f}")
    left, right = st.columns(2)
    with left:
        st.subheader("Distribución por categoría")
        st.bar_chart(filtered.groupby("category")["amount"].sum(), color="#22D3EE")
    with right:
        st.subheader("Evolución diaria")
        daily = filtered.set_index("date")["amount"].resample("D").sum()
        st.line_chart(daily, color="#A78BFA")
    st.dataframe(filtered, hide_index=True)
    st.download_button(
        "Descargar selección",
        filtered.to_csv(index=False).encode("utf-8"),
        "insight-selection.csv",
        "text/csv",
    )
    st.caption(
        "Ejemplo independiente sobre Streamlit. No modifica el motor de la biblioteca."
    )


if __name__ == "__main__":
    main()
