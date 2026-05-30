from pathlib import Path

import pandas as pd
import polib
from modules.env import settings
from modules.pofile import pddf2po_crowdin, po2pddf


def update_txt(data_base: pd.DataFrame, data_comp: pd.DataFrame) -> pd.DataFrame:
    df = data_base.merge(
        data_comp[["key", "source", "Translation"]], on=["key", "source"], how="left"
    )
    df["Translation"] = (
        df["Translation_x"]
        .case_when(
            [
                (
                    df["Translation_x"] == "",
                    df["Translation_y"],
                ),
                (df["Translation_x"] == df["Translation_x"], df["Translation_x"]),
            ]
        )
        .fillna("")
    )
    df["approved"] = True
    return df


def main(fp_base: Path, fp_comp: Path, fp_out: Path):
    print(f"reading {fp_base} as the base file")
    po_base = polib.pofile(fp_base, encoding="utf-8")
    data_base = po2pddf(po_base)
    print(f"reading {fp_comp} as the comparing file")
    po_comp = polib.pofile(fp_comp, encoding="utf-8")
    data_comp = po2pddf(po_comp)

    print(data_base)
    print(data_comp)

    df_updated = update_txt(data_base, data_comp)
    pof = pddf2po_crowdin(df_updated)
    pof.save(fp_out)


if __name__ == "__main__":
    lang = "ja"
    fp_base = (
        settings.inputdir.joinpath("original-po")
        .joinpath(settings.version)
        .joinpath("en")
        .joinpath("vein0.po")
    )
    fp_comp = (
        settings.inputdir.joinpath("from-crowdin").joinpath(lang).joinpath("vein0.po")
    )
    fp_out = settings.inputdir.joinpath("tmp-vein0.po")
    main(fp_base, fp_comp, fp_out)
