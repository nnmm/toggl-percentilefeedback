#!/usr/bin/python
# -*- coding: utf-8 -*-

import core.model as model
import view.mainwindow, view.plotwindow
import config

class Controller:
    def __init__(self, root):
        self.model = model.PercentileFeedback(config)
        self.model.percentage.addCallback(self.percentage_changed)
        self.model.plot_data.addCallback(self.plot_data_changed)

        self.view = view.mainwindow.MainWindow(root, config)
        self.view.refreshButton.config(command=self.refresh_percentile)
        self.view.plotButton.config(command=self.refresh_plot_data)

        self.plot = None


    def refresh_percentile(self):
        self.model.refresh_percentile()


    def refresh_plot_data(self):
        self.model.refresh_plot_data()


    # Called through the Observable 
    def percentage_changed(self, perc):
        """If the Observable notifies us that the percentage has changed, update the view"""
        self.view.set_percentile(perc)


    # Called through the Observable 
    def plot_data_changed(self, plot_data):
        """If the Observable notifies us that the plot data has changed, show the plot"""
        if not self.plot == None:
            self.plot.destroy()
            self.plot = None
        self.plot = view.plotwindow.PlotWindow(self.view)
        self.plot.draw_plot(plot_data)
    



if __name__ == '__main__':
    root = view.tk.Tk()
    root.withdraw()
    root.title("pfb")
    app = Controller(root)
    root.mainloop()