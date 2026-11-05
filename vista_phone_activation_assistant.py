#!/usr/bin/env python
"""Legacy Windows and Office activation helper.

This utility launches the installed product's activation UI and helps format
Installation IDs and Confirmation IDs obtained through Microsoft's supported
activation channel. It does not calculate or forge activation responses.
"""
from __future__ import print_function
import re
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox, ttk

SUPPORT_URL = ("https://support.microsoft.com/en-gb/windows/activation/"
               "activate-windows-online-or-offline-using-installation-and-confirmation-id")

PRODUCTS = {
    "Windows XP": {
        "iid_group": 6, "iid_expected": None,
        "launch": ["oobe/msoobe.exe", "/a"],
        "hint": "Open Start > Run and use the telephone activation option. "
                "XP's IID length can vary by activation context; this helper "
                "does not reject it based on a guessed length."
    },
    "Windows Vista": {
        "iid_group": 7, "iid_expected": 63,
        "launch": ["slui.exe", "4"],
        "hint": "Vista normally displays a 63-digit IID in 9 groups of 7."
    },
    "Office XP": {
        "iid_group": 6, "iid_expected": None, "launch": None,
        "hint": "Open an Office application > Help > Activate Product."
    },
    "Office 2003": {
        "iid_group": 6, "iid_expected": None, "launch": None,
        "hint": "Open an Office application > Help > Activate Product."
    },
    "Office 2007": {
        "iid_group": 6, "iid_expected": None, "launch": None,
        "hint": "Open an Office application > Office button > Options > Resources > Activate."
    },
    "Plus! Digital Media Edition": {
        "iid_group": 6, "iid_expected": None, "launch": None,
        "hint": "Use the activation option in the installed Plus! application."
    },
}

def only_digits(value):
    return re.sub(r"[^0-9]", "", value or "")

def group_digits(value, width):
    return " ".join(value[i:i + width] for i in range(0, len(value), width))

class ActivationAssistant(object):
    def __init__(self, root):
        self.root = root
        root.title("Legacy Windows & Office Activation Assistant")
        root.geometry("700x590")
        root.minsize(650, 550)

        tk.Label(root, text="Legacy activation assistant",
                 font=("Segoe UI", 16, "bold")).pack(pady=(14, 4))
        tk.Label(root, text="Windows XP / Vista and legacy Office activation",
                 fg="#444").pack(pady=(0, 12))

        product_row = tk.Frame(root)
        product_row.pack(fill="x", padx=24)
        tk.Label(product_row, text="Product:", width=12, anchor="w").pack(side="left")
        self.product = tk.StringVar(value="Windows Vista")
        self.product_box = ttk.Combobox(
            product_row, textvariable=self.product, values=list(PRODUCTS.keys()),
            state="readonly", width=34)
        self.product_box.pack(side="left")
        self.product_box.bind("<<ComboboxSelected>>", self.update_hint)

        self.hint = tk.Label(root, text="", wraplength=640, justify="left",
                             anchor="w", fg="#333")
        self.hint.pack(fill="x", padx=24, pady=10)

        self.launch_button = tk.Button(root, text="Open product activation",
                                        command=self.launch, height=2, width=34)
        self.launch_button.pack(pady=4)

        tk.Label(root, text="Installation ID (IID)", anchor="w",
                 font=("Segoe UI", 10, "bold")).pack(fill="x", padx=24, pady=(18, 3))
        self.iid = tk.Entry(root, font=("Consolas", 10))
        self.iid.pack(fill="x", padx=24)
        tk.Button(root, text="Format and copy IID", command=self.copy_iid).pack(pady=6)

        tk.Label(root, text="Confirmation ID (CID) supplied by Microsoft",
                 anchor="w", font=("Segoe UI", 10, "bold")).pack(
                     fill="x", padx=24, pady=(12, 3))
        self.cid = tk.Entry(root, font=("Consolas", 10))
        self.cid.pack(fill="x", padx=24)
        tk.Button(root, text="Check 48-digit format and copy CID",
                  command=self.copy_cid).pack(pady=6)

        buttons = tk.Frame(root)
        buttons.pack(pady=12)
        tk.Button(buttons, text="Microsoft activation instructions",
                  command=lambda: webbrowser.open(SUPPORT_URL)).pack(side="left", padx=5)
        tk.Button(buttons, text="Clear fields", command=self.clear).pack(side="left", padx=5)

        tk.Label(root, text=(
            "Important: this is an organizer and launcher, not a CID generator. "
            "It does not create, guess, authenticate, or submit CIDs. A correctly "
            "formatted 48-digit value is not proof that Microsoft issued or will "
            "accept it. Obtain the CID through Microsoft's supported activation "
            "channel for your licence, then enter it in the product's activation wizard."
        ), wraplength=645, justify="left", fg="#7a2e2e").pack(
            fill="x", padx=24, pady=(8, 14))
        self.update_hint()

    def update_hint(self, event=None):
        product = PRODUCTS[self.product.get()]
        self.hint.config(text=product["hint"])
        self.launch_button.config(
            state=("normal" if product["launch"] else "disabled"),
            text=("Open " + self.product.get() + " activation"
                  if product["launch"] else "Use the activation menu in the product"))

    def launch(self):
        command = PRODUCTS[self.product.get()]["launch"]
        if not command:
            messagebox.showinfo("Activation", PRODUCTS[self.product.get()]["hint"])
            return
        try:
            subprocess.Popen(command, shell=False)
        except Exception as exc:
            messagebox.showerror(
                "Could not open activation",
                "Windows could not start the activation wizard.\n\n" + str(exc))

    def copy_iid(self):
        product = PRODUCTS[self.product.get()]
        value = only_digits(self.iid.get())
        expected = product["iid_expected"]
        if not value:
            messagebox.showerror("IID", "Enter the Installation ID displayed by the product.")
            return
        if expected and len(value) != expected:
            messagebox.showerror(
                "IID length", "For Windows Vista, expected 63 digits; found %d." % len(value))
            return
        formatted = group_digits(value, product["iid_group"])
        self.iid.delete(0, tk.END)
        self.iid.insert(0, formatted)
        self.copy_to_clipboard(formatted)
        messagebox.showinfo("IID copied", "Formatted IID copied. Formatting does not validate the IID.")

    def copy_cid(self):
        value = only_digits(self.cid.get())
        if len(value) != 48:
            messagebox.showerror(
                "CID format", "A standard CID contains 48 digits (8 groups of 6). Found %d." % len(value))
            return
        formatted = group_digits(value, 6)
        self.cid.delete(0, tk.END)
        self.cid.insert(0, formatted)
        self.copy_to_clipboard(formatted)
        messagebox.showinfo(
            "CID copied",
            "The value has the expected length and was copied. This does not verify authenticity or activation.")
    
    def copy_to_clipboard(self, value):
        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()

    def clear(self):
        self.iid.delete(0, tk.END)
        self.cid.delete(0, tk.END)

def main():
    root = tk.Tk()
    ActivationAssistant(root)
    root.mainloop()

if __name__ == "__main__":
    main()
