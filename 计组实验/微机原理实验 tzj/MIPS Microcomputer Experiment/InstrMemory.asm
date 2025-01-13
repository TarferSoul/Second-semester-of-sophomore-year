main:
add $4,$2,$3
lw $4,4($2)
sw $2,8($2)
sub $2,$4,$3
or  $2,$4,$3
and $2,$4,$3
slt $2,$4,$3
beq $4,$3,exit
j main
exit:lw $2,0($3)
j main