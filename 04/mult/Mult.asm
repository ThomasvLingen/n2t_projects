// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    @0
    D=M                 // D = R0
    @times_to_add
    M=D                 // times_to_add = D
    @2
    M=0                 // R2 = 0
    @END                
    D;JEQ               // goto END if D == 0

(ADD_ONCE)
    @1
    D=M                 // D = R1
    @2
    M=M+D               // R2 += D
    @times_to_add
    M=M-1               // times_to_add -= 1
    D=M                 // D = time_to_add
    @ADD_ONCE
    D;JGT               // goto ADD_ONCE if D > 0
(END)
    @END
    0;JMP

