#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk
import tkFont

class MainWindow(tk.Toplevel):
    def __init__(self, master, config):
        tk.Toplevel.__init__(self, master)

        # create a custom font
        self.customFont = tkFont.Font(family="Verdana", size=16)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)

        # the refresh button
        self.refreshButton = tk.Button(self, text='Refresh', width=12, bg='lightgreen', activebackground='lightgreen', font=self.customFont)
        self.refreshButton.grid(row=0, padx=10, pady=10)
        self.refreshButton.focus()

        # the text below the percentage
        self.infotext = tk.StringVar()
        self.infotext.set('Press button or space to get\ntime entries from toggl.')
        self.infolabel = tk.Label(self, textvariable=self.infotext)
        self.infolabel.grid(row=2, padx=10, pady=10)

        # the plot button
        self.plotButton = tk.Button(self, text='Plot', width=12, font=self.customFont)
        self.plotButton.grid(row=3, padx=10, pady=10)


        self.attributes("-topmost", config.TOPMOST)
        self.resizable(width=False, height=False) 


    def set_percentile(self, content):
        self.refreshButton.config(text=content)
