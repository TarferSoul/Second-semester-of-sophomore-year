li $v0,5
syscall

addi $a0,$v0,0  # N
li $t1,2
addi $t0,$a0,1  #get n+1
mult $a0,$t0    #multiply n  and (n+1)
mflo $t2        #get n*(n+1)
div $t2,$t1     #div 2
mflo $t3        #get the result 

li $v0,1
addi $a0,$t3,0
syscall         #get the output

addi $v0,$t3,0  #save the result 


