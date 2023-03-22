# dend-rail-editor

## 概要

dend-rail-editor は、電車でDのレールバイナリを、GUI画面上で編集するソフトウェアである。

## 動作環境

* 電車でDが動くコンピュータであること
* OS: Windows 10 64bit の最新のアップデートであること
* OSの端末が日本語に対応していること

※ MacOS 、 Linux などの Unix 系 OS での動作は保証できない。

## 免責事項

このプログラムを使用して発生したいかなる損害も製作者は責任を負わない。

このプログラムを実行する前に、自身のコンピュータのフルバックアップを取得して、
安全を担保したうえで実行すること。
このプログラムについて、電車でD 作者である、地主一派へ問い合わせてはいけない。

このソフトウェアの更新やバグ取りは、作者の義務ではなく解消努力目標とする。
Issue に上げられたバグ情報が必ず修正されるものではない。

* ライセンス：MIT

電車でD の正式なライセンスを持っていること。

本プログラムに関連して訴訟の必要が生じた場合、東京地方裁判所を第一審の専属的合意管轄裁判所とする。

このプログラムのバイナリを実行した時点で、この規約に同意したものと見なす。

## 実行方法

![title](https://github.com/khttemp/dend-rail-editor/blob/main/image/title.png)

メニュの「ファイルの開く」で指定のBINファイルを開く。

必ず、プログラムが書込みできる場所で行ってください

レールバイナリにある情報を修正できるようになる。

また、レール情報、AMB情報のCSVを自動で作成する。

### BGM、配置情報

![bgm](https://github.com/khttemp/dend-rail-editor/blob/main/image/title.png)

BGMの数、登場させる車両の数、

それぞれ初期配置の位置を調整できる

### 要素１

![else1](https://github.com/khttemp/dend-rail-editor/blob/main/image/else1.png)

else1の機能は、夜景や背景の調整と思われる。

ddsや駅名標の定義、binファイルのアニメを調整できる

### smf情報

![smf](https://github.com/khttemp/dend-rail-editor/blob/main/image/smf.png)

ステージで使用するsmfのリストを調整できる

### 駅名位置情報

![stationName](https://github.com/khttemp/dend-rail-editor/blob/main/image/stationName.png)

ゲームの右上に現れる駅名をどの位置で表せるか調整できる

### 要素２

![else2](https://github.com/khttemp/dend-rail-editor/blob/main/image/else2.png)

未詳

### CPU情報

![cpu](https://github.com/khttemp/dend-rail-editor/blob/main/image/cpu.png)

レール位置によって、CPUの速度を調整できる

### ComicScript、土讃線

![comicDosan](https://github.com/khttemp/dend-rail-editor/blob/main/image/comicDosan.png)

ステージで使うコミックスクリプトの定義

土讃線スペシャルラインを調整できる

### レール情報

![rail](https://github.com/khttemp/dend-rail-editor/blob/main/image/rail.png)

ステージで使う、実際に走る線路の情報を見れる

修正するには、自動で作られたCSVを利用して調整する

RSのレール情報の要素についは、[【こちら】](/raildata.md)のリンクを参照

### 要素３

![else3](https://github.com/khttemp/dend-rail-editor/blob/main/image/else3.png)

未詳

### 要素４

![else4](https://github.com/khttemp/dend-rail-editor/blob/main/image/else4.png)

未詳

### AMB情報

![amb](https://github.com/khttemp/dend-rail-editor/blob/main/image/amb.png)

ステージで使う、オブジェクト扱いのAMBの情報を見れる

修正するには、自動で作られたCSVを利用して調整する


## ソースコード版の実行方法

このソフトウェアは Python3 系で開発されているため、 Python3 系がインストールされた開発機であれば、
ソースコードからソフトウェアの実行が可能である。


### 依存ライブラリ

* Tkinter

  Windows 版 Python3 系であれば、インストール時のオプション画面で tcl/tk and IDLE のチェックがあったと思う。
  tcl/tk and IDLE にチェックが入っていればインストールされる。
  
  Linux 系 OS では、 パッケージ管理システムを使用してインストールする。

### 動作環境

以下の環境で、ソースコード版の動作確認を行った

* OS: Windows 10 64bit
* Python 3.10.9 64bit
* pip 22.3.1 64bit
* PyInstaller 5.8.0 64bit
* 横1024×縦768ピクセル以上の画面解像度があるコンピュータ


## ソースコードの直接実行

Windows であれば以下のコマンドを入力する。


````
> python railEditor.py
````

これで、実行方法に記載した画面が現れれば動作している。

### FAQ

* Q. ImportError: No module named tkinter と言われて起動しない

  * A. 下のようなメッセージだろうか？ それであれば、 tkinter がインストールされていないので、インストールすること。
  
  ````
  > python editor.py
  Traceback (most recent call last):
    File "editor.py", line 6, in <module>
      from tkinter import *
  ImportError: No module named tkinter
  ````


* Q. 電車でDのゲームがあるが、指定したBINファイルがない。  

  * A. PackファイルをGARbro のような、アーカイバで展開すると得られる。

  * A. GARbro を使用して空パスワードで解凍すると無効なファイルになるので、適切なパスワードを入力すること。


* Q. BINファイルを指定しても、「電車でDのファイルではない、またはファイルが壊れた可能性があります。」と言われる

  * A. 抽出方法が間違っているか、抽出時のパスワードが間違っているのでは？作業工程をやり直した方がよい。

* Q. BINファイルを改造しても、変化がないけど？

  * A. 既存のPackファイルとフォルダーが同時にあるなら、Packファイルを優先して読み込んでいる可能性がある。

    読み込みしないように、抽出したPackファイルを変更するか消そう。

* Q. ダウンロードがブロックされる、実行がブロックされる、セキュリティソフトに削除される

  * A. ソフトウェア署名などを行っていないので、ブラウザによってはダウンロードがブロックされる

  * A. 同様の理由でセキュリティソフトが実行を拒否することもある。


### Windows 版実行バイナリ（ .exeファイル ）の作成方法

pyinstaller か Nuitka ライブラリをインストールする。 pip でも  easy_install  でも構わない。

下は、 pyinstaller を使用して、Windows 版実行バイナリ（ .exeファイル ）を作る例である。

````
> pyinstaller railEditor.py --onefile --noconsole
````

dist フォルダーが作られて、 railEditor.exe が出力される。

### Virustotal

![virustotal](https://github.com/khttemp/dend-rail-editor/blob/main/image/virustotal.png)

以上。