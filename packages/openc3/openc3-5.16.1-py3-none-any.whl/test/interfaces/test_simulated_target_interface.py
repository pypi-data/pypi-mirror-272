# Copyright 2024 OpenC3, Inc.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# This file may also be used under the terms of a commercial license
# if purchased from OpenC3, Inc.

import unittest
from unittest.mock import *
from test.test_helper import *
from openc3.interfaces.simulated_target_interface import SimulatedTargetInterface
from openc3.packets.packet import Packet
from openc3.interfaces.protocols.protocol import Protocol


class MyProtocol(Protocol):
    data = None
    packet = None

    def read_data(self, data):
        MyProtocol.data = data
        return data

    def read_packet(self, packet):
        MyProtocol.packet = packet
        return packet


class TestSimulatedTargetInterface(unittest.TestCase):
    def setUp(self):
        mock_redis(self)
        setup_system()

    def test_complains_if_the_simulated_target_file_doesnt_exist(self):
        with self.assertRaisesRegex(
            ModuleNotFoundError, "No module named 'doesnt_exist'"
        ):
            SimulatedTargetInterface("doesnt_exist.py")

    def test_creates_the_simulated_target_class(self):
        si = SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py")
        self.assertEqual(si.sim_target_class.__name__, "SimTgtInst")

    def test_connection_string(self):
        si = SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py")
        self.assertEqual(si.connection_string(), "SimTgtInst")

    def test_connects_the_simulated_target(self):
        sti = SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py")
        sti.target_names = ["INST"]
        self.assertFalse(sti.connected())
        sti.connect()
        self.assertTrue(sti.connected())

    def test_read_complains_if_disconnected(self):
        with self.assertRaisesRegex(RuntimeError, "Interface not connected"):
            SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py").read()

    def test_read_returns_a_simulated_packet(self):
        sti = SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py")
        sti.target_names = ["INST"]
        sti.connect()
        pkt = sti.read()
        self.assertEqual(pkt.target_name, "INST")
        self.assertEqual(pkt.packet_name, "ADCS")
        pkt = sti.read()
        self.assertEqual(pkt.target_name, "INST")
        self.assertEqual(pkt.packet_name, "HEALTH_STATUS")

    def test_writes_into_a_pkt(self):
        packet = System.telemetry.packet("INST", "HEALTH_STATUS")
        packet.write("ground1status", "CONNECTED")
        self.assertEqual(packet.read("ground1status"), "CONNECTED")
        packet.write("ground1status", "UNAVAILABLE")
        self.assertEqual(packet.read("ground1status"), "UNAVAILABLE")

    def test_write_complains_if_disconnected(self):
        with self.assertRaisesRegex(RuntimeError, "Interface not connected"):
            SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py").write(None)

    def test_writes_commands_to_the_simulator(self):
        sti = SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py")
        sti.target_names = ["INST"]
        sti.connect()
        sti.write(Packet("INST", "ABORT"))
        self.assertEqual(sti.sim_target.packet.target_name, "INST")
        self.assertEqual(sti.sim_target.packet.packet_name, "ABORT")

    def test_write_raw_raises_an_exception(self):
        with self.assertRaisesRegex(RuntimeError, "not implemented"):
            SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py").write_raw("")

    def test_disconnects_from_the_simulator(self):
        sti = SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py")
        sti.target_names = ["INST"]
        self.assertFalse(sti.connected())
        sti.connect()
        self.assertTrue(sti.connected())
        sti.disconnect()
        self.assertFalse(sti.connected())

    def test_handles_packet_protocols(self):
        sti = SimulatedTargetInterface("test/interfaces/sim_tgt_inst.py")
        sti.target_names = ["INST"]
        sti.add_protocol(MyProtocol, [], "READ_WRITE")
        sti.connect()
        pkt = sti.read()
        self.assertEqual(MyProtocol.packet, pkt)
