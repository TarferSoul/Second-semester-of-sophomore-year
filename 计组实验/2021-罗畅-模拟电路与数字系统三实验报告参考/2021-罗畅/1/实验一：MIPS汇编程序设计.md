# 实验一：MIPS汇编程序设计

专业班级：**提高2201班**

姓名：        **王翎羽**

学号：        **U202213806**

## 实验名称

MIPS汇编程序设计

## 实验目的：

1. 熟悉常见的MIPS汇编指令
2. 掌握MIPS汇编程序设计
3. 了解MIPS汇编语言与机器语言之间的对应关系
4. 了解C语言语句与汇编指令之间的关系
5. 掌握MARS的调试技术
6. 掌握程序的内存映像

## 实验仪器

***Mars MIPS汇编编译器***

## 实验任务

- 在数据段定义两个int型变量a, b;
- 在数据段定义一个int型数组c[40]，不初始化
- 通过系统调用功能从键盘输入a, b的值（不大于20）
- 采用MIPS汇编指令实现c[a+b] = a*b
- 通过系统调用功能分别显示c[a+b]所在的存储地址和值
- 指出程序运行后a, b, c[a+b]所在的数据段储存位置以及取值，验证程序功能的正确性

## 实验源代码

```mips
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

	# Initialize address entry parameters for array1
	la $a0, array1
	li $a1, 10
	jal FUNC

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

	# Initialize address entry parameters for array2
	la $a0, array2
	li $a1, 10
	jal FUNC

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

```

## 实验结果

### 程序代码段映像

![](1.png)  



### 输入输出端口测试

![Base/输入输出端口测试.png at master · HUSTerCH/Base · GitHub](https://github.com/HUSTerCH/Base/raw/master/circuitDesign/%E5%BE%AE%E6%9C%BA%E5%8E%9F%E7%90%86/ex1/%E8%BE%93%E5%85%A5%E8%BE%93%E5%87%BA%E7%AB%AF%E5%8F%A3%E6%B5%8B%E8%AF%95.png)

### 程序数据段映像

![Base/数据段映像1.png at master · HUSTerCH/Base · GitHub](https://github.com/HUSTerCH/Base/raw/master/circuitDesign/%E5%BE%AE%E6%9C%BA%E5%8E%9F%E7%90%86/ex1/%E6%95%B0%E6%8D%AE%E6%AE%B5%E6%98%A0%E5%83%8F1.png)

<img title="" src="https://github.com/HUSTerCH/Base/raw/master/circuitDesign/%E5%BE%AE%E6%9C%BA%E5%8E%9F%E7%90%86/ex1/%E6%95%B0%E6%8D%AE%E6%AE%B5%E6%98%A0%E5%83%8F2.png" alt="Base/数据段映像2.png at master · HUSTerCH/Base · GitHub" width="274">

### 结果分析

从I/O端口输入的数据正确的运算并存入了a、b、c[a+b]对应的内存映像中，实验正确

## 实验小结

   本次实验我使用了Mars软件进行汇编语言的练习，学会了使用syscall来进行数据的输入和输出，最后实验结果正确，收获很大！
