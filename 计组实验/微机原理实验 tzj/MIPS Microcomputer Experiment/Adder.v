`timescale 1ns / 1ps
module Adder (In1,In2,Out);  
//加法器 Adder 将两个 n 位宽的数据相加，输出结果
    parameter n=32;
input [n-1:0] In1,In2;
output [n-1:0] Out;
assign Out =In1 +In2;

endmodule