# Built-in/Generic Imports
import pytest
from typing import Union

# Local Functions
from ictoolkit.file.capture import capture_file_sections

# Local Dataclass
from ictoolkit.file.capture import ParseRipper, FindNStrip

__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_capture"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


def t1est_1_capture1():
    test_capture1 = """
    <ospf>
        <area>
            <name>0.0.0.0</name>
            <interface>
                <name>vlan.2</name>
            </interface>
            <interface>
                <name>vlan.129</name>
            </interface>
            <interface>
                <name>vlan.128</name>
                <passive>
                </passive>
            </interface>
            <interface>
                <name>vlan.3002</name>
            </interface>
        </area>
    </ospf>"""

    section_test: Union[
        list[dict[Union[int, str], Union[list[dict[Union[int, str], Union[str, None]]], None]]], None
    ] = capture_file_sections(
        my_list=test_capture1.splitlines(),
        strip=ParseRipper(
            start_detect="<ospf>",
            end_detect="</ospf>",
            find_n_strips=[
                # Replace Example:
                #   Original: <name>0.0.0.0/0</name>
                #   Replaced: 0.0.0.0/0
                FindNStrip(
                    group=1,
                    parent=True,
                    return_key="protocol_number_tag_name",
                    start_remove="<name>",
                    end_remove="</name>",
                    look_behind_minus_1="<area>",
                    required=True,
                ),
                # Replace Example:
                #   Original: <name>vlan.38</name>
                #   Replaced: vlan.38
                FindNStrip(
                    group=2,
                    parent=True,
                    return_key="vlan_number",
                    start_remove="<name>vlan.",
                    end_remove="</name>",
                    look_behind_minus_1="<interface>",
                ),
                # Replace Example:
                #   Original: </passive>
                #   Replaced: <>
                FindNStrip(
                    group=2,
                    parent=False,
                    return_key="passive",
                    start_remove="/passive",
                ),
            ],
        ),
    )

    print(section_test)


def t1est_2_capture1():
    test_capture1 = """
    <ethernet-switching-options>
        <voip>
            <interface>
                <name>ge-0/0/1.0</name>
                <vlan>VLAN_VOICE</vlan>
                <forwarding-class>expedited-forwarding</forwarding-class>
            </interface>
            <interface>
                <name>ge-0/0/3.0</name>
                <vlan>VLAN_VOICE</vlan>
                <forwarding-class>expedited-forwarding</forwarding-class>
            </interface>
            <interface>
                <name>ge-0/0/4.0</name>
                <vlan>VLAN_VOICE</vlan>
                <forwarding-class>expedited-forwarding</forwarding-class>
            </interface>
            <interface>
                <name>ge-0/0/5.0</name>
                <vlan>VLAN_VOICE</vlan>
                <forwarding-class>expedited-forwarding</forwarding-class>
            </interface>
            <interface>
                <name>ge-0/0/6.0</name>
                <vlan>VLAN_VOICE</vlan>
                <forwarding-class>expedited-forwarding</forwarding-class>
            </interface>
        </voip>
        <storm-control>
            <interface>
                <name>all</name>
            </interface>
        </storm-control>
    </ethernet-switching-options>"""

    section_test: Union[
        list[dict[Union[int, str], Union[list[dict[Union[int, str], Union[str, None]]], None]]], None
    ] = capture_file_sections(
        my_list=test_capture1.splitlines(),
        strip=ParseRipper(
            start_detect="<ethernet-switching-options>",
            end_detect="</ethernet-switching-options>",
            find_n_strips=[
                # Replace Example:
                #   Original: <name>ge-0/0/1.0</name>
                #   Replaced: ge-0/0/1.0
                FindNStrip(
                    group=2,
                    parent=True,
                    return_key="interface_name",
                    start_remove="<name>",
                    end_remove="</name>",
                    look_behind_minus_1="<interface>",
                    required=True,
                ),
                # Replace Example:
                #   Original: <vlan>VLAN_VOICE</vlan>
                #   Replaced: VLAN_VOICE
                FindNStrip(
                    group=2,
                    parent=False,
                    return_key="vlan_name",
                    start_remove="<vlan>",
                    end_remove="</vlan>",
                ),
                # Replace Example:
                #   Original: <forwarding-class>expedited-forwarding</forwarding-class>
                #   Replaced: <>
                FindNStrip(
                    group=2,
                    parent=False,
                    return_key="forwarding_class",
                    start_remove="<forwarding-class>",
                    end_remove="</forwarding-class>",
                ),
            ],
        ),
    )

    print(section_test)


def test_3_capture1():
    test_capture1 = """
    interface Port-channel1
     description TI-Netapp-Cluster1-01 - e0a & e0b
     switchport trunk allowed vlan 6-8,24,29,30,202
     switchport mode trunk
    !
    interface Port-channel2
     description TI-Netapp-Cluster1-02 - e0a & e0b
     switchport trunk allowed vlan 6-8,24,29,30,202
     switchport mode trunk
    !
    interface GigabitEthernet0/0
     vrf forwarding Mgmt-vrf
     no ip address
     negotiation auto
    !
    interface GigabitEthernet1/0/1
     description Front Room Port 1 (FireTV)
     switchport access vlan 62
     spanning-tree portfast
    !
    interface GigabitEthernet1/0/2
     description Front Room Port 2
     switchport access vlan 10
     spanning-tree portfast
    !
    interface GigabitEthernet1/0/3
     description Front Room Port 3 (Cisco AP)
     switchport access vlan 200
     switchport mode access
     spanning-tree portfast
    !
    interface GigabitEthernet1/0/4
     description Front Room Port 4 (Meraki AP)
     switchport trunk native vlan 200
     switchport trunk allowed vlan 10,11,18,200
     switchport mode trunk
     spanning-tree portfast
    !
    interface GigabitEthernet1/0/5
     description Front Room TV
     switchport access vlan 18
     spanning-tree portfast
    !
    interface GigabitEthernet1/0/6
     description Upstairs Bedroom P1
     switchport access vlan 10
    !
    interface GigabitEthernet1/0/7
     description Upstairs Bedroom P2
     switchport trunk native vlan 999
     switchport trunk allowed vlan 5,9-13,18,50,62,80,81,150,168,200,201,800,801
     switchport mode trunk
    !
    interface Vlan1
     no ip address
     shutdown
    !"""

    section_test: Union[
        list[dict[Union[int, str], Union[list[dict[Union[int, str], Union[str, None]]], None]]], None
    ] = capture_file_sections(
        my_list=test_capture1.splitlines(),
        strip=ParseRipper(
            start_detect="interface ",
            end_detect="!",
            find_n_strips=[
                # Replace Example:
                #   Original: interface GigabitEthernet1/0/7
                #   Replaced: GigabitEthernet1/0/7
                FindNStrip(
                    group="mygroup",
                    parent=True,
                    return_key="interface_name",
                    start_remove="interface ",
                    look_behind_minus_1="!",
                    required=True,
                ),
                # Replace Example:
                #   Original: description TI-Netapp-Cluster1-01 - e0a & e0b
                #   Replaced: TI-Netapp-Cluster1-01 - e0a & e0b
                FindNStrip(
                    group="mygroup",
                    parent=False,
                    return_key="description",
                    start_remove="description ",
                ),
                # Replace Example:
                #   Original: switchport access vlan 62
                #   Replaced: 62
                FindNStrip(
                    group="mygroup",
                    parent=False,
                    return_key="access_vlan",
                    start_remove="switchport access vlan ",
                ),
                # Replace Example:
                #   Original: switchport trunk allowed vlan 6-8,24,29,30,202
                #   Replaced: 6-8,24,29,30,202
                FindNStrip(
                    group="mygroup",
                    parent=False,
                    return_key="trunk_vlans",
                    start_remove="switchport trunk allowed vlan ",
                ),
            ],
            # exclude_values=["6-8,24,29,30,202"],
        ),
    )

    formatted_all_section_groups = None
    if section_test:
        formatted_all_section_groups = "  - parsed_data (list):" + str(
            "\n        - " + "\n        - ".join(map(str, section_test))
        )
    # print(formatted_all_section_groups)
