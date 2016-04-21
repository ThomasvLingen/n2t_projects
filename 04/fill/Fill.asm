// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

    @SCREEN
    D=A                 // D = &SCREEN
    @8192
    D=D+A               // D = &SCREEN + 8192
    @max_screen_address
    M=D                 // max_screen_address = D

(RESET_CURRENT_SCREEN)
    @SCREEN
    D=A                 // D = &SCREEN
    @current_screen
    M=D                 // current_screen = D

(KEYBOARD_LOOP)
    @KBD
    D=M
    @FILL_SCREEN_BLACK
    D;JNE
    @FILL_SCREEN_WHITE
    D;JEQ

(FILL_SCREEN_BLACK)
    @current_screen
    D=M                 // D = current_screen
    @max_screen_address
    D=M-D               // D = max_screen_address - current_screen
    @RESET_CURRENT_SCREEN
    D;JLE               // Jump if D == 0 (aka if we've reached the last row!)
    @current_screen
    A=M
    M=-1
    @current_screen
    M=M+1
    @FILL_SCREEN_BLACK
    0;JMP

(FILL_SCREEN_WHITE)    
    @current_screen
    D=M                 // D = current_screen
    @max_screen_address
    D=M-D               // D = max_screen_address - current_screen
    @RESET_CURRENT_SCREEN
    D;JLE               // Jump if D == 0 (aka if we've reached the last row!)
    @current_screen
    A=M
    M=0
    @current_screen
    M=M+1
    @FILL_SCREEN_WHITE
    0;JMP

(END)
    @END
    0;JMP
