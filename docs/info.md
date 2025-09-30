<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements an **8-bit programmable binary counter** with the following features:

- **Asynchronous reset (`rst_n`)**: clears the counter immediately when asserted low.  
- **Synchronous load (`uio_in[0]`)**: loads an external value from `ui_in` into the counter on the next rising clock edge.  
- **Enable (`uio_in[1]`)**: when high, the counter updates on each rising clock edge. When low, the counter holds its value.  
- **Direction (`uio_in[2]`)**: selects counting direction. `0` = up, `1` = down.  
- **Tri-state output enable (`uio_in[3]`)**: when high, the counter value is driven to `uo_out`. When low, the outputs are set to high impedance (`Z`).  

The counter value is visible on the 8-bit dedicated output bus `uo_out` whenever tri-state is enabled.  
Unused IO signals (`uio_out`, `uio_oe`) are tied off.  

---

## How to test

1. **Reset the counter**  
   - Drive `rst_n = 0` for a few clock cycles, then release (`rst_n = 1`).  
   - The counter value will reset to `0`.  

2. **Load a value**  
   - Apply the desired value to `ui_in`.  
   - Assert `uio_in[0] = 1` (load).  
   - On the next clock, the counter loads `ui_in` into its register.  
   - Deassert `uio_in[0] = 0` after loading.  

3. **Count up or down**  
   - Set `uio_in[1] = 1` (enable).  
   - Choose direction: `uio_in[2] = 0` (up) or `uio_in[2] = 1` (down).  
   - Ensure `uio_in[3] = 1` so outputs are visible.  
   - The counter will increment or decrement on each rising clock edge.  

4. **Tri-state the output**
