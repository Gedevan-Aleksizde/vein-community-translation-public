from datetime import datetime
from pathlib import Path

import pandas as pd

from .modules.pofile import pddf2po

dir_text = Path("../text")


def get_latest_dir_name(dp: Path):
    l = list(dp.glob("*"))
    sorted(l)
    return l[-1].name


fp_text_original = dir_text.joinpath(
    get_latest_dir_name(dir_text.joinpath("original"))
).joinpath("Game.locres.csv")
fp_text_jp = dir_text.joinpath("Game.locres.csv")

fp_output = dir_text.joinpath("Game.locres.csv")
fp_po = dir_text.joinpath("vein.po")


def main():
    df_en = pd.read_csv(fp_text_original).reset_index()
    df_jp = pd.read_csv(fp_text_jp)
    if df_en.shape[0] != df_jp.shape[0]:
        print(f"inconsistent row numbers en={df_en.shape[0]}, jp={df_jp.shape[0]}")
    dup_en = df_en["key"].value_counts().reset_index().loc[lambda d: d["count"] != 1]
    dup_jp = df_jp["key"].value_counts().reset_index().loc[lambda d: d["count"] != 1]
    if dup_en.shape[0] > 0:
        print(f"duplications in the original: {list(dup_en["key"])}")
    if dup_jp.shape[0] > 0:
        print(f"duplications in the previous translation: {list(dup_jp["key"])}")
    df_jp.to_csv(
        dir_text.joinpath(
            f"bak/Game.locres-{datetime.now().strftime("%Y%m%d-%H%M")}.csv"
        )
    )
    df = df_en.merge(df_jp, on=["key"], how="left")
    df = (
        df.drop(columns=["Translation"])
        .rename(columns={"text_JP": "Translation"})
        .sort_values(["index"])
    )
    pof = pddf2po(df)
    pof.save(fp_po)
    df.to_csv(fp_output, index=False)


if __name__ == "__main__":
    main()
