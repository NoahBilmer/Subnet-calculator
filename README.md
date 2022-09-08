# Subnet Calculator 
This application calculates information about a given IPv4 address and subnet mask.

# How to run this application 
1. Fork or download the app 
2. Navigaite to the /src directory with your terminal 
3. Run `python subnetCalc.py [IPv4 Address] [Subent Mask] `

# Example 
### Input 
`python subnetCalc.py 192.150.4.55 /16`
### Output:
Address:  192.150.4.55             11000000.10010110.00000100.00110111
Netmask:  255.255.0.0 = 16          11111111.11111111.00000000.00000000
Wildcard: 0.0.255.255               00000000.00000000.11111111.11111111
=>
Subnet (Network): 192.150.0.0/16    11000000.10010110.00000000.00000000 (Class C)
Broadcast: 192.150.255.255          11000000.10010110.11111111.11111111
HostMin (FHIP): 192.150.0.1         11000000.10010110.00000000.00000001
HostMax (LHIP): 192.150.255.254     11000000.10010110.11111111.11111110
h=16
HIPs Hosts/Net: 65534
