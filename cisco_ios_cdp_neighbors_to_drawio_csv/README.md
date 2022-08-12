# What is this?
This is a script for graphing all CDP neighbors in a network and create a topology diagram in https://app.diagrams.net/.

The script currently supports running on Cisco IOS and NXOS devices.

# How does it work?
The script is run from SecureCRT. The script will loop through all open tabs and run the "show cdp neighbors detail" command to get all of the device CDP neighbors.
Using this input, the script then creates a txt-file, allowing you to copy its contents and paste it into digrams.net to automatically create a network topology diagram.

# Requirements
1. You need to have all Cisco devices opened in their own tabs in SecureCRT. So if you have two routers and five switches, you need one tab open to each device.
2. SecureCRT must be able to run Python3: https://forums.vandyke.com/showthread.php?t=14295
3. You must be using a Windows PC

# Example output
You can paste the contents below in diagrams.net to see what the end result would look like:

    ##
    ## Import me into Draw.io / app.diagrams.net by copying the text in this file.
    ## Then open the program and go to Arrange -> Insert -> Advanced -> CSV
    ## Clear all the text in the box and replace it with the text you copied here.
    ## File should now load with your topology displayed!
    # stylename: platform
    # width: 40
    # height: 40
    # styles: {\
    # "N5K": "shape=mxgraph.cisco19.rect;prIcon=nexus_7k;fillColor=#FAFAFA;strokeColor=#005073;align=center;verticalAlign=top;labelPosition=center;verticalLabelPosition=bottom;", \
    # "SWITCH": "labelPosition=right;shape=mxgraph.cisco19.rect;prIcon=l2_switch;fillColor=#FAFAFA;strokeColor=#005073;align=center;verticalAlign=top;labelPosition=center;verticalLabelPosition=bottom;", \
    # "LINUX": "verticalLabelPosition=bottom;html=1;verticalAlign=top;aspect=fixed;align=center;pointerEvents=1;shape=mxgraph.cisco19.rect;prIcon=database_relational;fillColor=none;strokeColor=none;"}
    # levelspacing: 40
    # edgespacing: 40
    # connect: {"from":"neighbors", "to":"node", "style": "curved=0;endArrow=0;endFill=1;"}
    node,platform,neighbors
    SPINE1,N5K,'LEAF1A,LEAF1B,LEAF2A,LEAF2B,LEAF3A,LEAF3B'
    SPINE2,N5K,'LEAF1A,LEAF1B,LEAF2A,LEAF2B,LEAF3A,LEAF3B'
    LEAF1A,N5K,''
    LEAF1B,N5K,''
    LEAF2A,SWITCH,''
    LEAF2B,SWITCH,''
    LEAF3A,N5K,''
    LEAF3B,N5K,''
    SERVER11,LINUX,'LEAF1A,LEAF1B'
    SERVER12,LINUX,'LEAF1A,LEAF1B'
    SERVER13,LINUX,'LEAF1A,LEAF1B'
    SERVER14,LINUX,'LEAF1A,LEAF1B'
    SERVER15,LINUX,'LEAF1A,LEAF1B'
    SERVER21,LINUX,'LEAF2A,LEAF2B'
    SERVER22,LINUX,'LEAF2A,LEAF2B'
    SERVER23,LINUX,'LEAF2A,LEAF2B'
    SERVER24,LINUX,'LEAF2A,LEAF2B'
    SERVER25,LINUX,'LEAF2A,LEAF2B'
    SERVER31,LINUX,'LEAF3A,LEAF3B'
    SERVER33,LINUX,'LEAF3A,LEAF3B'
    SERVER33,LINUX,'LEAF3A,LEAF3B'
    SERVER34,LINUX,'LEAF3A,LEAF3B'
    SERVER35,LINUX,'LEAF3A,LEAF3B'
