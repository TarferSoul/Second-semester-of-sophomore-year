`timescale 1ns /1ps
module MIPSCPU (  //简单指令集MIPS微处理器
     input Clk,
     input Reset
     );
   wire [31:0] CurrentPC,SequencePC,JumpPC,BranchPC,TempPC,Boffset,Instr,MemData,Data2Reg,Res,RsData,RtData,ALUIn2,SignExtended;
   wire [1:0] ALUOp,PCsel;
   wire [4:0] WrAddr;
   wire J,B,RegDst,ALUSrc,RegWr,MemWr,Mem2Reg,Zero,BZero;
   wire [27:0] JumpTarget;
   wire [3:0] ALUCtr;
   
   PC U0_PC(TempPC, Clk, Reset, CurrentPC);
   InstrROM ROM_U0(CurrentPC[6:2],~Clk,Instr);
   defparam ROM_U0.n=5;
   Controller U2_Contr(Instr[31:26],Instr[5:0], J, B, RegDst, RegWr, ALUSrc, MemWr, Mem2Reg, ALUCtr);
   Mux2_1 U3(Instr[20:16], Instr[15:11],RegDst,WrAddr);
   defparam U3.n=5;
   LeftShift U4(Instr[25:0], JumpTarget);
   defparam U4.n=26,U4.m=28,U4.x=2;
   Adder U5(CurrentPC,'h4,SequencePC);
   defparam U5.n=32;
   Concat U6(SequencePC[31:28], JumpTarget, JumpPC);
   defparam U6.n=4,U6.m=28;
   Adder U7(SequencePC,Boffset,BranchPC);
   defparam U7.n=32;
   Mux3_1 U8(SequencePC, BranchPC,JumpPC,PCsel, TempPC);
   defparam U8.n=32;
   LeftShift U9(SignExtended, Boffset);
   defparam U9.n=32,U9.m=32,U9.x=2;
   RegFile RegFile_U1(Instr[25:21],Instr[20:16], WrAddr,Data2Reg, RegWr,Clk, RsData, RtData);
   SignedExtend U11(Instr[15:0], SignExtended);
   defparam U11.n=16,U11.m=32;
   Mux2_1 U12(RtData, SignExtended,ALUSrc,ALUIn2);
   defparam U12.n=32;
   ALU U13(RsData,ALUIn2,ALUCtr,Res,Zero);
   Mux2_1 U14(Res, MemData,Mem2Reg,Data2Reg);
   defparam U14.n=32;
   Concat U15(J, BZero, PCsel);
   defparam U15.n=1,U15.m=1;
   DataRAM RAM_U3(Res[6:2],RtData,MemWr,Clk, MemData);
   defparam RAM_U3.n=5,RAM_U3.m=32;
   and(BZero,B,Zero);
   
endmodule