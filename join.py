#!/usr/bin/env python3
"""Recolle les parties et vérifie le SHA-256 du fichier d'origine.
Usage : python join.py [nom_du_fichier_de_sortie]
À lancer dans le dossier qui contient les parties, manifest.json et ce script."""
import hashlib, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "manifest.json"), encoding="utf-8") as f:
    m = json.load(f)
out = sys.argv[1] if len(sys.argv) > 1 else m["original_name"]
h = hashlib.sha256()
with open(out, "wb") as dst:
    for part in m["parts"]:
        with open(os.path.join(here, part["name"]), "rb") as src:
            while chunk := src.read(8 * 1024 * 1024):
                dst.write(chunk)
                h.update(chunk)
ok = h.hexdigest() == m["sha256"]
print("Fichier reconstruit :", out)
print("Vérification SHA-256 :", "OK" if ok else "ERREUR, fichier corrompu")
