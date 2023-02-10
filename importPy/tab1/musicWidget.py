import tkinter
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import simpledialog as sd


class MusicWidget:
    def __init__(self, frame, decryptFile, reloadFunc):
        self.frame = frame
        self.decryptFile = decryptFile
        self.reloadFunc = reloadFunc

        self.txtFrame = tkinter.Frame(self.frame, padx=10, pady=5)
        self.txtFrame.pack(anchor=tkinter.NW)

        self.musicLb = tkinter.Label(self.txtFrame, text="BGM数", font=("", 20), width=7, borderwidth=1, relief="solid")
        self.musicLb.grid(row=0, column=0, sticky=tkinter.W + tkinter.E)

        self.varMusic = tkinter.IntVar()
        self.varMusic.set(self.decryptFile.musicCnt)
        self.musicTextLb = tkinter.Label(self.txtFrame, textvariable=self.varMusic, font=("", 20), width=7, borderwidth=1, relief="solid")
        self.musicTextLb.grid(row=0, column=1, sticky=tkinter.W + tkinter.E)
        self.musicBtn = tkinter.Button(self.txtFrame, text="修正", font=("", 14), command=lambda: self.editVar(self.varMusic.get()))
        self.musicBtn.grid(row=0, column=2, sticky=tkinter.W + tkinter.E)

    def editVar(self, value):
        result = EditMusicCnt(self.frame, "BGM数変更", self.decryptFile, value)

        if result.reloadFlag:
            if not self.decryptFile.saveMusic(result.resultValue):
                self.decryptFile.printError()
                mb.showerror(title="エラー", message="予想外のエラーが発生しました")
                return
            mb.showinfo(title="成功", message="BGM情報を修正しました")

            self.reloadFunc()


class EditMusicCnt(sd.Dialog):
    def __init__(self, master, title, decryptFile, val):
        self.decryptFile = decryptFile
        self.val = val
        self.reloadFlag = False
        self.resultValue = 0
        super(EditMusicCnt, self).__init__(parent=master, title=title)

    def body(self, master):
        self.resizable(False, False)

        self.valLb = ttk.Label(master, text="値を入力してください", font=("", 14))
        self.valLb.pack()

        self.varMusicCnt = tkinter.IntVar()
        self.varMusicCnt.set(self.val)
        self.valEt = ttk.Entry(master, textvariable=self.varMusicCnt, font=("", 14), width=16)
        self.valEt.pack()

    def validate(self):
        result = mb.askokcancel(title="確認", message="この値で修正しますか？", parent=self)

        if result:
            try:
                try:
                    res = int(self.varMusicCnt.get())
                    if res <= 0:
                        errorMsg = "1以上の数字で入力してください。"
                        mb.showerror(title="数字エラー", message=errorMsg)
                        return False
                    self.resultValue = res
                    return True
                except Exception:
                    errorMsg = "整数で入力してください。"
                    mb.showerror(title="数字エラー", message=errorMsg)
            except Exception:
                errorMsg = "予想外のエラーです"
                mb.showerror(title="エラー", message=errorMsg)

    def apply(self):
        self.reloadFlag = True
