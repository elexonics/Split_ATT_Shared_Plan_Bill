
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

	global Path, billDetail
	Path=ent.get()
	if not os.path.exists(os.path.dirname(Path)):
		txt.delete(1.0, END)
		txt.insert(1.0, "Provide with a valid bill HTML pathname first!\nWaiting for commands...")
	elif Data == "":
		txt.delete(1.0, END)
		txt.insert(1.0, "Provide with the data usage first!\nWaiting for commands...")
	else:
		txt.delete(1.0, END)
		
		billDetail.findBillAndUsageForEach()
		billDetail.splitBill()
		billDetail.printMessage(redirectedPrint)


def newWindowGetText(dest):
	def quitAndPaste():
		if dest == "Data":
			data=txt.get(1.0, END)
			billDetail.setDataUsage(data)
		else:
			bill=txt.get(1.0, END)
			billDetail.setBillContent(bill)
		newWindow.destroy()

	#print("new window expected!")
	newWindow=Tk()
	newWindow.iconbitmap("hedgehogle.ico")
	newWindow.title("Data Usage Details")
	newWindow.geometry("300x400")
	frmTop=Frame(newWindow)
	frmBottom=Frame(newWindow)
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
	filename=filedialog.askopenfilename(filetypes=(("Text file", ".txt"),("All files", ".*")))
	clearBox(None, ent, "Entry")
	ent.insert(0, filename)



if __name__ == "__main__":

	billDetail=BillDetailer() #billDetailer object from calcAtt.py

	root=Tk()
	root.iconbitmap("hedgehogle.ico")
	root.title("CalcAtt")
	root.geometry("502x353")

	frmTop=Frame(root)
	frmBottom=Frame(root)
	frmTop.pack(side=TOP)
	frmBottom.pack(side=BOTTOM)

	hhGIF=PhotoImage(file="hedgehogle.gif")
	hhlbl0=Label(frmTop, image=hhGIF) #hedgehog icon
	hhlbl0.grid(row=0, column=1, rowspan=2, columnspan=2, sticky=E)
	hhlbl1=Label(frmTop, text="CalcAtt", font=("Helvetica", 18, "bold")) #calcatt
	hhlbl1.grid(row=0, column=3, rowspan=2, columnspan=2, sticky=W)

	
	ent=Entry(frmTop, bd=3, width=55, )
	ent.bind("<Button-1>", lambda event: clearBox(event, ent, "Entry"))
	ent.insert(0, "Enter here the file to add monthly balance, *.txt.") #enter file path entry
	Btn1=Button(frmTop, text="Save to File:", command=browseFile) #save to file button
	Btn2=Button(frmTop, text="Enter Bill", command=browseFile) #enter bill button
	ent.grid(row=2, column=4, columnspan=4, padx=5)
	Btn1.grid(row=2, column=1, columnspan=1, padx=5)
	
	Btn2.grid(row=2, column=0, columnspan=1, padx=5)

	btn=Button(frmTop, width=15, text="Enter Data Usage", lambda: newWindowGetText("Data")) #enter data usage
	btn.grid(row=0, column=6, columnspan=2, padx=5, sticky=E)
	btn=Button(frmTop, width=15, text="Calc & Split Bill", command=calc) #calc&split bill
	btn.grid(row=1, column=6, columnspan=2, padx=5, sticky=E)

	

	txt=Text(frmBottom, bg="#000000", fg="#01DF01", bd=8) #text box for msgs
	txt.insert(1.0, "Waiting for commands...")
	txt.pack(fill=BOTH)

	root.mainloop()
