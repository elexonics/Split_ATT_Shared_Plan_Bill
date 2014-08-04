
# Copyright (c) 2014 Zirui Wang @elexonics

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.



from tkinter import *
from tkinter import filedialog
from calcAtt import BillDetailer
import os



def calc():
	def redirectedPrint(*output):
		for out in output:
			txt.insert(INSERT, out)
		txt.insert(INSERT, "\n")

	global Path
	Path=ent.get()
	if not os.path.exists(os.path.dirname(Path)):
		txt.delete(1.0, END)
		txt.insert(1.0, "Provide with a valid bill HTML pathname first!\nWaiting for commands...")
	elif Data == "":
		txt.delete(1.0, END)
		txt.insert(1.0, "Provide with the data usage first!\nWaiting for commands...")
	else:
		txt.delete(1.0, END)
		billDetail=BillDetailer(Path, Data)
		billDetail.findBillAndUsageForEach()
		billDetail.splitBill()
		billDetail.printMessage(redirectedPrint)


def newWindowGetText():
	def quitAndPaste():
		global Data
		Data=txt.get(1.0, END)
		#print(Data)
		dataUsage.destroy()

	#print("new window expected!")
	dataUsage=Tk()
	dataUsage.iconbitmap("hedgehogle.ico")
	dataUsage.title("Data Usage Details")
	dataUsage.geometry("300x400")
	frmTop=Frame(dataUsage)
	frmBottom=Frame(dataUsage)
	frmTop.pack(side=TOP)
	frmBottom.pack(side=BOTTOM)

	#Note, text must put at bottom, in order to auto-resize correctly
	txt=Text(frmBottom, bg="#000000", fg="#01DF01", bd=8)
	txt.bind("<Button-1>", lambda event: clearBox(event, txt, "Text"))
	txt.insert(INSERT, "Copy the data usage HERE.")
	txt.pack(fill=X)
	btn=Button(frmTop, width=20, text="Save and Close", command=quitAndPaste)
	btn.pack(fill=BOTH)


def clearBox(event, instance, insName):
	instance.delete(0 if insName == "Entry" else 1.0, END)
	# print(event)


def browseFile():
	filename=filedialog.askopenfilename(filetypes=(("html files", ".htm; .html"),("All files", ".*")))
	clearBox(None, ent, "Entry")
	ent.insert(0, filename)

if __name__ == "__main__":
	Path=""
	Data=""

	root=Tk()
	root.iconbitmap("hedgehogle.ico")
	root.title("CalcAtt")
	root.geometry("502x353")

	frmTop=Frame(root)
	frmBottom=Frame(root)
	frmTop.pack(side=TOP)
	frmBottom.pack(side=BOTTOM)

	hhGIF=PhotoImage(file="hedgehogle.gif")
	hhlbl0=Label(frmTop, image=hhGIF)
	hhlbl0.grid(row=0, column=2, rowspan=2, columnspan=2, sticky=E)
	hhlbl1=Label(frmTop, text="CalcAtt", font=("Helvetica", 18, "bold"))
	hhlbl1.grid(row=0, column=4, rowspan=2, columnspan=2, sticky=W)

	lbl=Button(frmTop, text="Bill HTML File Browse:", command=browseFile)
	ent=Entry(frmTop, bd=3, width=55, )
	ent.bind("<Button-1>", lambda event: clearBox(event, ent, "Entry"))
	ent.insert(0, "Type in the full pathname of bill html file.  e.g. E:\\att\\bill.htm")
	lbl.grid(row=2, column=0, columnspan=2, padx=5)
	ent.grid(row=2, column=2, columnspan=6, padx=5)

	btn=Button(frmTop, width=15, text="Enter Data Usage", command=newWindowGetText)
	btn.grid(row=0, column=6, columnspan=2, padx=5, sticky=E)

	btn=Button(frmTop, width=15, text="Calc & Split Bill", command=calc)
	btn.grid(row=1, column=6, columnspan=2, padx=5, sticky=E)

	

	txt=Text(frmBottom, bg="#000000", fg="#01DF01", bd=8)
	txt.insert(1.0, "Waiting for commands...")
	txt.pack(fill=BOTH)

	root.mainloop()
