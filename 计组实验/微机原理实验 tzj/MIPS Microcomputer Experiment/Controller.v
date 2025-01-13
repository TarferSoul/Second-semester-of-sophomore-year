`timescale 1ns / 1ps
module Controller (OpCode, Funct, J, B, RegDst, RegWr, ALUSrc, MemWr, Mem2Reg, ALUCtr); //控制器
input [5:0] OpCode, Funct;
output J, B, RegDst, RegWr, ALUSrc, MemWr, Mem2Reg;
output [3:0] ALUCtr;
wire [1:0] ALUOp;

//引用主控制器 Mainctr 以及 ALU 控制器 ALUControl 实现对指令的操作码和功能码译码产生控制信号
MainCtr U0(OpCode,J, B, RegDst, RegWr, ALUSrc, MemWr, Mem2Reg, ALUOp);//主控制器第一级译码,得到ALUOp[1:0]
ALUControl U1(ALUOp, Funct, ALUCtr);  //ALU控制器第二级译码，产生ALUCtr[3:0]
endmodule