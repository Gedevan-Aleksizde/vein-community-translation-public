from pathlib import Path

import pandas as pd

dir_text = Path("../text")

fp_text_jp = dir_text.joinpath("Game.locres.csv")
fp_text_en = dir_text.joinpath("demo003/Game.locres.csv")

fp_output = dir_text.joinpath("output.csv")


def main():
    df_en = pd.read_csv(fp_text_en)
    df_jp = pd.read_csv(fp_text_jp, header=None, escapechar="\\")
    df_jp.columns = ["key", "text_JP"]
    df = df_en.merge(df_jp, on=["key"], how="left")
    df = df.drop(columns=["Translation"]).rename(columns={"text_JP": "Translation"})
    df.to_csv(fp_output, index=False)


if __name__ == "__main__":
    main()
