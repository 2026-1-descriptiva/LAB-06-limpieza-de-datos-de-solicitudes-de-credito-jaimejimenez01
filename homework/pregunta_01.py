"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    import os
    import pandas as pd

    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";", index_col=0)

    # Eliminar filas con valores nulos
    df = df.dropna()

    # Normalizar columnas de texto: quitar espacios y convertir a minúsculas
    text_cols = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "línea_credito"]
    for col in text_cols:
        df[col] = df[col].str.strip().str.lower()

    # Reemplazar guiones bajos y guiones medios por espacios en idea_negocio y barrio
    for col in ["idea_negocio", "barrio"]:
        df[col] = (
            df[col]
            .str.replace("_", " ", regex=False)
            .str.replace("-", " ", regex=False)
            .str.strip()
        )

    # Normalizar fecha_de_beneficio: pasar de yyyy/mm/dd a dd/mm/yyyy
    def normalize_date(date_str):
        parts = date_str.strip().split("/")
        if len(parts[0]) == 4:  # formato yyyy/mm/dd
            return f"{parts[2]}/{parts[1]}/{parts[0]}"
        return date_str.strip()

    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(normalize_date)

    # Limpiar monto_del_credito: quitar símbolo "$", comas y ".00", convertir a int
    df["monto_del_credito"] = (
        df["monto_del_credito"]
        .astype(str)
        .str.strip()
        .str.replace("$ ", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace(".00", "", regex=False)
        .astype(int)
    )

    # Eliminar filas duplicadas
    df = df.drop_duplicates()

    # Escribir archivo de salida
    os.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)
