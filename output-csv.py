from pathlib import Path

import polib

from modules.pofile import po2pddf

dir_text = Path("../text")


fp_output = dir_text.joinpath("out.csv")
fp_po = dir_text.joinpath("vein.po")


def main():
    pof = polib.pofile(fp_po, encoding="utf-8")
    df = po2pddf(pof)
    df.to_csv(fp_output, index=False)


if __name__ == "__main__":
    main()
