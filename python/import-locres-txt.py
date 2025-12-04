#! /usr/bin/env python3
# reads English and another language CSVs, merges them, then writes it as a PO file for the each langauge.
# due to the UE4loctool's issue, we need to implement a method that read from plain TXT file...

import warnings
from pathlib import Path
from typing import List

import pandas as pd
from modules.env import settings
from modules.pofile import pddf2po_crowdin

version = settings.version

dp_input = settings.inputdir.joinpath(f"original-txt/{version}")
dp_output = settings.inputdir.joinpath(f"original-po/{version}")

fp_txt_en = dp_input.joinpath("en/Game.locres.txt")


def merge_locreses(data_en: pd.DataFrame, data_lang: pd.DataFrame) -> pd.DataFrame:
    """
    input
    -------
        data_en should have key and source columns
        data_lang should have key and Translation columns
    """

    count = count_dup(data_lang, ["key"])
    if count > 0:
        warnings.warn(f"The tranlsation file has {count} key duplications")
    count_en = count_dup(data_en, ["key"])
    if count_en > 0:
        warnings.warn(f"English file has {count_en} key duplications")

    if count != count_en:
        warnings.warn(
            f"Inconsistent row numbers: The English file has {count_en} rows while the transl. file has {count} rows"
        )

    data_en["Translation"] = data_lang["Translation"]
    data_en = data_en.fillna("")
    return data_en


def count_dup(data: pd.DataFrame, keys: List[str]) -> int:
    dup = data["key"].value_counts().reset_index().loc[lambda d: d["count"] != 1]
    return dup.shape[0]


def read_txt(fp: Path) -> pd.DataFrame:
    txt = [l.rstrip() for l in fp.open("r", encoding="utf-8")]  # ¯\_(ツ)_/¯
    d_plain = pd.DataFrame({"raw": txt})
    d_plain.columns = ["raw"]
    d_plain["key"] = d_plain["raw"].str.extract("(^.+?)=")
    d_plain["text"] = d_plain["raw"].str.extract("^.+?=(.+)$")
    d_plain = d_plain.drop(columns=["raw"])
    return d_plain


def main():
    print(f"reading English file: {fp_txt_en}")
    df_en = read_txt(fp_txt_en).rename(columns={"text": "source"})

    for fp_txt in dp_input.rglob("*.txt"):
        lang = fp_txt.parent.name
        fp_output = dp_output.joinpath(f"{lang}/vein0.po")
        if lang != "en":
            print(f"reading {lang} files: {fp_txt.resolve()}")
            df_lang = read_txt(fp_txt).rename(columns={"text": "Translation"})
            df_merged = merge_locreses(df_en, df_lang)
            df_merged["index"] = [f"{x:06}" for x in range(df_merged.shape[0])]
            df_merged["approved"] = True
            pof = pddf2po_crowdin(df_merged, locale=lang if lang != "jp" else None)
            if not fp_output.parent.exists():
                fp_output.parent.mkdir(parents=True)
            pof.save(fp_output)

    df_en["Translation"] = ""
    df_en["index"] = [f"{x:06}" for x in range(df_merged.shape[0])]
    pof = pddf2po_crowdin(df_en, locale="en_US")
    fp_output_en = dp_output.joinpath("en/vein0.po")
    if not fp_output_en.parent.exists():
        fp_output_en.parent.mkdir(parents=True)
    print(
        f"{fp_output_en.resolve()} is the output English file (translation master file)."
    )
    pof.save(fp_output_en)


if __name__ == "__main__":
    main()
