from datetime import datetime
from pathlib import Path
import shutil
import pandas as pd
import numpy as np
from modules.pofile import pddf2po_crowdin
import json


def get_latest_dir_name(dp: Path):
    l = list(dp.glob("*"))
    sorted(l)
    return l[-1].name

dp_work = Path(__file__).parent



dp_text = Path("../text")
dp_crowdin = dp_text.joinpath("crowdin")
dp_bak = dp_text.joinpath("bak")

settings = json.load(dp_work.joinpath("settings.json").open("r", encoding="utf-8"))
version = settings["version"]

fp_text_original = (
    dp_text.joinpath(f"original/{version}/Game.locres.csv")
)
fp_text_jp = dp_text.joinpath("Game.locres.csv")

fp_output = dp_text.joinpath("Game.locres.csv")
fp_po = dp_text.joinpath(f"vein-{version}.po")

def main():
    print(f"original: {fp_text_original}")
    print(f"previous translation: {fp_text_jp}")
    dt_bak  = datetime.now().strftime("%Y%m%d-%H%M")
    df_en = (
        pd.read_csv(fp_text_original, keep_default_na=False)
        .reset_index()
        .assign(index=lambda d: d["index"].astype(str).str.zfill(5))
        .drop(columns=["Translation"], errors="ignore")
    )
    df_jp = (
        pd.read_csv(fp_text_jp, keep_default_na=False)
        .drop(columns=["index"], errors="ignore")
    )
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
    df_jp.to_csv(
        dp_bak.joinpath(
            f"Game.locres-{dt_bak}.csv"
        )
    )
    df = df_en.merge(df_jp, on=["key", "source"], how="left")
    df = df.sort_values(["index"])
    df.assign(Translation=lambda d: d["Translation"].fillna("")).assign(Translation=lambda d: np.where(d["Translation"] == d["source"], "", d["Translation"])).rename(columns={"key": "string ID", "source": "source Text", "index": "label"}).to_csv(dp_crowdin.joinpath("vein0.csv"), index=False)
    df = df.assign(Translation=lambda d: np.where((d["Translation"].isna()) | (d["Translation"]==""), d["source"], d["Translation"]))
    if not "approved" in df.columns:
        df["approved"] = False
    print(df)
    pof = pddf2po_crowdin(df)
    if fp_po.exists():
        shutil.copy(fp_po, dp_bak.joinpath(f"vein-{dt_bak}.po")) 
    pof.save(fp_po)
    df.to_csv(fp_output, index=False)


if __name__ == "__main__":
    main()
