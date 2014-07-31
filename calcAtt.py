
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



# This is a simple ATT Mobile Share Value Plan 10GB phone bill spliter.
# The basic pricing is as follows,
# 	Group owner basic is 104.54, including member basic and group addition
# 	Group member basic is 19.39
# So the average basic for each is 27.905, the average group addition per person is 8.515
# If there exists any over usage, will lead to extra fees, works as follows,
# 	Data over usage: fees applied to the owners, need to split with actual over-user
#   Other over usage & extra service: 
# 	  1) if applied to individual, counts on him/herself
# -->>2) if applied to owner, need calc manually (split method unkown)


#  Dev Plan
#  Based on currnt bill statements online, the bill split strategy is as above.
#  Bill details is available online in html format.
#  1. Input is from one html bill detail, and one pdf data usage detail;
#     html is auto-processed, pdf needs manually select and paste.
#  2. Calculation is done using above strategy;
#  3. Output is decided to be a text msg content.
# 
#  Future plan
#  Auto retreive and pre-process input html pdf, auto send bill text to members.


import os.path
import re

class BillDetailer:
	def __init__(self, billFilePathName, dataUsage, path=os.getcwd()):
		self.path=path
		self.dataUsage=re.sub('[-]', ' ', dataUsage)
		with open(billFilePathName, "r", encoding="utf-8") as self.billPage:
			self.billContent=self.billPage.read()
			self.billContent=self.billContent.lower()
		self.dataBase={} #{[expense, data, dataExtraExpense]:number}
		self.phoneBook={'512 468 5514':'A',
						'512 468 6959':'B',
						'512 496 3468':'C',
						'512 694 7091':'D',
						'512 826 6324':'E',
						'512 865 8134':'F',
						'512 913 2195':'G',
						'512 923 2219':'Owner',
						'512 954 7686':'H',
						'512 954 7693':'I',
						'Owner':'512 923 2219'}
		self.totalMember=len(self.phoneBook)
		self.extraDataTotal=0

	def findBillAndUsageForEach(self):
		#find bill detail for each
		startPoint=0
		for x in range(10):
			startNumber=self.billContent.find("total for", startPoint)
			startExpense=self.billContent.find("$", startNumber)
			endPoint=self.billContent.find("<", startExpense)
			number=self.billContent[startNumber+10:startNumber+22]
			number=re.sub('[\n\t]', '', number)
			number=re.sub('[-]', ' ', number) #number stored as string
			expense=float(self.billContent[startExpense+1:endPoint])
			startPoint=startNumber+1
			self.dataBase[number]=[expense]

		#find usage detail for each
		startPoint=0
		for eachNumber in self.dataBase:
			startNumber=self.dataUsage.find(eachNumber, startPoint)
			endPoint=self.dataUsage.find("\n", startNumber)
			data=self.dataUsage[startNumber+13:endPoint]
			data=re.findall(r"\d+", data)
			data=int("".join(data))
			self.extraDataTotal
			self.dataBase[eachNumber].append(data)

	def splitBill(self):
		dataExtraExpense=self.dataBase[self.phoneBook['Owner']][0]-104.54
		for eachNumber in self.dataBase:
			if self.extraDataTotal > 0:
				self.dataBase[eachNumber].append(dataExtraExpense*(self.dataBase[eachNumber][1]-1000)/float(self.extraDataTotal))
			else:
				self.dataBase[eachNumber].append(0)
			if eachNumber == self.phoneBook['Owner']:
				self.dataBase[eachNumber].append(self.dataBase[eachNumber][2]+27.905)
			else:
				self.dataBase[eachNumber].append(self.dataBase[eachNumber][0]+self.dataBase[eachNumber][2]+8.515)

	def printMessage(self, display=print, index=3):
		#print("index=",index)
		for eachNumber in self.dataBase:
			display(self.phoneBook[eachNumber],"'s balance:",self.dataBase[eachNumber][index])




if __name__ == "__main__":
	billFilePathName="E:\\att\\bill.htm"
	dataUsage="512 468-5514 1,082\n\
				512 468-6959 176\n\
				512 496-3468 1,755\n\
				512 694-7091 1,272\n\
				512 826-6324 2,274\n\
				512 865-8134 657\n\
				512 913-2195 1,122\n\
				512 923-2219 319\n\
				512 954-7686 103\n\
				512 954-7693 85\n\
				This is just test data"
	billDetail=BillDetailer(billFilePathName, dataUsage)
	billDetail.findBillAndUsageForEach()
	billDetail.splitBill()
	billDetail.printMessage()

