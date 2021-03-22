import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np


import sqlite3


class TopPanel(wx.Panel):
	def __init__(self,parent):
		wx.Panel.__init__(self,parent = parent)
		self.figure = Figure()
		self.CreateFigure()

	def CreateFigure(self):
		self.axes = self.figure.add_subplot(111)
		self.canvas = FigureCanvas(self,-1,self.figure)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.canvas, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		self.axes.set_xlabel("X")
		self.axes.set_ylabel("Y")


	def LoadProblem(self, x, y):
		self.figure.clf()
		self.CreateFigure()
		self.axes.plot(x,y)

class BottomPanel(wx.Panel):
	def __init__(self, parent, top):
		wx.Panel.__init__(self,parent = parent)

		self.graph = top

		labelLoad = wx.StaticText(self,-1,"Load a problem: ",pos = (100,10))
		self.textboxLoad = wx.TextCtrl(self,-1,"file name",pos=(100,30))
		self.buttonLoad = wx.Button(self,-1,"Load",pos=(100,55))
		self.buttonLoad.Bind(wx.EVT_BUTTON, self.LoadProblem)

	def LoadProblem(self, event):
		conn = sqlite3.connect('TSP_db.db')
		c = conn.cursor()
		problem_name = self.textboxLoad.GetValue()
		item = c.execute('SELECT * FROM solutions WHERE Problem_name = ?', (problem_name,))
		rows = c.fetchall()

		if not rows:
			print("Solution is not in database.")
			exit()

		min_distance = rows[0][1]
		optimal_solution_index = 0
		for i in range(len(rows)):
			if rows[i][1] < min_distance:
				min_distance = rows[i][1]
				optimal_solution_index = i

		optimal_route = (rows[optimal_solution_index][2].split(","))
		for i in range(len(optimal_route)):
			optimal_route[i] = int(optimal_route[i])

		x = []
		y = []
		for i in range(len(optimal_route)):
			x.append(optimal[i][1][0])
			y.append(optimal[i][1][1])

		self.graph.LoadProblem(x,y)





class Main(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, parent = None, title = "TSP Solver", size=(800,600))

		splitter = wx.SplitterWindow(self)

		top = TopPanel(splitter)
		bottom = BottomPanel(splitter, top)
		splitter.SplitHorizontally(top,bottom)
		splitter.SetMinimumPaneSize(400)










if __name__ == "__main__":
	app = wx.App()
	frame = Main()
	frame.Show()
	app.MainLoop()