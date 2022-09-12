"""Helpers file

This file contains various helper functions 

Student Name: Noah Bilmer
Lab section: 010
Assignemnt: Bonus Subnet Calculator
Python Version: 3.7.9
File: helpers.py

"""


def validateIpInput(ip):
    num = ""
    periodCount = 0
    numList = []
    for char in ip:
        if char.isnumeric():
            num += char
        elif char == ".":
            # If the user enters more than 4 period, just return the valid part of the ip.
            if periodCount == 4:
                return numList
            periodCount += 1
            if int(num) > 255:
                 numList.append(255);
            else:
                 numList.append(int(num));
            num = ""
        else:
            return None
    # Append the final number to the array
    if num.isnumeric() == False:
        return None
    if int(num) > 255:
        numList.append(255);
    else:
        numList.append(int(num));
    if periodCount != 3:
        return None
    else:
        return numList
    
def validateSubnetInput(subnet):
    if subnet[0] == "/":
        if len(subnet) < 3:
            stringNumber = subnet[1]
        else:
            stringNumber = subnet[1] + subnet[2]
        if stringNumber.isnumeric():
            if int(stringNumber) <= 32 and int(stringNumber) >= 8:
                return stringNumber
    return None

def convertSubenetToList(num):
    n = 0;
    ipList = []
    fullOctets = 0;
    while(n <= num):
        fullOctets += 1
        n += 8
    # our only number that is not 255
    num = num - (n - 8)
    for i in range(0,fullOctets - 1):
        ipList.append(255)
    finalNum = 0
    for i in range(0,num):
        finalNum += 2**(7 - i)   
    ipList.append(finalNum)
    while (len(ipList) < 4):
        ipList.append(0)
    # quick workarond for preventing 5 octet subnet masks
    if len(ipList) == 5:
        del ipList[4]
    return ipList

def convertToDecimal(binaryNum):
    binaryNum = str(binaryNum)
    exponent = len(binaryNum) - 1
    num = 0
    for bit in binaryNum:
        if bit == "1":
            num += 2**exponent
        exponent -= 1
    return num


def convertToBinary(num):
    str = "";
    while (int(num) != 0):
        num = int(num) / 2
        # If this number ends in .5
        if int(num) != num:
            # Build the string backwards
            str = "1" + str
        else:
            # Build the string backawrds
            str = "0" + str
    return str

def concatList(list):
    str = ""
    for string in list:
        str += string
    return str

def logicalAndTwoBinaryStrings(str1,str2):
    str = ""
    if len(str1) != len(str2):
        return "0"
    for i in range(0,len(str1)):
        if int(str1[i]) and int(str2[i]):
            str += "1" 
        else:
            str += "0" 
    return str

def listCpy(list):
    listCpy = []
    for i in range(len(list)):
        listCpy.append(list[i])
    return listCpy

def createAddressString(ipList, binary = False):
        ipStr = ""
        for i in range(0,len(ipList)):
            if i + 1 != len(ipList):
                # Awkward formatting logic for binary addresses
                if binary == True and i == 1:
                    ipStr += str(ipList[i])
                elif binary == True and i == 2:
                    ipStr += "." + ipList[i][0] + " " + str(ipList[i][1:]) + "."
                else:
                    ipStr += str(ipList[i]) + "."
            else:
                ipStr += str(ipList[i]) 
        return ipStr
