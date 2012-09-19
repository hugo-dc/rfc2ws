import wx


class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, style= wx.DEFAULT_FRAME_STYLE)


