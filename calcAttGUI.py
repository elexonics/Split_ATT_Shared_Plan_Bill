
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

#! python3

from tkinter import *
from tkinter import filedialog
from calcAtt import BillDetailer
import os



def calc():
	def redirectedPrint(*output):
		for out in output:
			txt.insert(INSERT, out)
		txt.insert(INSERT, "\n")

	path=ent1.get()
	if not os.path.exists(os.path.dirname(path)):
		txt.delete(1.0, END)
		txt.insert(1.0, "Provide a valid balance store location.\nWaiting for commands...")
	else:
		txt.delete(1.0, END)
		billDetail.setBalanceStoreLocation(path)
		if billDetail.checkAllDetailsSet():
			billDetail.findBillAndUsageForEach()
			billDetail.splitBill()
			billDetail.printMessage(redirectedPrint)
		else:
			txt.insert(1.0, "Provide the data usage and bill detail first!\nWaiting for commands...")


def newWindowGetText(dest):
	def pasteAndQuit():
		if dest == 1:
			data=txt.get(1.0, END)
			billDetail.setDataUsage(data)
		else:
			bill=txt.get(1.0, END)
			billDetail.setBillContent(bill)
		newWindow.destroy()

	#print("new window expected!")
	newWindow=Tk()
	newWindow.iconbitmap("hedgehogle.ico")
	newWindow.title("Data Usage") if dest == 1 else newWindow.title("Bill Details")
	newWindow.geometry("300x400")
	frmTop=Frame(newWindow)
	frmBottom=Frame(newWindow)
	frmTop.pack(side=TOP)
	frmBottom.pack(side=BOTTOM)

	#Note, text must put at bottom, in order to auto-resize correctly
	txt=Text(frmBottom, bg="#000000", fg="#01DF01", bd=8)
	txt.bind("<Button-1>", lambda event: clearBox(txt, "Text"))
	txt.insert(INSERT, "Paste data usage HERE.") if dest == 1 else txt.insert(INSERT, "Paste bill details HERE.")
	txt.pack(fill=X)
	btn=Button(frmTop, width=20, text="Save and Close", command=pasteAndQuit)
	btn.pack(fill=BOTH)


def clearBox(instance, insName):
	instance.delete(0 if insName == "Entry" else 1.0, END)


def browseFile():
	filename=filedialog.askopenfilename(filetypes=(("Text file", ".txt"),("All files", ".*")))
	clearBox(ent1, "Entry")
	ent1.insert(0, filename)



if __name__ == "__main__":

	billDetail=BillDetailer() #billDetailer object from calcAtt.py


	#layout and button registering
	root=Tk()
	root.iconbitmap("hedgehogle.ico")
	root.title("Split AT&T")
	root.geometry("502x353")

	frmTop=Frame(root)
	frmBottom=Frame(root)
	frmTop.pack(side=TOP)
	frmBottom.pack(side=BOTTOM)

	#icon and heading
	iconName=PhotoImage(file="hedgehogle.gif")
	lbl0=Label(frmTop, image=iconName) #hedgehog icon
	lbl0.grid(row=0, column=1, rowspan=2, columnspan=2, sticky=E)
	lbl1=Label(frmTop, text="Split AT&T", font=("Helvetica", 18, "bold")) #heading
	lbl1.grid(row=0, column=3, rowspan=2, columnspan=2, sticky=W)

	#Paste Data Usage button, Paste Billing Details Button
	btn1=Button(frmTop, width=15, text="Paste Billing Details", command=lambda dest = 0 : newWindowGetText(dest))
	btn1.grid(row=0, column=6, columnspan=2, padx=5, sticky=E)
	btn2=Button(frmTop, width=15, text="Paste Data Usage", command=lambda dest = 1 : newWindowGetText(dest))
	btn2.grid(row=1, column=6, columnspan=2, padx=5, sticky=E)

	#Split Bill button, Save to File button and File Path entry box
	btn3=Button(frmTop, text="Split Bill", command=calc) #do the calculation
	btn3.grid(row=2, column=0, columnspan=1, padx=5)

	ent1=Entry(frmTop, bd=3, width=55)
	ent1.bind("<Button-1>", lambda event: clearBox(ent1, "Entry"))
	ent1.insert(0, "Save balance sheet to file as *.txt") #enter file path entry
	btn4=Button(frmTop, text="Save to File:", command=browseFile) #save to file button
	ent1.grid(row=2, column=4, columnspan=4, padx=5)
	btn4.grid(row=2, column=1, columnspan=1, padx=5)


	#console text box
	txt=Text(frmBottom, bg="#000000", fg="#01DF01", bd=8) #text box for msgs
	txt.insert(1.0, "Waiting for commands...")
	txt.pack(fill=BOTH)

	#start
	root.mainloop()
