# $language = "Python3"
# $interface = "1.0"

import json
import re
import os


def run_command(command: str, tab: object) -> list:
    tab.Screen.Send(command + "\n")
    return tab.Screen.ReadString(["# ", "#"], 15).split("\n")[1:-1]


def return_string(command: str, tab: object) -> str:
    """output is converted string and returned"""
    return "\n".join(run_command(command, tab))


def get_cdp_neighbors(tab: object, neighbors: dict):

    tab.Screen.Synchronous = True
    tab.Activate()
    tab.Screen.Send("terminal length 0\n")
    tab.Screen.ReadString(["# ", "#"], 15)

    my_hostname = return_string("show startup-config | include ^hostname", tab)
    my_hostname = my_hostname.replace("hostname ", "").split(".")[0].strip()
    if not my_hostname in neighbors:
        neighbors[my_hostname] = {}

    output = return_string("show cdp neighbors detail", tab)
    cdp_neighbors = output.split("-------------------------")[1:]

    for neighbor in cdp_neighbors:

        """Get neighbor data"""
        nbr_hostname = re.findall("Device ID:\s?(\S+)", neighbor)[0].split(".")[0]
        nbr_hostname.strip()
        nbr_platform = re.findall("Platform: (.+),", neighbor)[0]
        my_port = re.findall("Interface: (\S+),", neighbor)[0]
        nbr_port = re.findall("outgoing port\): (\S+)", neighbor)[0]

        """Add neighbor data to neighbors"""

        if not nbr_hostname in neighbors:
            neighbors[nbr_hostname] = {}

        neighbors[nbr_hostname]["platform"] = nbr_platform

        if my_hostname < nbr_hostname:

            if not "neighbors" in neighbors[my_hostname]:
                neighbors[my_hostname]["neighbors"] = {}

            if not nbr_hostname in neighbors[my_hostname]["neighbors"]:
                neighbors[my_hostname]["neighbors"][nbr_hostname] = {"interfaces": []}

            port_combo = f"{my_port} <> {nbr_port}"
            if not port_combo in neighbors[my_hostname]["neighbors"][nbr_hostname]["interfaces"]:
                neighbors[my_hostname]["neighbors"][nbr_hostname]["interfaces"].append(port_combo)

        elif nbr_hostname < my_hostname:

            if not "neighbors" in neighbors[nbr_hostname]:
                neighbors[nbr_hostname]["neighbors"] = {}

            if not my_hostname in neighbors[nbr_hostname]["neighbors"]:
                neighbors[nbr_hostname]["neighbors"][my_hostname] = {"interfaces": []}

            port_combo = f"{nbr_port} <> {my_port}"
            if not port_combo in neighbors[nbr_hostname]["neighbors"][my_hostname]["interfaces"]:
                neighbors[nbr_hostname]["neighbors"][my_hostname]["interfaces"].append(port_combo)

    return neighbors


def write_cdp_output_to_json(json_file_path: str):

    neighbors = {}
    if os.path.exists(json_file_path):
        BUTTON_YESNOCANCEL = 3
        DEFBUTTON2 = 256
        IDYES = 6
        IDNO = 7
        IDCANCEL = 2
        result = crt.Dialog.MessageBox(
            "Neighbors file already exist.\nClick Yes to remove file and start from scratch.",
            "Remove file?",
            BUTTON_YESNOCANCEL | DEFBUTTON2,
        )
        if result == IDCANCEL:
            return
        elif result == IDNO:
            with open(json_file_path, "r") as json_file:
                neighbors = json.loads(json_file.read())
        elif result == IDYES:
            os.remove(json_file_path)

    tabs = crt.GetTabCount()
    for tab_id in range(tabs):

        tab_id += 1
        if tab_id > tabs:
            continue

        tab = crt.GetTab(tab_id)
        if tab.Caption == "Script Tab":
            return

        neighbors = get_cdp_neighbors(tab, neighbors)

        with open(json_file_path, "w") as json_file:
            json_file.write(json.dumps(neighbors, indent=2, sort_keys=True))


def parse_json_to_drawio_csv(json_file_path: str, csv_file_path: str):

    try:
        with open(json_file_path, "r") as json_file:
            nodes = json.loads(json_file.read())
    except FileNotFoundError:
        return

    settings = """##
## Import me into Draw.io / app.diagrams.net by copying the text in this file.
## Then open the program and go to Arrange -> Insert -> Advanced -> CSV
## Clear all the text in the box and replace it with the text you copied here.
## File should now load with your topology displayed!
# stylename: platform
# width: 40
# height: 40
# styles: {\\
# "N5K": "shape=mxgraph.cisco19.rect;prIcon=nexus_7k;fillColor=#FAFAFA;strokeColor=#005073;align=center;verticalAlign=top;labelPosition=center;verticalLabelPosition=bottom;", \\
# "SWITCH": "labelPosition=right;shape=mxgraph.cisco19.rect;prIcon=l2_switch;fillColor=#FAFAFA;strokeColor=#005073;align=center;verticalAlign=top;labelPosition=center;verticalLabelPosition=bottom;", \\
# "VMWARE": "verticalLabelPosition=bottom;html=1;verticalAlign=top;aspect=fixed;align=center;pointerEvents=1;shape=mxgraph.cisco19.rect;prIcon=hypervisor;fillColor=#FAFAFA;strokeColor=#005073;", \\
# "LINUX": "verticalLabelPosition=bottom;html=1;verticalAlign=top;aspect=fixed;align=center;pointerEvents=1;shape=mxgraph.cisco19.rect;prIcon=database_relational;fillColor=none;strokeColor=none;", \\
# "ROUTER": "verticalLabelPosition=bottom;html=1;verticalAlign=top;aspect=fixed;align=center;pointerEvents=1;shape=mxgraph.cisco19.rect;prIcon=router;fillColor=#FAFAFA;strokeColor=#005073;", \\
# "L3_SWITCH": "verticalLabelPosition=bottom;html=1;verticalAlign=top;aspect=fixed;align=center;pointerEvents=1;shape=mxgraph.cisco19.rect;prIcon=l3_switch;fillColor=#FAFAFA;strokeColor=#005073;", \\
# "ISE": "verticalLabelPosition=bottom;html=1;verticalAlign=top;aspect=fixed;align=center;pointerEvents=1;shape=mxgraph.cisco19.rect;prIcon=ise;fillColor=#FAFAFA;strokeColor=#005073;"}
# levelspacing: 40
# edgespacing: 40
# connect: {"from":"neighbors", "to":"node", "style": "curved=0;endArrow=0;endFill=1;"}
"""
    headers = "node,platform,neighbors\n"
    data = ""

    for node in nodes:

        platform = ""
        if "platform" in nodes[node]:

            if "N5K-" in nodes[node]["platform"]:
                platform = "N5K"

            elif "N3K-" in nodes[node]["platform"]:
                platform = "SWITCH"

            elif "C3850" in nodes[node]["platform"]:
                platform = "L3_SWITCH"

            elif "C3750" in nodes[node]["platform"]:
                platform = "L3_SWITCH"

            elif "CISCO" in nodes[node]["platform"]:
                platform = "ROUTER"

            elif " ASR" in nodes[node]["platform"]:
                platform = "ROUTER"

            elif " ISR" in nodes[node]["platform"]:
                platform = "ROUTER"

            elif "VMware " in nodes[node]["platform"]:
                platform = "VMWARE"

            elif nodes[node]["platform"] == "Linux":
                platform = "LINUX"

            elif nodes[node]["platform"] == "ISE-VM-K9":
                platform = "ISE"

        """Combine neighbors into a comma-separated string"""
        neighbors = ""
        if "neighbors" in nodes[node]:
            neighbors = []
            for neighbor in nodes[node]["neighbors"]:
                neighbors.append(neighbor)
            neighbors = "'" + ",".join(neighbors) + "'"

        node_data = f"{node},{platform},{neighbors}\n"
        data += node_data

    with open(csv_file_path, "w") as csv_file:
        csv_file.write(settings)
        csv_file.write(headers)
        csv_file.write(data)


def main():

    json_file_path = f"{os.getenv('APPDATA')}\cdp.json"
    csv_file_path = f"{os.getenv('APPDATA')}\cpd.txt"

    write_cdp_output_to_json(json_file_path)
    parse_json_to_drawio_csv(json_file_path, csv_file_path)

    crt.Dialog.MessageBox(f"Open the file '{csv_file_path}' and read the instructions for importing to Draw.io.")


main()
