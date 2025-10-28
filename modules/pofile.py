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
    for i, r in data.iterrows():
        pof.append(
            polib.POEntry(
                msgid=r[col_index] + r[col_source],
                msgtxt=r[col_transl],
                tcomment=r[col_key],
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
    input: Po の msgid が index+source
    return:
    """
    d = pd.DataFrame(
        [(x.msgid, x.msgstr, x.tcomment[0]) for x in pofile if x.msgid != ""],
        columns=["id", "Translation", "id"],
    )
    d["key"] = d["comment"]
    d["index"] = d["id"].str.replace("^(.+?)/.+$", "\1", regex=True).astype(int)
    d["source"] = d["id"].str.replace("^.+?/(.+)$", "\1", regex=True)
    return d
