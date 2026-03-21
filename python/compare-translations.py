# %%
from pathlib import Path

import numpy as np
import pandas as pd
import polib
from modules.env import settings
from modules.pofile import po2pddf

version = settings.version

LANG = "ja"

dp_text = Path(__file__).parent.parent.joinpath(settings.inputdir)
dp_crowdin = dp_text.joinpath("from-crowdin")
fp_out = dp_text.joinpath("comparison.csv")

# fp_text_original = dp_text.joinpath(f"original-po/{version}/en/vein0.po")
fp_po_original = dp_text.joinpath(f"original-po/{version}/{LANG}/vein0.po")
fp_po_jp = dp_crowdin.joinpath(f"{LANG}/vein0.po")
# %%
df_text_original = po2pddf(polib.pofile(fp_po_original, encoding="utf-8"))
df_text = po2pddf(polib.pofile(fp_po_jp, encoding="utf-8")).assign(
    Translation=lambda d: np.where(
        d["Translation"].fillna("") == "", d["source"], d["Translation"]
    )
)
# %%
df_comparison = (
    df_text_original.rename(columns={"Translation": "text_official"})
    .merge(
        df_text.rename(columns={"Translation": "text_correct"}),
        on=["key", "source"],
        how="outer",
    )
    .drop(columns=["index_x", "index_y"])
    .rename(columns={"source": "English"})
)
# %%
print(f"writing to {fp_out.resolve()}")

pd.concat(
    (
        df_comparison.loc[
            lambda d: (d["key"].str.contains("^Items::BP.+_Name$", regex=True))
        ].assign(category="アイテム"),
        df_comparison.loc[
            lambda d: (d["key"].str.contains("^Furniture::.+_Name$", regex=True))
        ].assign(category="家具"),
        df_comparison.loc[
            lambda d: (d["key"].str.contains("^StatPerks::.+_Name$", regex=True))
        ].assign(category="パークスキル"),
    )
)[["category", "English", "text_official", "text_correct"]].rename(
    columns={
        "English": "原文",
        "text_official": "非公式訳",
        "text_correct": "非公式訳",
        "category": "分類",
    }
).to_csv(
    fp_out, index=False
)
# %%
