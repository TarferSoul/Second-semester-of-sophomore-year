`timescale 1ns / 1ps
module LeftShift (In, Out);
//左移运算器 LeftShift 将 n 位数据左移 x 位(低位补充 0，高位移出)输出 m 位数据
    parameter n=32,m=32,x=2;
input  [n-1:0] In;
output [m-1:0] Out;
assign Out =In << x;
endmodule