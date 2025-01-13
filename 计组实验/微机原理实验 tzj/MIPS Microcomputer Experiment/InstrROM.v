`timescale 1ns / 1ps
module InstrROM(Addr,Clk,Instr);  //输出指令存储器 InstrROM，容量为 2n*32
parameter n=5;
input [n-1:0] Addr;  //输入引脚：地址线 Addr (位宽 n)、同步时钟 Clk
input Clk;
output reg [31:0] Instr;  //输出引脚：指令 Instr（位宽 32，具有保持功能）
reg [31:0] regs[2**n-1:0];

always @ (posedge Clk)
Instr = regs[Addr];     //时钟上升沿输出相应地址的指令
endmodule