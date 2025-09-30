# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import ReadOnly

async def reset_dut(dut, cycles=5):
    """Reset helper (active-low reset)."""
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, cycles)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start testbecnh of 8-bit programmable counter")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Init signals
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uo_out.value = 0
    dut.uio_in.value = 0
    await reset_dut(dut)
    
    # TASK 1 : RUN NORMAL TEST FROM 0 TO 325
    dut._log.info("TASK 1: Counting up 0 to 325")
    dut.uio_in.value = 0b1010    # tri_state_en = 1, enable = 1, dir = 0 (up), load  =0

    await ClockCycles(dut.clk, 1)
    for i in range (325):
        assert dut.uo_out.value.integer == i % 256, f"Expected {i} and got {dut.uo_out.value.integer}"
        await ClockCycles(dut.clk, 1)
    
    # TASK 2: RESET
    dut._log.info("TASK 2: Resetting")
    await reset_dut(dut)

    # TASK 3: LOAD 72 THEN GOES UP TO 97
    dut._log.info("TASK 3: Load 71, then count up to 97")
    dut.ui_in.value = 71
    dut.uio_in.value = 0b1001    # tri_state_en = 1, enable = 0, dir = 0 (up), load = 1
    await ClockCycles(dut.clk, 1)
    await ReadOnly()
    await ClockCycles(dut.clk, 1)
    
    dut.uio_in.value = 0b1010    # tri_state_en = 1, enable = 1, dir = 0 (up), load = 0
    assert dut.uo_out.value.integer == 71 % 256, f"Expected {71} and got {dut.uo_out.value.integer}"
    await ReadOnly()
    await ClockCycles(dut.clk, 1)
    
    for i in range(71, 97):
        cocotb.log.info(dut.uo_out.value.integer)
        assert dut.uo_out.value.integer == i % 256, f"Expected {i} and got {dut.uo_out.value.integer}"
        await ClockCycles(dut.clk, 1)

    # TASK 4: CHANGE DIRECTION TO COUNT DOWN UNTIL 80
    dut._log.info("TASK 4: Counting down until 80")
    dut.uio_in.value = 0b1110    # Enable = 1, dir = 1, tri_state = 1
    await ReadOnly()
    # await ClockCycles(dut.clk, 1)
    for i in range(97, 80, -1):
        assert dut.uo_out.value.integer == i % 256, f"Expected {i} and got {dut.uo_out.value.integer}"
        await ClockCycles(dut.clk, 1)

    # TASK 5: TURN TRI-STATE OUTPUT TO Z
    dut._log.info("TASK 5: Tri-state output to z")
    dut.uio_in.value = 0b0110 # enable = 1, dir = 1, tri_state = 0
    await ClockCycles(dut.clk, 5) # Output Z 5 clock cycles
    assert dut.uo_out.vale.is_resolvable is False, "Output should be Z"

    # TASK 6: LOAD 38 AND RUN UP TO 57
    dut._log.info("TASK 6: Load 38, then count up to 57")
    dut.ui_in.value = 38
    dut.uio_in.value = 0b1001
    await ClockCycles(dut.clk, 1)
    await ReadOnly()
    await ClockCycles(dut.clk, 1)
    
    dut.uio_in.value = 0b1010    # tri_state_en = 1, enable = 1, dir = 0 (up), load = 0
    assert dut.uo_out.value.integer == 38 % 256, f"Expected {38} and got {dut.uo_out.value.integer}"
    await ReadOnly()
    await ClockCycles(dut.clk, 1)
    
    for i in range(39, 57):
        assert dut.uo_out.value.integer == i % 256, f"Expected {i} and got {dut.uo_out.value.integer}"
        await ClockCycles(dut.clk, 1)

    dut._log.info("Test completed")

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
