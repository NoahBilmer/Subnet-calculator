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

from helpers import validateIpInput, validateSubnetInput, convertToBinary, convertSubenetToList, concatList, logicalAndTwoBinaryStrings,convertToDecimal,listCpy,createAddressString

import sys
from address import Address

# default subnet mask dictionary
defaultSubnetMasks = {
    "A" : 8,
    "B" : 16,
    "C" : 24
}

# Whitespace constant, affects the space between the decimal and binary representations
WHITESPACE = 36
# subnet mask in slash notation, (which is the amount of bits in the mask)
subnetMaskBitCount = 0

def main():
    """Entry point for the program
    """    
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
    printOutput("Subnet (Network): ", network, postDecimalText="/" + str(subnetMaskBitCount),postBinaryText=" (Class " + ipClass + ")")
    printOutput("Broadcast: ", (broadcast))
    # if the network address and brodcast address is the same than there is only 1 possible ip for this subnet, thus first host and last host don't really make sense.
    if not(network.getAddressList() == broadcast.getAddressList()):
        printOutput("HostMin (FHIP): ", HostMin)
        printOutput("HostMax (LHIP): ", HostMax)
    s = subnetMaskBitCount - defaultSubnetMasks[ip.getClass()]
    h = 32 - subnetMaskBitCount
    if s > -1:
        print("s=" + str(s))
        print("S=" + str(2**s))
        print("h=" + str(h))
        print("Subnet Index (" + subnetIndex + ")" + " = " + str(convertToDecimal(subnetIndex)))
    else:
        print("h=" + str(h))
    HIP = (2**h) - 2
    if HIP <= 0:
        HIP = 1
    print("HIPs Hosts/Net: " + str(HIP))


def printOutput(text, address, postDecimalText="",postBinaryText=""):
    """Prints one line of output, will print both binary and decimal notations of an ip.

    Args:
        text (str): the text to output
        address (Address): 
        postDecimalText (str, optional): the text to addright after the decimal representation. Defaults to "".
        postBinaryText (str, optional): the text to add right after the binary representation.  Defaults to "".
    """    
    ipStr = text + createAddressString(address.getAddressList()) + postDecimalText
    binaryStr = createAddressString(address.getAddressListBinary()) + postBinaryText
    whitespace = WHITESPACE - len(ipStr)
    print(ipStr + (" " * whitespace) + binaryStr)
    

def calculateWildCard(wildCard,subnetMaskBitCount):
    binaryNum = ""
    subnetBitCount = int(subnetMaskBitCount)
    wildCardBinaryList = []
    # for each octet
    for octet in wildCard.getAddressListBinary():
        for i in range(0,len(octet)):
            subnetMaskBitCount -= 1
            if subnetMaskBitCount < 0:
                binaryNum += "1"
            else:
                binaryNum += "0" 
        wildCardBinaryList.append(binaryNum)
        binaryNum = ""
    wildCard.setAddressListBinary(wildCardBinaryList)

def calculateNetwork(network,subnetMaskIp):
    """Calculates the network address of the given ip and given subnet mask. 

    Args:
        network (Address): The given ip, this is the object that gets mutated.
        subnetMaskIp (Address): The given subnetmask, this will remain unchanged.
    """  
    ipBits = network.getAddressListBinary()
    subnetBits = subnetMaskIp.getAddressListBinary()
    networkIpList = []
    str = ""
    for i in range(0,len(ipBits)):    
        networkIpList.append(logicalAndTwoBinaryStrings(ipBits[i],subnetBits[i]))  
    network.setAddressListBinary(networkIpList)
    list = network.getAddressList()
    network.setAddressList(list)

def calculateBroadcast(broadcast,subnetMaskBitCount):
    """Calculates broadcast address

    Args:
        broadcast (Address): The given ip, this is the object that gets mutated.
        subnetMaskBitCount (): The given subnetmask, this will remain unchanged.
    """    
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
    """Calculates the minimum host address from the network address

    Args:
        HostMin (Address): the address object to store the HostMin object inside
        networkAddress (Address): the network address of the subnet 
    """    
    list = networkAddress.getAddressList()
    # edit a copy of the networkAddressList
    list = listCpy(list)
    # 
    list[3] += 1
    if list[3] > 255:
        list[3] = 255
    HostMin.setAddressList(list)

def calculateHostMax(HostMax,brodcastAddress):
    """Calculates the maximum host address from the brodcast address

    Args:
        HostMax (Address): the address object to store the HostMax address inside
        brodcastAddress (Address): the brodcast address of the subnet
    """    
    list = brodcastAddress.getAddressList()
     # edit a copy of the networkAddressList
    list = listCpy(list)
    for i in range(0,len(list)):
        if int(list[i]) == 0:
            list[i] = 255
    list[3] -= 1
    HostMax.setAddressList(list)

def calculateSubnetIndex(ip,subnetMaskBitCount):
    """Calculates subnet index.

    Args:
        ip (Address): the ip address to caclulate the subnet index from.
        subnetMaskBitCount (int): Subnet mask in slash notation (or the number of 1s in the subnet mask.)

    Returns:
        str: the subnet index, in binary, in the form of a string.
    """ 
    # default subnet mask   
    dsm = defaultSubnetMasks[ip.getClass()]
    ipBinaryStr = concatList(ip.getAddressListBinary())
    str = ""
    # get the bits between the DSM and the subnet mask
    for i in range(dsm,subnetMaskBitCount):
        str += ipBinaryStr[i]
    return str


# Run the program
main()