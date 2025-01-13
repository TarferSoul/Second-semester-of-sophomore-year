.data
	array1:.word 1,-4,8,-9,5,6,-10,19,22,23
	array2:.word 121,-124,138,-199,255,2566,-1034,1019,2032,2033
	
	msg1: .asciiz "\n Sum of these positive odd values = "
	msg2: .asciiz "\n Sum of these negative even values = "
	
	.globl main
	
.text

main:
	# Print message for sum of positive odd values in array1
	li $v0, 4
	la $a0, msg1
	syscall

	# Initialize address entry parameters for array1
	la $a0, array1
	li $a1, 10
	jal FUNC

	# Print sum of positive odd values in array1
	move $a0, $s0
	li $v0, 1
	syscall

	# Print message for sum of negative even values in array1
	li $v0, 4
	la $a0, msg2
	syscall

	# Print sum of negative even values in array1
	move $a0, $s1
	li $v0, 1
	syscall

	# Print message for sum of positive odd values in array2
	li $v0, 4
	la $a0, msg1
	syscall

	# Initialize address entry parameters for array2
	la $a0, array2
	li $a1, 10
	jal FUNC

	# Print sum of positive odd values in array2
	move $a0, $s0
	li $v0, 1
	syscall

	# Print message for sum of negative even values in array2
	li $v0, 4
	la $a0, msg2
	syscall

	# Print sum of negative even values in array2
	move $a0, $s1
	li $v0, 1
	syscall

	# Exit the program
	li $v0, 10
	syscall

	# Function to calculate sum of positive odd and negative even numbers
	FUNC:
		# Initialize $s0 and $s1 to store the sums
  		  li $s0, 0
  		  li $s1, 0
	loop:
  	 	blez $a1, return # If counter is less than 1, return and exit loop
   		addi $a1, $a1, -1
    		lw $t0, 0($a0)
   		addi $a0, $a0, 4
   	 	bltz $t0, negative_even # Check if number is less than 0
    		bgtz $t0, positive_odd # Check if number is greater than 0
   		j loop

	negative_even:
		# Add negative even number to sum
    		andi $t1, $t0, 1
   	 	bne $t1, $0, loop
  	  	add $s1, $s1, $t0
  	  	j loop

	positive_odd:
		# Add positive odd number to sum
  	  	andi $t1, $t0, 1
   	 	beq $t1, $0, loop
   	 	add $s0, $s0, $t0
   	 	j loop

	return:
		jr $ra # Return
