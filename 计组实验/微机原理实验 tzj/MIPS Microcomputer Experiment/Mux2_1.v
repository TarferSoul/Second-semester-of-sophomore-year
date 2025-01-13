`timescale 1ns / 1ps
module Mux2_1 (In1, In2, sel, Out);  //多路复用器 Mux2_1
parameter n=32;
input [n-1:0] In1, In2;   //输入：In1（n 位），In2（n 位），sel
input sel;
output [n-1:0] Out;    //输出：Out（n 位）
//将两个 n 位宽的输入通道复用到一个输出同位宽通道，当 sel 为 0 时，选择 In1 输出，否则选择 In2 输出
assign Out = sel?In2:In1;
endmodule