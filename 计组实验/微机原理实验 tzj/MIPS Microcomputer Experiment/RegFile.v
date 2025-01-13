`timescale 1ns / 1ps
module RegFile (RsAddr, RtAddr, WrAddr, DataIn, RegWr,Clk, RsData, RtData);
//同步输入\异步输出寄存器文件 RegFile，容量为 32*32，且编号为 0 的寄存器取值恒为 0
//输入引脚：Rs 寄存器编号 RsAddr (位宽 5)、Rt 寄存器编号 RtAddr (位宽 5)，写寄存器编号 WrAddr（(位宽 5)）输入数据线 DataIn（位宽
//32），写控制信号 RegWr（高电平有效），同步时钟 Clk
input [4:0] RsAddr,RtAddr, WrAddr;
input [31:0] DataIn;
input RegWr,Clk;
//输出引脚：Rs 寄存器数据 RsData（位宽 32），Rt 寄存器数据 RtData（位宽 32）
output [31:0] RsData, RtData;
reg [31:0] regs[31:0];

//R型指令执行时，首先根据指令字段Instr[25...21],Instr[20...16]获取$Rs,$Rt的值
assign RsData=RsAddr?regs[RsAddr]:0;
assign RtData=RtAddr?regs[RtAddr]:0;

always @(posedge Clk)
    if(RegWr)
    regs[WrAddr]=DataIn;
    
endmodule