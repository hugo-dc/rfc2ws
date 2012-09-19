import wx
#import gui
#import texts



class Rfc2Ws(wx.App):
	def init(self):
		# Splash window
		image = wx.Image(os.getcwd() + '/resources/splash.png', wx.BITMAP_TYPE_PNG)
		image = image.ConvertToBitmap()

		wx.SplashScreen(image, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 5500, None, -1)
		wx.Yield()

		self.frame = gui.MainWindow(parent=None, id=-1, title=texts.title)
		self.frame.Maximize()
		self.frame.Show(True)
		self.SetTopWindow(self.frame)

		return True

	def OnExit(self):
		pass 
		
		

if __name__ == '__main__':
	App = Rfc2Ws()
	App.MainLooop()
				


