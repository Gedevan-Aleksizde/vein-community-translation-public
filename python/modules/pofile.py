from datetime import datetime, timezone
from typing import Optional

import pandas as pd
import polib


def pddf2po(
    data: pd.DataFrame,
    locale: str = None,
    col_key: str = "key",
    col_source: str = "source",
    col_transl: str = "Translation",
    col_index: str = "index",
) -> polib.POFile:
    """
    UE4localizationsTool の制約のため, id を index + source として, key をコメントにする
    """
    if locale is None:
        locale = "ja_JP"
    pof = initializePOFile(lang="ja_JP")
    for _, r in data.iterrows():
        pof.append(
            polib.POEntry(
                msgid=str(r[col_index]) + "/" + r[col_source],
                msgstr=str(r[col_transl]),
                tcomment=str(r[col_key]),
            )
        )
    return pof


def pddf2po_crowdin(
    data: pd.DataFrame,
    locale: str = None,
    col_key: str = "key",
    col_source: str = "source",
    col_transl: str = "Translation",
    col_approved: str = "approved",
    col_index: str = "index",
) -> polib.POFile:
    """
    key will be set to msgctxt (context)
    """
    if locale is None:
        locale = "ja_JP"
    pof = initializePOFile(lang="ja_JP")
    for _, r in data.iterrows():
        pof.append(
            polib.POEntry(
                msgid=str(r[col_source]),
                msgstr=(
                    str(r[col_transl])
                    if (r[col_source] != r[col_transl]) or r[col_approved]
                    else ""
                ),  # FIXME
                msgctxt=str(r[col_key]),
                tcomment=str(r[col_index]),
            )
        )
    return pof


def initializePOFile(
    lang: str, encoding: str = "utf-8", email: Optional[str] = None
) -> polib.POFile:
    po = polib.POFile(encoding=encoding)
    dt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S%z")
    metadata = {
        "Project-Id-Version": "1.0",
        "POT-Creation-Date": dt,
        "PO-Revision-Date": dt,
        "MIME-Version": "1.0",
        "Language": lang,
        "Content-Type": "text/plain; charset=utf-8",
        "Plural-Forms": "nplurals=1; plural=0;",
        "Genereted-BY": "polib",
        "Content-Transfer-Encoding": "8bit",
    }
    if email:
        metadata["Last-Translator"] = email
        metadata["Report-Msgid-Bugs-To"] = email
        metadata["Language-Team"] = f"""{lang}, {email}"""
    po.metadata = metadata
    return po


def po2pddf(pofile: polib.POFile) -> pd.DataFrame:
    """
    output a pandas DataFrame matching UE4localizationsTool's format.

    return:
        pandas.DataFrame that each columns are corresponded to:

        - msgid to source
        - msgstr to Translation
        - msgctxt to key
        - msgtcomment to index
    """
    d = pd.DataFrame(
        [(x.msgid, x.msgstr, x.tcomment, x.msgctxt) for x in pofile if x.msgid != ""],
        columns=["source", "Translation", "index", "key"],
    )
    return d[["key", "source", "Translation", "index"]].sort_values(["index"])
