import pandas as pd
import numpy as np
from pathlib import Path

def write_as_text_ue4loctool(data: pd.DataFrame, fp_output: Path, file_encoding="utf-8", col_key:str="key", col_source:str="source", col_translation:str="Translation") -> bool:
    df_text = pd.DataFrame({"col": np.where((data[col_translation].isna()) | (data[col_translation] == ""), data[col_source], data[col_translation])})  # needed?
    df_text["col"] = data[col_key] + "=" + data[col_translation]
    df_text["col"] = df_text["col"].str.replace("\n", " ", regex=True)
    fp_output.open("w", encoding=file_encoding).writelines([x + "\n" for x in df_text["col"].values.tolist()])  # bluh they want to force us to use a for loop?