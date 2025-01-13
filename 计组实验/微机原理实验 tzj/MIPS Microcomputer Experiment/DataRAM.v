`timescale 1ns / 1ps
module DataRAM(Addr,DataIn,MemWR,Clk,DataOut);
//同步（时钟上升沿）输入\异步输出数据存储器 DataRAM，容量为 2n*m
parameter n=5,m=32;
reg [m-1:0] regs[2**n-1:0];
input [n-1:0] Addr;
input [m-1:0] DataIn;
input MemWR,Clk;
output [m-1:0] DataOut;
//地址线 Addr (位宽 n)、输入数据线 DataIn（位宽 m），写控制信号 MemWR(高电平有效)，同步时钟 Clk
//数据输出 DataOut（位宽 m，具有保持功能）

assign DataOut = regs[Addr];
always @ (posedge Clk)
begin
   if(MemWR)
   regs[Addr] <= DataIn;
end
endmodule