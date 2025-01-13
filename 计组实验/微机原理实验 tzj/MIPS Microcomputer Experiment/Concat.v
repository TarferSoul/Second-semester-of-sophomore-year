`timescale 1ns / 1ps
module Concat (In1, In2, Out);
//位拼接器 Concat 将输入源 In1（n 位），In2（m 位）拼接合成为 Out（n+m 位，且 In1 在高位部分，In2 在低位部分）
    parameter n=4,m=28;
input [n-1:0] In1;
input [m-1:0] In2;
output [n+m-1:0] Out;
assign Out = {In1,In2};

endmodule