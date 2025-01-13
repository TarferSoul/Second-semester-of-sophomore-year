`timescale 1ns / 1ps
module MainCtr(OpCode,J, B, RegDst, RegWr, ALUSrc, MemWr, Mem2Reg, ALUOp);//主控制器 Mainctr
input [5:0] OpCode;
output J, B, RegDst, RegWr, ALUSrc, MemWr, Mem2Reg;
output [1:0] ALUOp;
reg [8:0] temp;

assign{J, B, RegDst, RegWr, ALUSrc, MemWr, Mem2Reg, ALUOp}=temp;

always @(OpCode)   //对6位操作码Op[5:0]进行译码
case(OpCode)
     6'b000000:temp=9'b001100010;
     6'b100011:temp=9'b000110100;
     6'b101011:temp=9'b00x011x00;
     6'b000100:temp=9'b01x000x01;
     6'b000010:temp=9'b1xx0x0xxx;
     default:temp=9'b000000000;
endcase

endmodule