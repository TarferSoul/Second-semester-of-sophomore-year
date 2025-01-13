module ALU( //32 位宽算术逻辑运算单元 ALU
    input signed [31:0] In1,
    input signed [31:0] In2,
    input [3:0] ALUCtr,
    //输入引脚：输入数据源 1-In1（32 位），输入数据源 2-In2（32 位），运算类型控制-ALUCtr（3 位）
    output reg [31:0] ALURes,
    output  Zero
    //输出引脚：运算结果 Res（32 位宽）
    );
//运算结果零标志 Zero（1 位，如果 Res 不为零 Zero 为 0，否则 Zero 为 1
assign Zero=(ALURes==0)?1:0;
    
always @(In1 or In2 or ALUCtr)
begin
     case(ALUCtr)
        4'b0110://sub
           begin
           ALURes = In1-In2;
           
           end
         4'b0010://add
           begin
           ALURes = In1+In2;
           
           end
         4'b0000://and
           begin
           ALURes = In1 & In2;
           
           end
          4'b0001://or
           begin
           ALURes = In1 | In2;
          
           end
          4'b0111://slt
           begin
           ALURes = (In1<In2)?1:0;
           
           end
          default:
            begin
            ALURes=0;
            
            end
       endcase
end
endmodule