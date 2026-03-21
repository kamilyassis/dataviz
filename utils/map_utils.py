import json
import numpy as np

def aplicar_filtro(gdf, estado, metrica, modo_analise):
    gdf_filtrado = gdf.copy()
    if estado != "Todos":
        gdf_filtrado = gdf_filtrado[gdf_filtrado["uf"] == estado].copy()

    prefixo = "taxa_" if "Taxa" in modo_analise else "nu_ocorrencias_"

    if metrica == "Internações":
        gdf_filtrado["valor"] = gdf_filtrado[f"{prefixo}internacoes"].fillna(0)
        escala = "Reds"
    elif metrica == "Ambulatórios":
        gdf_filtrado["valor"] = gdf_filtrado[f"{prefixo}ambulatorio"].fillna(0)
        escala = "Blues"
    else:
        gdf_filtrado["valor"] = (
            gdf_filtrado[f"{prefixo}internacoes"].fillna(0)
            + gdf_filtrado[f"{prefixo}ambulatorio"].fillna(0)
        )
        escala = "Purples"

    return gdf_filtrado, escala


def calcular_view(gdf, municipio_destaque=None):
    """Retorna view_state. Sem município → visão geral do Brasil."""
    if not municipio_destaque:
        return {"latitude": -14.2, "longitude": -51.9, "zoom": 3.8, "pitch": 45, "bearing": -10}

    row = gdf[gdf["no_municipio"] == municipio_destaque]
    if row.empty:
        return calcular_view(gdf, None)

    minx, miny, maxx, maxy = row.geometry.iloc[0].bounds
    delta = max(maxx - minx, maxy - miny) * 1.25
    zoom = float(np.clip(np.log2(8 / delta) + 4, 5.5, 11))
    return {
        "latitude": (miny + maxy) / 2,
        "longitude": (minx + maxx) / 2,
        "zoom": zoom,
        "pitch": 45,
        "bearing": -10,
    }


def preparar_geojson(gdf, coluna_valor, municipio_destaque=None):
    """Prepara GeoJSON com elevation e cores calculadas."""
    gdf = gdf.copy()
    vmax = gdf[coluna_valor].quantile(0.95) or 1
    ratio = (gdf[coluna_valor] / vmax).clip(0, 1)

    gdf["elevation"] = ratio * 80000
    gdf["cor_r"] = (ratio * 220 + 35).astype(int)
    gdf["cor_g"] = ((1 - ratio) * 130).astype(int)
    gdf["cor_b"] = ((1 - ratio) * 200 + 55).astype(int)
    gdf["alpha"] = 200

    if municipio_destaque:
        mask = gdf["no_municipio"] == municipio_destaque
        gdf.loc[mask, ["cor_r", "cor_g", "cor_b", "alpha"]] = [255, 200, 0, 255]
        gdf.loc[mask, "elevation"] *= 1.3

    return json.loads(gdf.to_json())