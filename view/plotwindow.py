#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk

class PlotWindow(tk.Toplevel):
    """Simple plotting with the Tkinter Canvas class"""
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.width = 800
        self.height = 300
        self.margin = 50
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg='white', highlightthickness=0)
        self.canvas.pack()


    def make_point(self, x, y):
        """Creates a dot from a pair of values"""
        x_c = self.margin + float(x)/float(self.data_max_x)*(self.width - 2*self.margin)
        y_c = self.height - self.margin + float(y)/float(self.data_max_y)*(2*self.margin-self.height)
        self.canvas.create_oval(x_c-6, y_c-6, x_c+6, y_c+6, width=1, fill='SkyBlue2', outline='')


    def draw_axes(self, plot_data):
        """Draws and labels the axes"""
        # helper variables, all in pixels
        x0 = self.margin
        y0 = self.height - self.margin
        plotwidth = self.width - 2*self.margin
        plotheight = self.height - 2*self.margin

        self.data_max_x = len(plot_data)
        self.data_max_y = max(plot_data)

        # draw x and y axes
        self.canvas.create_line(0, y0, self.width, y0)
        self.canvas.create_line(x0, 0, x0, self.height)

        # where do we put the markings on the x axis?
        # if there’s more than 20 px for each datapoint, we make markings for all of them
        num_steps_x = self.data_max_x
        if plotwidth/self.data_max_x < 20:
            num_steps_x = plotwidth/20
        step_x = float(plotwidth)/num_steps_x
        # label_step_x is the increment of the number below the markings
        label_step_x = float(self.data_max_x)/float(num_steps_x)

        for i in range(num_steps_x):
            x = self.margin + ((i+1) * step_x)
            self.canvas.create_line(x,self.height - self.margin+3,x,self.height - self.margin-4)
            self.canvas.create_text(x,self.height - self.margin+4, text='%d'% (label_step_x*(i+1)), anchor=tk.N)

        # where do we put the markings on the y axis? Same procedure as above.
        num_steps_y = self.data_max_y
        if plotheight/self.data_max_y < 20:
            num_steps_y = plotheight/20
        step_y = float(plotheight)/num_steps_y
        label_step_y = float(self.data_max_y)/float(num_steps_y)

        for i in range(num_steps_y):
            y = y0 - ((i+1) * step_y)
            self.canvas.create_line(self.margin-3, y, self.margin+4, y)
            self.canvas.create_text(self.margin-4,y, text='%5.1f'% (label_step_y*(i+1)), anchor=tk.E)
        

    def draw_plot(self, plot_data):
        """Scales the values and creates the plot"""
        percentages = [float(x)/576.0 for x in plot_data]
        self.draw_axes(percentages)
        for (x, y) in zip(range(self.data_max_x), percentages):
            self.make_point(x, y)