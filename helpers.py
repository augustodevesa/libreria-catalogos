#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Funciones auxiliares para manejar la librería de catálogos"""

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import with_statement
import os
import sys
import json
import pandas as pd
from pydatajson import DataJson


def nodes_to_csv(input_path, output_path):
    """Convierte el JSON de la red de nodos en un CSV."""
    df = nodes_to_df(input_path)
    df.to_csv(output_path, encoding="utf8", index=False)


def nodes_to_df(input_path):
    """Lee los catálogos de la red de nodos a un DataFrame."""

    with open(input_path) as f:
        nodes = json.load(f)

    rows = []
    for jurisdiction in nodes["jurisdictions"]:
        for catalog in jurisdiction["catalogs"]:
            print("Leyendo catálogo '{}' de la jurisdiccion '{}' ({})".format(
                catalog["id"], jurisdiction["id"], jurisdiction["title"]))
            dj = DataJson(catalog["url_json"])

            rows.append({
                "jurisdiction_id": jurisdiction["id"],
                "jurisdiction_title": jurisdiction["title"],
                "catalog_id": catalog["id"],
                "catalog_title": dj.get("title"),
                "catalog_homepage": dj.get("homepage"),
                "catalog_url_json": catalog["url_json"],
                "catalog_url_xlsx": catalog.get("url_xlsx"),
                "catalog_url_datosgobar": catalog.get("url_datosgobar")
            })

    fields = ["jurisdiction_id", "jurisdiction_title",
              "catalog_id", "catalog_title", "catalog_homepage",
              "catalog_url_json", "catalog_url_xlsx", "catalog_url_datosgobar"]

    return pd.DataFrame(rows)[fields]


def main():
    nodes_to_csv("nodes.json", "nodes.csv")


if __name__ == '__main__':
    main()
