"""
Mini GUI for the Trading ROBOT 
"""
from setting import DOMAIN, ACCOUNT_ID, ACCESS_TOKEN
from tkinter import *
import sys

class GUI(Frame): 
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.parent = parent
		self.variables = []
		self.draw()

	def draw(self):
		bottomframe = Frame(self.parent, relief=SUNKEN, bd=2)
		bottomframe.pack(side=BOTTOM, fill = X)
		Button(bottomframe, text='START Trading', command=()).pack(side=LEFT)
		Button(bottomframe, text='STOP Trading', command=()).pack(side=LEFT)
		Button(bottomframe, text='Fetch Entries', command=(lambda: self.fetch(self.variables))).pack(side=LEFT)
		Button(bottomframe, text='Help?', command=()).pack(side=LEFT)
		Button(bottomframe, text='Quit', command=(lambda: sys.exit())).pack(side=LEFT)

		''' 
		begins Oanda form
		'''
		oandaform = Frame(self.parent, relief=SUNKEN, bd=2)
		#Trade settings
		oanda1 = Frame(oandaform)
		oandarite1 = Frame(oandaform)
		
		oandaform.pack(side=LEFT, expand=YES, fill=BOTH)
		Heading = Label(oandaform, text="Oanda Settings")
		Heading.pack(side=TOP)
		
		oanda1.pack(side=LEFT)
		oandarite1.pack(side=RIGHT, expand=YES, fill=X) # grow horizontal	

			###domain - practise or real?
		lab10 = Label(oanda1, width=20, text="Domain") # add to columns
		ent10 = Entry(oandarite1)
		lab10.pack(side=TOP)
		ent10.pack(side=TOP, fill=X) # grow horizontal
		var10 = StringVar()
		ent10.config(textvariable=var10) # link field to var
		var10.set(DOMAIN)
		self.variables.append(var10)

			###account number
		lab9 = Label(oanda1, width=20, text="Account Number") # add to columns
		ent9 = Entry(oandarite1)
		lab9.pack(side=TOP)
		ent9.pack(side=TOP, fill=X) # grow horizontal
		var9 = StringVar()
		ent9.config(textvariable=var9) # link field to var
		var9.set(ACCOUNT_ID)
		self.variables.append(var9)

			###api key
		lab11 = Label(oanda1, width=20, text="API Key") # add to columns
		ent11 = Entry(oandarite1)
		lab11.pack(side=TOP)
		ent11.pack(side=TOP, fill=X) # grow horizontal
		var11 = StringVar()
		ent11.config(textvariable=var11) # link field to var
		var11.set(ACCESS_TOKEN)
		self.variables.append(var11)



		''' 
		begins Form1
		'''
		form1 = Frame(self.parent, relief=SUNKEN, bd=2)
		#Trade settings
		left1 = Frame(form1)
		rite1 = Frame(form1)
		
		form1.pack(side=LEFT, expand=YES, fill=BOTH)
		Heading = Label(form1, text="Trade Settings")
		Heading.pack(side=TOP)
		
		left1.pack(side=LEFT)
		rite1.pack(side=RIGHT, expand=YES, fill=X) # grow horizontal	
			###currency pair
		lab1 = Label(left1, width=20, text="Currency Pair") # add to columns
		ent1 = Entry(rite1)
		lab1.pack(side=TOP)
		ent1.pack(side=TOP, fill=X) # grow horizontal
		var1 = StringVar()
		ent1.config(textvariable=var1) # link field to var
		var1.set('EUR_USD')
		self.variables.append(var1)
			###number of units
		lab2 = Label(left1, width=20, text="Number of Units") # add to columns
		ent2 = Entry(rite1)
		lab2.pack(side=TOP)
		ent2.pack(side=TOP, fill=X) # grow horizontal
		var2 = StringVar()
		ent2.config(textvariable=var2) # link field to var
		var2.set('5')
		self.variables.append(var2)

		''' 
		begins Form2
		'''
		
		form2 = Frame(self.parent, relief=SUNKEN, bd=2)
		#Config settings
		left2 = Frame(form2)
		rite2 = Frame(form2)

		form2.pack(side=LEFT, fill=BOTH, expand=YES)
		Heading = Label(form2, text="Config Settings")
		Heading.pack(side=TOP)

		left2.pack(side=LEFT)
		rite2.pack(side=RIGHT, expand=YES, fill=X)
			###Hearthbeat
		lab4 = Label(left2, width=20, text="Hearthbeat") # add to columns
		ent4 = Entry(rite2)
		lab4.pack(side=TOP)
		ent4.pack(side=TOP, fill=X) # grow horizontal
		var4 = StringVar()
		ent4.config(textvariable=var4) # link field to var
		var4.set('10')
		self.variables.append(var4)

		'''
		begins Form3
		'''
		
		form3 = Frame(self.parent, relief=SUNKEN, bd=2)
		#Config settings
		left3 = Frame(form3)
		rite3 = Frame(form3)

		form3.pack(side=RIGHT, fill=BOTH, expand=YES)
		Heading = Label(form3, text="Strategy Settings")
		Heading.pack(side=TOP)

		left3.pack(side=LEFT)
		rite3.pack(side=RIGHT, expand=YES, fill=X)
			###Strategy
		lab5 = Label(left3, width=20, text="Choose Strategy:") # add to columns
		var5 = StringVar()
		var5.set('RSI')
		ent5 = OptionMenu(rite3, var5, "TestRandomStrategy", "RSI", "...")
		lab5.pack(side=TOP)
		ent5.pack(side=TOP, fill=X) # grow horizontal
		
		#ent5.config(textvariable=var5) # link field to var
		
		self.variables.append(var5)

			###min_window
		lab6 = Label(left3, width=20, text="Minimum Window:") # add to columns
		ent6 = Entry(rite3)
		lab6.pack(side=TOP)
		ent6.pack(side=TOP, fill=X) # grow horizontal
		var6 = StringVar()
		ent6.config(textvariable=var6) # link field to var
		var6.set('15')
		self.variables.append(var6)

			###persistence
		lab12 = Label(left3, width=20, text="Persistence:") # add to columns
		ent12 = Entry(rite3)
		lab12.pack(side=TOP)
		ent12.pack(side=TOP, fill=X) # grow horizontal
		var12 = StringVar()
		ent12.config(textvariable=var12) # link field to var
		var12.set('3')
		self.variables.append(var12)


			###up_boundary
		lab7 = Label(left3, width=20, text="Up Boundary:") # add to columns
		ent7 = Entry(rite3)
		lab7.pack(side=TOP)
		ent7.pack(side=TOP, fill=X) # grow horizontal
		var7 = StringVar()
		ent7.config(textvariable=var7) # link field to var
		var7.set('80')
		self.variables.append(var7)

			### low_boundary
		lab8 = Label(left3, width=20, text="Low Boundary:") # add to columns
		ent8 = Entry(rite3)
		lab8.pack(side=TOP)
		ent8.pack(side=TOP, fill=X) # grow horizontal
		var8 = StringVar()
		ent8.config(textvariable=var8) # link field to var
		var8.set('20')
		self.variables.append(var8)


	def fetch(self, variables):
		for variable in variables:
			print('Input %s => "%s"' % (variables.index(variable), variable.get())) # get from var


if __name__=='__main__':
	root = Tk()
	root.title("QSForex-mini by M.Terzi")
	gui = GUI(root)
	root.mainloop()
