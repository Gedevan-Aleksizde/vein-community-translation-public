# VEIN Community Translation

コミュニティ (1名)

v0.9.9

## ユーザー向けの説明

Nexusのアカウントを既に作っているならNexusからダウンロードできます. 作ってない・作りたくない人は右側の Releases から最新版をダウンロードし, 展開し, でてきた Vein フォルダをVeinのインストールフォルダに上書きしてください. 以下のように1以上のファイルがコピーされれば正常にインストールされています. 2つ目のファイルはバージョンによって含まれていたりいなかったりします.

* `Vein\Vein\Content\Pak\~zzzVein-JP.pak`
* (`Vein\Vein\Content\Pak\~zzzVein-JP-font.pak`)

## 使用方法 (WIP)

日本語ファイルではなく, ここで公開されている翻訳用ツールの説明です.

### 環境設定

1. VEIN本体に対応したUnreal Editor をインストールする
2. uv をインストールする.
3. このリポジトリをクローンまたはダウンロードする
4. [UE4 localizations Tool](https://github.com/amrshaheen61/UE4LocalizationsTool) をダウンロードし, .exe と .dll を bin フォルダにコピーする.
5. `bin\settings.bat` を開いてバージョン, 一時保存ディレクトリ, Unreal Editor のバイナリの場所, VEIN のインストールフォルダのパスを設定する. バージョンはこの後の保存用フォルダに使用するだけなので, 厳密に一致しなくともよい.


### POファイルを作成するまで

1. `settings.json` を開いてファイルパスとバージョンが適切であるかを確認する.
2. `bin\unpack.bat` を実行してVEIN本体のPAKファイルを展開し, 翻訳データをテキストファイルにする.
3. `uv run python/import-locres-txt.py` を実行し, テキストファイルをPOファイルに変換する.
4. 出力された PO ファイルを crowdin の source にアップロードするか, もしくはローカルで Poedit などを使って翻訳する.


### POファイルを言語ファイルとしてパッケージ化する

1. 自分へ編集したPOファイルか, Crowdin からダウンロードしたファイルを,  `<STORAGEDIR>\fromcrowdin\<VERSION>\<LANG>\*.po` に配置する
2. `uv run python/po2csv.py` を実行して更新された翻訳文を変換する.
3.  `bin\update-licres.bat` を実行して翻訳を反映したLOCRESファイルを作成する
4.  `bin\pack.bat` を実行する


一時保存フォルダの構造

* ./
  * text
    * from-crowdin : PAKに再度パッキングするPOファイルを置く
    * original-po : VEIN本体に含まれている翻訳データをPOファイルに変換したものを置く
    * original-locres : PAK ファイルに入っている LOCRES ファイルを置く
      *  <version>\<lang>\Game.locres
    * oritinal-txt : 実際にはCSVも入っている
      * <version>\<lang>game.locres.txt
    * to-locres : 新しい翻訳を反映したLOCRESファイルを置く
      * <version>\<lang>game.locres.txt