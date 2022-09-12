"""Subnet Calculator

Contains the Address class, always keeps tract of a "numberList" which is a four
element list that is dynamically updated whether the binary representation of the data
is changed or the decimal representation is changed.

Student Name: Noah Bilmer
Lab section: 010
Assignemnt: Bonus Subnet Calculator
Python Version: 3.7.9
File: address.py

"""

from helpers import convertToBinary, convertToDecimal, 


class Address:
    """The address class keeps track of a four element list of decimal numbers and provides methods for 
    returning or setting the binary representation. If the binary representaton is set, numberList is updated to 
    reflect the correct representation.

    """   
    numberList = []

    def __init__(self, numberList):
        self.numberList = numberList

    def getAddressList(self):
        return self.numberList

    def setAddressList(self,numberList):
        self.numberList = numberList

    def getAddressListBinary(self):
        numListBinary = []
        for num in self.numberList:
            bit = convertToBinary(num)
            if len(bit) != 8:
                bit = ("0" * (8 - len(bit))) + bit
            numListBinary.append(bit)
        return numListBinary

    def setAddressListBinary(self,binaryAddressList):
        numList = []
        for num in binaryAddressList:
            numList.append(convertToDecimal(str(num)))
        self.numberList = numList

    def getClass(self):
        if self.numberList == None:
            return "unidentified"
        if self.numberList[0] in range(0,128):
            return "A"
        elif self.numberList[0] in range(127,192):
            return "B"
        elif self.numberList[0] in range(191,224):
            return "C"
        elif self.numberList[0] in range(223,240):
            return "D"
        elif self.numberList[0] in range(239,255):
            return "E"
        else:
            return "Unknown"
