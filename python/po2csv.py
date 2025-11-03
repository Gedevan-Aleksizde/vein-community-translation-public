#! /usr/bin/env python3
# currently needs to export as TXT. why so ineffient design?

from pathlib import Path

import polib
import warnings
from modules.pofile import po2pddf
from modules.env import settings
from modules.ue4loctool import write_as_text_ue4loctool

dp_input = settings.inputdir.joinpath("from-crowdin")
dp_output = settings.inputdir.joinpath("from-crowdin-csv")
dp_output_locres = settings.inputdir.joinpath("to-locres")


def convertpo2csv(fp: Path) -> bool:
    lang = fp.parent.name
    if lang != "en":
        fp_output = dp_output.joinpath(f"{settings.version}/{lang}/vein0.csv")
        fp_output_locres = dp_output_locres.joinpath(f"{lang}/Game.locres.txt")
        print(f"reading {lang} files: {fp}, trying to output to {fp_output.resolve()}")
        pof = polib.pofile(fp, encoding="utf-8")
        df = po2pddf(pof)
        if not fp_output.parent.exists():
            fp_output.parent.mkdir(parents=True)
        if not fp_output_locres.exists():
            fp_output_locres.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(fp_output, index=False)
        write_as_text_ue4loctool(df, fp_output_locres)
        return True
    else:
        print("English files skipped")
        return True

def main():
    for fp_po in dp_input.rglob("*.po"):
        convertpo2csv(fp_po)


if __name__ == "__main__":
    main()
