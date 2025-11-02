#! /usr/bin/env python3
# reads English and another language CSVs, merges them, then writes it as a PO file for the each langauge.

from pathlib import Path

import polib
import warnings
from modules.pofile import po2pddf
import pandas as pd
from modules.pofile import pddf2po_crowdin
from typing import List

from modules.env import settings


version = settings.version

dp_input = settings.inputdir.joinpath(f"original/{version}")
dp_output = settings.inputdir.joinpath(f"merged/{version}")

fp_csv_en = dp_input.joinpath(f"en/Game.locres.csv")

def merge_locreses(fp_input_en: Path, fp_input: Path) -> pd.DataFrame:
    """
    input
    -------
        path, assuming input/<lang>/fromlocres/Game.locres.csv, with columns: key, source, Translation columns
    """
    lang = fp_input.parent.parent.name
    print(f"reading {lang} files: {fp_input}")
    df = pd.read_csv(fp_input)
    df_en = pd.read_csv(fp_input_en)

    count = count_dup(df, ["key"])
    if count > 0:
        warnings.warn(f"{lang} file has {count} key duplications")
    count_en = count_dup(df_en, ["key"])
    if count_en > 0:
        warnings.warn(f"English file has {count_en} key duplications")

    df_merged = df_en.drop(columns=["Translation"]).merge(df, on=["key", "source"], how="left").reset_index(drop=True).assign(index=lambda d: d.index, Translation=lambda d: d["Translation"].fillna(""))
    count_merged = count_dup(df_merged, ["key"])
    if count_merged > 0:
        warnings.warn(f"The merged file has {count_en} key duplications")
    
    if df_en.shape[0] != df_merged.shape[0]:
        warnings.warn(f"Inconsistent row numbers: Englishfile has {df_en.shape[0]} rows while {lang} file has {df.shape[0]} rows")
    
    return df_merged


def count_dup(data: pd.DataFrame, keys: List[str]) -> int:
    dup = data["key"].value_counts().reset_index().loc[lambda d: d["count"] != 1]
    return dup.shape[0]
    


def main():
    for fp_csv in dp_input.rglob("*.csv"):
        lang = fp_csv.parent.name
        fp_output = dp_output.joinpath(f"{lang}/vein0.po")
        if lang != "en":
            df_merged = merge_locreses(fp_csv_en, fp_csv)
            pof = pddf2po_crowdin(df_merged, locale=lang if lang != "jp" else None)
            if not fp_output.parent.exists():
                fp_output.parent.mkdir(parents=True)
            pof.save(fp_output)


if __name__ == "__main__":
    main()
