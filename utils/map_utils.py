import json
import numpy as np


def aplicar_filtro(gdf, metrica, modo_analise):
    """
    metrica:      "Internações" | "Ambulatórios" | "Ambos"
    modo_analise: "Números Absolutos" | "Taxa / 100k hab." | "Ambos"
    """
    gdf_filtrado = gdf.copy()
    usar_taxa = modo_analise == "Taxa / 100k hab."

    if metrica == "Internações":
        col = "taxa_internacoes" if usar_taxa else "nu_ocorrencias_internacoes"
        gdf_filtrado["valor"] = gdf_filtrado[col].fillna(0)
    elif metrica == "Ambulatórios":
        col = "taxa_ambulatorio" if usar_taxa else "nu_ocorrencias_ambulatorio"
        gdf_filtrado["valor"] = gdf_filtrado[col].fillna(0)
    else:  # Ambos — usa taxa se qualquer modo que não seja absoluto puro
        if modo_analise == "Números Absolutos":
            gdf_filtrado["valor"] = (
                gdf_filtrado["nu_ocorrencias_internacoes"].fillna(0)
                + gdf_filtrado["nu_ocorrencias_ambulatorio"].fillna(0)
            )
        else:
            gdf_filtrado["valor"] = (
                gdf_filtrado["taxa_internacoes"].fillna(0)
                + gdf_filtrado["taxa_ambulatorio"].fillna(0)
            )

    return gdf_filtrado


def calcular_view(gdf, municipio_destaque=None):
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