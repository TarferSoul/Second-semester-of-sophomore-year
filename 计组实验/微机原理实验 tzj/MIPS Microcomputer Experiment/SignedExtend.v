`timescale 1ns / 1ps
module SignedExtend (In, Out);
//将 n 位符号数扩展为 m 位符号数模块 SignedExtend
    parameter n=16,m=32;
input [n-1:0] In;
output reg [m-1:0] Out;

integer i;

always @(In)
begin
if(In[n-1])    //有符号数则最高位补1
    
    for(i=n;i<m;i=i+1)
    Out[i]=1'b1;   
else
               //无符号数则最高位补0
    for(i=n;i<m;i=i+1)
    Out[i]=1'b0;
    Out[n-1:0]=In;
    
end
endmodule