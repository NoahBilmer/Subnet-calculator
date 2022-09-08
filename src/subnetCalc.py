"""Subnet Calculator

This program accepts two command line arguments, an ipv4 address and
a subnet mask in the standard slash notation. The program validates both inputs
and prints out various information about the address.

Student Name: Noah Bilmer
Lab section: 010
Assignemnt: Bonus Subnet Calculator
Python Version: 3.7.9
File: subnetCalc.py

"""

from helpers import validateIpInput, validateSubnetInput, convertToBinary, convertSubenetToList, concatList, logicalAndTwoBinaryStrings,convertToDecimal
import sys
from address import Address

defaultSubnetMasks = {
    "A" : 8,
    "B" : 16,
    "C" : 24
}


WHITESPACE = 36
subnetMaskBitCount = 0

def main():
    # Validate input
    if (len(sys.argv) != 3):
        print("Usage: ./subnetCalc IPv4-Address subnet-mask-(slash-notation) ")
        exit(0)
    ipList = validateIpInput(sys.argv[1])
    ip = Address(validateIpInput(sys.argv[1]))
    ipClass = ip.getClass()
    if ipList == None:
        print("Invalid IPv4 Address, example: [192.168.2.1]")
        exit(0)
    subnetMaskBitCount = validateSubnetInput(sys.argv[2])
    if subnetMaskBitCount == None:
        print("Invalid subnet mask, use standard slash notation. Example: [/30], valid numbers are between 8 to 32")
        exit(0)
    # Create addresses for every field 
    subnetMaskBitCount = int(subnetMaskBitCount)
    subnetMaskList = convertSubenetToList(int(subnetMaskBitCount))
    subnet = Address(subnetMaskList)
    wildcard = Address(subnet.getAddressList())
    network = Address(ip.getAddressList())
    broadcast = Address(ip.getAddressList())
    HostMin = Address(ip.getAddressList())
    HostMax = Address(ip.getAddressList())

    # Do all of our calculations
    calculateWildCard(wildcard,subnetMaskBitCount)
    calculateNetwork(network,subnet)
    calculateBroadcast(broadcast,subnetMaskBitCount)
    subnetIndex = calculateSubnetIndex(ip,subnetMaskBitCount)
    calculateHostMin(HostMin,network)
    calculateHostMax(HostMax,broadcast)
    

    # Print out all of our data 
    printOutput("Address:  ", ip)
    printOutput("Netmask:  ",subnet, postDecimalText=" = " + str(subnetMaskBitCount))
    printOutput("Wildcard: ", wildcard)
    print("=>")
    list = network.getAddressList()
    list[3] -= 1
    network.setAddressList(list)
    printOutput("Subnet (Network): ", network, postDecimalText="/" + str(subnetMaskBitCount),postBinaryText=" (Class " + ipClass + ")")
    printOutput("Broadcast: ", add1(broadcast))
    HostMin = Address(HostMin.getAddressList())
   
    printOutput("HostMin (FHIP): ", add1(HostMin))
    printOutput("HostMax (LHIP): ", sub1(HostMax))
    s = subnetMaskBitCount - defaultSubnetMasks[ip.getClass()]
    h = 32 - subnetMaskBitCount
    if s > -1:
        print("s=" + str(s))
        print("S=" + str(2**s))
        print("h=" + str(h))
        print("Subnet Index (" + subnetIndex + ")" + " = " + str(convertToDecimal(subnetIndex)))
    else:
        print("h=" + str(h))
    print("HIPs Hosts/Net: " + str((2**h) - 2))

def calculateNetworkAddress(ip,mask):
    ipBinary = convertToBinary(ip)
    maskBinary = convertToBinary(mask)
    networkBinary = ""
    for Ipchar in ipBinary:
        for maskChar in maskBinary:
            networkBinary += int(maskChar and Ipchar)
    convertToDecimal(networkBinary)

def printOutput(text, address, postDecimalText="",postBinaryText=""):
    ipStr = text + createAddressString(address.getAddressList()) + postDecimalText
    binaryStr = createAddressString(address.getAddressListBinary()) + postBinaryText
    whitespace = WHITESPACE - len(ipStr)
    print(ipStr + (" " * whitespace) + binaryStr)

def createAddressString(ipList, binary = False):
    ipStr = ""
    for i in range(0,len(ipList)):
        if i + 1 != len(ipList):
            # Akward formatting logic for binary addresses
            if binary == True and i == 1:
                ipStr += str(ipList[i])
            elif binary == True and i == 2:
                ipStr += "." + ipList[i][0] + " " + str(ipList[i][1:]) + "."
            else:
                ipStr += str(ipList[i]) + "."
        else:
            ipStr += str(ipList[i]) 
    return ipStr

def ipToBinary(ipList):
    binaryIpList = []
    for num in ipList:
        binaryNum = convertToBinary(num)
        length = len(binaryNum)
        if length != 8:
            # add enough leading zeros
            binaryNum = ((8 - length) * "0") + binaryNum
        binaryIpList.append(binaryNum)
    return binaryIpList

def calculateWildCard(ip,subnetMaskBitCount):
    binaryNum = ""
    subnetBitCount = int(subnetMaskBitCount)
    wildCardBinaryList = []
    for octet in ip.getAddressListBinary():
        for i in range(0,len(octet)):
            subnetMaskBitCount -= 1
            if subnetMaskBitCount < 0:
                binaryNum += "1"
            else:
                binaryNum += "0" 
        wildCardBinaryList.append(binaryNum)
        binaryNum = ""
    ip.setAddressListBinary(wildCardBinaryList)

def calculateNetwork(ip,subnetMaskIp):
    ipBits = ip.getAddressListBinary()
    subnetBits = subnetMaskIp.getAddressListBinary()
    networkIpList = []
    str = ""
    for i in range(0,len(ipBits)):    
        networkIpList.append(logicalAndTwoBinaryStrings(ipBits[i],subnetBits[i]))  
    ip.setAddressListBinary(networkIpList)
    list = ip.getAddressList()
    ip.setAddressList(list)

def calculateBroadcast(broadcast,subnetMaskBitCount):
    broadcastBinary = broadcast.getAddressListBinary()
    broadcastList = []
    binaryNum = ""
    for i in range(0,len(broadcastBinary)):
        for j in range (0,8):
            subnetMaskBitCount -= 1
            if subnetMaskBitCount < 0:
                binaryNum += "1"
            else:
                binaryNum += broadcastBinary[i][j] 
        broadcastList.append(binaryNum)
        binaryNum = ""
    broadcast.setAddressListBinary(broadcastList)

def calculateHostMin(HostMin,networkAddress):
    list = networkAddress.getAddressList()
    list[3] += 1
    HostMin.setAddressList(list)

def calculateHostMax(HostMax,brodcastAddress):
    list = brodcastAddress.getAddressList()
    for i in range(0,len(list)):
        if int(list[i]) == 0:
            list[i] = 255
    list[3] -= 1
    HostMax.setAddressList(list)

def calculateSubnetIndex(ip,subnetMaskBitCount):
    dsm = defaultSubnetMasks[ip.getClass()]
    ipBinaryStr = concatList(ip.getAddressListBinary())
    str = ""
    for i in range(dsm,subnetMaskBitCount):
        str += ipBinaryStr[i]
    return str


def add1(addr):
    list = addr.getAddressList()
    list[3] += 1
    return addr

def sub1(addr):
    list = addr.getAddressList()
    list[3] -= 1
    return addr

main()