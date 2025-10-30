from pathlib import Path

import polib

from modules.pofile import po2pddf

dp_text = Path("../text")

fp_output = dp_text.joinpath("out.csv")
fp_po = dp_text.joinpath("vein0.po")


def main():
    pof = polib.pofile(fp_po, encoding="utf-8")
    df = po2pddf(pof)
    print(df)
    df.to_csv(fp_output, index=False)


if __name__ == "__main__":
    main()
