#! /usr/bin/env python3
# merges a previous PO file with the latest CSV file exported from locres files.
# now outdated. don't have to use.

import shutil
from datetime import datetime

import numpy as np
from modules.env import settings
from modules.pofile import pddf2po_crowdin, po2pddf

version = settings.version

import polib

dp_text = settings.inputdir
dp_crowdin = dp_text.joinpath("from-crowdin")
dp_bak = dp_text.joinpath("bak")


# fp_text_original = dp_text.joinpath(f"original-po/{version}/en/vein0.po")
fp_po_original = dp_text.joinpath(f"original-po/{version}/en/vein0.po")
fp_text_jp = dp_text.joinpath("Game.locres.csv")
fp_po_jp = dp_crowdin.joinpath("jp/vein0.po")

fp_output = dp_text.joinpath("Game.locres.csv")
fp_po_output = dp_text.joinpath("vein0.po")


def main():
    print(f"original: {fp_po_original}")
    print(f"previous translation: {fp_po_jp}")
    if not fp_po_original.exists():
        raise FileNotFoundError("アホ死ね")
    if not fp_po_jp.exists():
        raise FileNotFoundError("アホ死ね2")
    dt_bak = datetime.now().strftime("%Y%m%d-%H%M")
    df_en = po2pddf(polib.pofile(fp_po_original, encoding="utf-8")).drop(
        columns=["Translation"]
    )
    df_jp = po2pddf(polib.pofile(fp_po_jp, encoding="utf-8")).drop(columns=["index"])
    for dp in [dp_text, dp_crowdin, dp_bak]:
        if not dp.exists():
            dp.mkdir(parents=True)

    if df_en.shape[0] != df_jp.shape[0]:
        print(f"inconsistent row numbers en={df_en.shape[0]}, jp={df_jp.shape[0]}")
    dup_en = df_en["key"].value_counts().reset_index().loc[lambda d: d["count"] != 1]
    dup_jp = df_jp["key"].value_counts().reset_index().loc[lambda d: d["count"] != 1]
    if dup_en.shape[0] > 0:
        print(f"duplications in the original: {list(dup_en["key"])}")
    if dup_jp.shape[0] > 0:
        print(f"duplications in the previous translation: {list(dup_jp["key"])}")
    df_jp.to_csv(dp_bak.joinpath(f"Game.locres-{dt_bak}.csv"))
    df = df_en.merge(df_jp, on=["key", "source"], how="left")
    df = df.sort_values(["index"])
    df.assign(Translation=lambda d: d["Translation"].fillna("")).assign(
        Translation=lambda d: np.where(
            d["Translation"] == d["source"], "", d["Translation"]
        )
    ).rename(
        columns={"key": "string ID", "source": "source Text", "index": "label"}
    ).to_csv(
        dp_crowdin.joinpath("vein0.csv"), index=False
    )
    df = df.assign(
        Translation=lambda d: np.where(
            (d["Translation"].isna()) | (d["Translation"] == ""),
            d["source"],
            d["Translation"],
        )
    )
    if "approved" not in df.columns:
        df["approved"] = False
    print(df)
    pof = pddf2po_crowdin(df)
    if fp_po_output.exists():
        shutil.copy(fp_po_output, dp_bak.joinpath(f"vein-{dt_bak}.po"))
    pof.save(fp_po_output)
    df.to_csv(fp_output, index=False)


if __name__ == "__main__":
    main()
