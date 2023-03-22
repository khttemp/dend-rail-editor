# レールデータの要素(RS)

## 1. index

レールの番号。RSでCSVで上書きする際、この情報は読み込まない。

## 2. prev_rail

初期位置の基準レールの番号。

-1の場合、原点から置き、

それ以外の場合、そのレール番号の「終端」を基準に配置する。

## 3. block

表示するレールのグループ（ブロックとする）。

現在位置のブロック番号から

およそ、±1のブロック番号に所属するレールを全部表示する。

## 4. dir_x

レールを上下に曲げる。下記を図を参照


| デフォルト | dir_x (+3) | dir_x (-3) |
| --- | --- | --- | 
| ![default](/image/rail_default.png) | ![dir_x_3](/image/rail_dir_x_3.png) | ![dir_x_-3](/image/rail_dir_x_-3.png) |

## 5. dir_y

レールを左右に曲げる。下記の図を参照

| デフォルト | dir_y (+3) | dir_y (-3) |
| --- | --- | --- | 
| ![default](/image/rail_default.png) | ![dir_y_3](/image/rail_dir_y_3.png) | ![dir_y_-3](/image/rail_dir_y_-3.png) |

## 6. dir_z

レールのカントを設定する。下記の図を参照

| デフォルト | dir_z (+3) | dir_z (-3) |
| --- | --- | --- | 
| ![default](/image/rail_default.png) | ![dir_z_3](/image/rail_dir_z_3.png) | ![dir_z_-3](/image/rail_dir_z_-3.png) |

## 7. mdl_no

「smf情報」リストのモデル番号。

## 8. mdl_kasen

レールの架線情報。今は「smf情報」で指定しているので【-1】固定。

## 9. mdl_kasenchu

「smf情報」リストのモデル番号。

ただし、架線柱モデルのみ読み込む。

-1の場合、「smf情報」に設定したモデルの架線柱を設定する。

-2の場合、架線柱モデルを置かない。

## 10. per

レールの長さの倍率。デフォルトは1.0倍

## 11~14. flg

レールのフラグ情報。

## 15. rail_data

レールの進行方向を決めるデータの数。

これに基づいて、次のデータ数も変わる。

## 16~. next_rail, next_no, prev_rail, prev_no

next_railは、現在レールから次のレール番号。

next_noは、次のレール番号のボーン数。

prev_railは、現在レールから以前のレール番号。

prev_noは、以前のレール番号のボーン数。

ボーン数は、「smf情報」にある長さに依存する。

詳しい繋ぎ方は、下記の図を参照。

![rail_data](/image/rail_data.png)