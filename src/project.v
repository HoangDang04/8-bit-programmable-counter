/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
	input  wire [7:0] ui_in,    // Dedicated inputs (this is my load value to get the value of the things)
	output wire [7:0] uo_out,   // Dedicated outputs (this is my output of the counter value of x amount of clock cycles)
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);
	// So this is my counter to save the state of the counter right now
    reg[7:0] counter;

	// There are 3 main signals: load to load the counter, enable to keep counting and dir to check if it is going up or down
    wire load = uio_in[0];
    wire enable = uio_in[1];
    wire dir = uio_in[2];
	wire tri_state_en = uio_in[3];

	// Counter logic
	always @(posedge clk or negedge rst_n) begin
		if(!rst_n)
			counter <= 8'b0;
		else if (load)
			counter <= ui_in;	// Load the input value right now
		else if (enable) begin	// Enable the system
			if(direction)
				counter <= counter - 1'b1;
			else
				counter <= counter + 1'b1;
		end
	end

	// If the tri_state_en is on then used the counter
	assign uo_out = (tri_state_en) ? counter : 8'bz;

  // List all unused inputs to prevent warnings
	wire _unused = &{ena, uio_out, uio_oe, 1'b0};

endmodule
