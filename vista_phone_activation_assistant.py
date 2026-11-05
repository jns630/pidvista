#!/usr/bin/env python
"""Windows Vista phone-activation assistant.

Launches Vista's own phone activation UI and helps format/copy the IID/CID.
It does not calculate, request, forge, or submit a Confirmation ID.
No product key is requested, stored, or transmitted.
"""
from __future__ import print_function
import re
import subprocess
import tkinter as tk
from tkinter import messagebox

def digits(s):
    return re.sub(r"[^0-9]", "", s or "")

def groups(s, width):
    d = digits(s)
    return " ".join(d[i:i+width] for i in range(0, len(d), width))

class App(object):
    def __init__(self, root):
        self.root = root
        root.title("Vista Phone Activation Assistant")
        root.geometry("610x430")
        root.resizable(False, False)
        tk.Label(root, text="Windows Vista phone activation",
                 font=("Segoe UI", 15, "bold")).pack(pady=(14, 4))
        tk.Label(root, text=("Uses the activation wizard built into Windows. "
                             "This helper does not generate a CID."),
                 wraplength=560).pack(pady=(0, 12))

        tk.Button(root, text="Open Windows phone activation (slui.exe 4)",
                  command=self.launch, height=2, width=48).pack(pady=5)

        tk.Label(root, text="Installation ID (IID) — normally 63 digits / 9 groups of 7",
                 anchor="w").pack(fill="x", padx=24, pady=(14, 3))
        self.iid = tk.Entry(root, width=82)
        self.iid.pack(padx=24)
        tk.Button(root, text="Format and copy IID", command=self.copy_iid).pack(pady=5)

        tk.Label(root, text="Confirmation ID (CID) — enter the 48 digits supplied by Microsoft",
                 anchor="w").pack(fill="x", padx=24, pady=(12, 3))
        self.cid = tk.Entry(root, width=82)
        self.cid.pack(padx=24)
        tk.Button(root, text="Validate, format and copy CID",
                  command=self.copy_cid).pack(pady=5)

        tk.Label(root,
          text=("The IID comes from Windows. Obtain the CID through Microsoft's "
                "supported activation channel for your licence. Then enter it in "
                "the Windows activation wizard. This app cannot contact Microsoft "
                "or activate Windows on its own."),
          wraplength=550, justify="left", fg="#333333").pack(padx=24, pady=16)

    def launch(self):
        try:
            subprocess.Popen(["slui.exe", "4"], shell=False)
        except Exception as e:
            messagebox.showerror("Could not open activation", str(e))

    def copy_iid(self):
        d = digits(self.iid.get())
        if len(d) != 63:
            messagebox.showerror("IID length", "Expected 63 digits. Check the IID shown by Windows.")
            return
        formatted = groups(d, 7)
        self.iid.delete(0, tk.END)
        self.iid.insert(0, formatted)
        self.root.clipboard_clear()
        self.root.clipboard_append(formatted)
        messagebox.showinfo("IID copied", "Formatted IID copied to clipboard.")

    def copy_cid(self):
        d = digits(self.cid.get())
        if len(d) != 48:
            messagebox.showerror("CID length", "Expected 48 digits. This checks format only, not authenticity.")
            return
        formatted = groups(d, 6)
        self.cid.delete(0, tk.END)
        self.cid.insert(0, formatted)
        self.root.clipboard_clear()
        self.root.clipboard_append(formatted)
        messagebox.showinfo("CID copied", "CID format looks correct and was copied. Enter it in Windows activation.")

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
