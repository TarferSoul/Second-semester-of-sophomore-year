# 实验三：并行IO接口设计

专业班级：**提高2202班**
姓名：        **王翎羽**
学号：        **U202213806**

## 实验名称

并行IO接口设计

## 实验目的

- 掌握GPIO IP核的工作原理和使用方法
- 掌握中断控制方式的IO接口设计原理
- 掌握中断程序设计方法
- 掌握IO接口程序控制方法

## 实验仪器

***Vivado 2023.2、Vitis 2023.2***

## 实验任务

- 所有实验任务要求分别采用程序控制方式、普通中断方式、快速中断方式实现，中断方式时，GPIO输入、延时都采用中断实现。
  
  嵌入式计算机系统将独立按键以及独立开关作为输入设备，LED 灯作为输出设备。修改实验示例程序代码，实现以下功能：
  
  1） 按下BTNC 按键时，计算机读入一组16 位独立开关状态作为第一个输入的二进制数据，并即时显示输入的二进制数到16 位LED 灯上。（没有按下BTNC按键时，开关拨动不读入数据）
  
  2） 按下BTNR 按键时，计算机读入另一组16 位独立开关状态作为第二个输入的二进制数据，并即时显示输入的二进制数到16 位LED 灯上。（没有按下BTNR按键时，开关拨动不读入数据）
  
  3） 按下BTNU 按键时，将保存的2 组二进制数据做无符号加法运算，并将运算结果输出到LED 灯对应位。
  
  4） 按下BTND 按键时，将保存的2 组二进制数据做无符号乘法运算，并将运算结果输出到LED 灯对应位。
  
  程序控制方式提示：循环读取按键键值，根据按键的值读取开关状态，并做相应处理。

## 实验原理

### 硬件电路框图

![](D:\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\计组实验\实验报告三\硬件电路框图1.png)

![](D:\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\计组实验\实验报告三\硬件电路框图2.png)

根据硬件电框图搭建的硬件平台整体框图如下：

![](D:\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\计组实验\实验报告三\硬件平台.png)

### 软件流程图

![](D:\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\计组实验\实验报告三\软件流程图.png)

## 实验源码

### 程序控制方式

```c
/*
Author: Carl Wang
Date: 2024/4/30
*/

#include <stdio.h>
#include <xil_io.h>
#include "platform.h"
#include "xil_printf.h"
#include "xgpio.h"
#include "sleep.h"
#include "xparameters.h"

int main()
{
    u8 seg_code[17] = {0x40, 0x79, 0x24, 0x30, 0x19, 0x12, 0x02, 0x78, 0x80, 0x10, 0x08, 0x03, 0x46, 0x21, 0x06, 0x0E, 0xFF};
    int read_flag, read_flag1 = 0;
    u8 num[8];
    XGpio xgpio;
    XGpio xgpio1;
    XGpio xgpio2;
    u32 sw_btn, prev_button_state = 0, prev_button_state1 = 0, button_state, button_state1, num1, num2;

    XGpio_Initialize(&xgpio, XPAR_AXI_GPIO_0_BASEADDR);
    XGpio_Initialize(&xgpio1, XPAR_AXI_GPIO_1_BASEADDR);
    XGpio_Initialize(&xgpio2, XPAR_AXI_GPIO_2_BASEADDR);
    XGpio_SetDataDirection(&xgpio, 1, 0xffff);
    XGpio_SetDataDirection(&xgpio, 2, 0x0);
    XGpio_SetDataDirection(&xgpio1, 1, 0x0);
    XGpio_SetDataDirection(&xgpio1, 2, 0xffffff00);
    XGpio_SetDataDirection(&xgpio2, 1, 0x1f);


    while (1) {
        button_state = XGpio_DiscreteRead(&xgpio2, 1) & 0x01; // 读取最低位

        if (button_state && !prev_button_state) { // 边缘检测
            read_flag = !read_flag; // 切换状态
            if (read_flag == 0) {
                XGpio_DiscreteWrite(&xgpio, 2, 0x0000); // 清除LED显示
                XGpio_DiscreteWrite(&xgpio1, 2, 0xFF); // 清除数码管显示
                break;
            }
        }

        if (read_flag) {
            sw_btn = XGpio_DiscreteRead(&xgpio, 1);
            num1 = sw_btn;
            XGpio_DiscreteWrite(&xgpio, 2, sw_btn); // 显示到LED

            num[7] = 16;
            num[6] = 16;
            num[5] = 16;
            num[4] = 16;

            num[3] = (sw_btn & 0xf000) >> 12;
            num[2] = (sw_btn & 0xf00) >> 8;
            num[1] = (sw_btn & 0xf0) >> 4;
            num[0] = (sw_btn & 0xf);

            for (int i = 1; i < 9; i++)
            {
                XGpio_DiscreteWrite(&xgpio1, 1, ~(0x1 << (i-1)));
                XGpio_DiscreteWrite(&xgpio1, 2, seg_code[num[i - 1]]);
                usleep(500);
            }
        }

        prev_button_state = button_state; // 更新前一状态
        usleep(5000); // 适当延时减少读取频率，减少抖动
    }

        
    while (1) {
        button_state1 = (XGpio_DiscreteRead(&xgpio2, 1) & 0x8) >> 3; 

        if (button_state1 && !prev_button_state1) { // 边缘检测
            read_flag1 = !read_flag1; // 切换状态
            if (read_flag1 == 0) {
                XGpio_DiscreteWrite(&xgpio, 2, 0x0000); // 清除LED显示
                XGpio_DiscreteWrite(&xgpio1, 2, 0xFF); // 清除数码管显示
                break;
            }
        }

        if (read_flag1) {
            sw_btn = XGpio_DiscreteRead(&xgpio, 1);
            num2 = sw_btn;
            XGpio_DiscreteWrite(&xgpio, 2, sw_btn); // 显示到LED

            num[7] = 16;
            num[6] = 16;
            num[5] = 16;
            num[4] = 16;

            num[3] = (sw_btn & 0xf000) >> 12;
            num[2] = (sw_btn & 0xf00) >> 8;
            num[1] = (sw_btn & 0xf0) >> 4;
            num[0] = (sw_btn & 0xf);

            for (int i = 1; i < 9; i++)
            {
                XGpio_DiscreteWrite(&xgpio1, 1, ~(0x1 << (i-1)));
                XGpio_DiscreteWrite(&xgpio1, 2, seg_code[num[i - 1]]);
                usleep(500);
            }
        }

        prev_button_state1 = button_state1; // 更新前一状态
        usleep(5000); // 适当延时减少读取频率，减少抖动
    }

    while (1) {
        int btnu = (XGpio_DiscreteRead(&xgpio2, 1) & 0x2) >> 1;
        int btnd = (XGpio_DiscreteRead(&xgpio2, 1) & 0x10) >> 4;

        if (btnu)
        {
            u32 sum = num1  + num2;
            XGpio_DiscreteWrite(&xgpio, 2, sum); // 显示到LED
            usleep(50000);
        }
        else if (btnd) {
            u32 mul = (num1 & 0xffff) * (num2 & 0xffff);
            XGpio_DiscreteWrite(&xgpio, 2, mul); // 显示到LED       
            usleep(50000);  
        }
    }
    return 0;
}
```

### 普通中断控制方式

```c
/*
Author: Carl Wang
Date: 2024/4/30
*/

#include <mb_interface.h>
#include <stdio.h>
#include <xil_io.h>
#include <xil_types.h>
#include "platform.h"
#include "xil_printf.h"
#include "xgpio.h"
#include "xparameters.h"

void buttonHandler(void)__attribute__((interrupt_handler));
void swHandler();
XGpio xgpio, xgpio2;
u32 data1 = 0, data2 = 0;
u8 data_ready = 0;
int main()
{
    XGpio_Initialize(&xgpio, XPAR_AXI_GPIO_0_BASEADDR);
    XGpio_Initialize(&xgpio2, XPAR_AXI_GPIO_2_BASEADDR);
    XGpio_SetDataDirection(&xgpio, 1, 0xFFFF); 
    XGpio_SetDataDirection(&xgpio, 2, 0x0);    
    XGpio_SetDataDirection(&xgpio2, 1, 0x1f);

    Xil_Out32(XPAR_AXI_GPIO_2_BASEADDR + 0x120, 0x1); //写 AXI_GPIO_O IPISR 清除中断
    Xil_Out32(XPAR_AXI_GPIO_2_BASEADDR + 0x128, 0x1); //写 AXI_GPIO_O IPIER（D0=1使能通道一中断）
    Xil_Out32(XPAR_AXI_GPIO_2_BASEADDR + 0x11c, 0x80000000); //写 AXI_GPIO_O GIER（仅D31有效，D31=1使能中断信号输出）

    // 初始化INTC
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0x8, 0x0);      // 禁用中断 IER（中断使能寄存器）
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0x1c, 0x3);      // 主使能中断控制器MER，使能硬件中断irq输出
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0xc, 0xFFFFFFFF); // 清除中断状态IAR

    // 使能 GPIO 中断
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0x8, 0x20); // 使能 intr[2]和[5] 中断, BUTTONS

    // 使能中断控制器
    microblaze_enable_interrupts();
    return 0;
}

void buttonHandler(void)
{
    u32 buttons;
    buttons = XGpio_DiscreteRead(&xgpio2, 1); // 读取按键状态

    if (buttons & 0x1) // 按下BTNC
    {
        data_ready |= 0x1; // 允许录入第一组数据
        swHandler();
    }
    else if ((buttons & 0x8) >> 3) // 按下BTNR
    {
        data_ready |= 0x2; // 允许录入第二组数据
        swHandler();
    }
    else if ((buttons & 0x2) >> 1) // 按下BTNU
    {
        if (data_ready == 0xF) // 检查两组数据是否都准备好
        {
            u32 sum = data1 + data2; // 无符号加法
            XGpio_DiscreteWrite(&xgpio, 2, sum); // 显示到LED
        }
    }
    else if ((buttons & 0x10) >> 4) // 按下BTND
    {
        if (data_ready == 0xF) // 检查两组数据是否都准备好
        {
            u32 mul = data1 * data2; // 无符号乘法
            XGpio_DiscreteWrite(&xgpio, 2, mul); // 显示到LED
        }
    }

    // 清除中断
    Xil_Out32(XPAR_AXI_GPIO_2_BASEADDR + 0x120, 0x1);
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0xc, 0x20);
}

void swHandler(void){
    int sw;
    sw = XGpio_DiscreteRead(&xgpio, 1);
    if (data_ready == 0x1)
    {
        data1 = sw;
        data_ready |= 0x4;
        XGpio_DiscreteWrite(&xgpio, 2, sw); // 显示到LED
    }
    else if(data_ready == 0x7)
    {
        data2 = sw;
        data_ready |= 0x8;
        XGpio_DiscreteWrite(&xgpio, 2, sw); // 显示到LED
    }
}
```

### 快速中断控制方式

```c
/*
Author: Carl Wang
Date: 2024/4/30
*/

#include <mb_interface.h>
#include <stdio.h>
#include <sys/_types.h>
#include <xil_io.h>
#include <xil_types.h>
#include "platform.h"
#include "xil_printf.h"
#include "xgpio.h"
#include "xparameters.h"

void buttonHandler(void)__attribute__((fast_interrupt));
void setup_gpio_interrupt(void);
void swHandler();
XGpio xgpio, xgpio2;
u32 data1 = 0, data2 = 0;
u8 data_ready = 0;
int main()
{
    XGpio_Initialize(&xgpio, XPAR_AXI_GPIO_0_BASEADDR);
    XGpio_Initialize(&xgpio2, XPAR_AXI_GPIO_2_BASEADDR);
    XGpio_SetDataDirection(&xgpio, 1, 0xFFFF); 
    XGpio_SetDataDirection(&xgpio, 2, 0x0);    
    XGpio_SetDataDirection(&xgpio2, 1, 0x1f);

    setup_gpio_interrupt();
    return 0;
}

void setup_gpio_interrupt(void)
{
    Xil_Out32(XPAR_AXI_GPIO_2_BASEADDR + 0x120, 0x1); //写 AXI_GPIO_O IPISR 清除中断
    Xil_Out32(XPAR_AXI_GPIO_2_BASEADDR + 0x128, 0x1); //写 AXI_GPIO_O IPIER（D0=1使能通道一中断）
    Xil_Out32(XPAR_AXI_GPIO_2_BASEADDR + 0x11c, 0x80000000); //写 AXI_GPIO_O GIER（仅D31有效，D31=1使能中断信号输出）

    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0x8, 0x0);      // 禁用中断 IER（中断使能寄存器）
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0xc, 0xFFFFFFFF); // 清除中断状态IAR
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0x8, 0x20); // 使能 intr[5] 中断, BUTTONS
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0x1c, 0x3);      // 主使能中断控制器MER，使能硬件中断irq输出

    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0X20, 0x20); //快速中断模式
    Xil_Out32(XPAR_XINTC_0_BASEADDR + 0x100 + 4*5, (unsigned int) buttonHandler); //快速中断模式
    microblaze_enable_interrupts();

}

void buttonHandler(void)
{
    u32 buttons;
    buttons = XGpio_DiscreteRead(&xgpio2, 1); // 读取按键状态

    if (buttons & 0x1) // 按下BTNC
    {
        data_ready |= 0x1; // 允许录入第一组数据
        swHandler();
    }
    else if ((buttons & 0x8) >> 3) // 按下BTNR
    {
        data_ready |= 0x2; // 允许录入第二组数据
        swHandler();
    }
    else if ((buttons & 0x2) >> 1) // 按下BTNU
    {
        if (data_ready == 0xF) // 检查两组数据是否都准备好
        {
            u32 sum = data1 + data2; // 无符号加法
            XGpio_DiscreteWrite(&xgpio, 2, sum); // 显示到LED
        }
    }
    else if ((buttons & 0x10) >> 4) // 按下BTND
    {
        if (data_ready == 0xF) // 检查两组数据是否都准备好
        {
            u32 mul = data1 * data2; // 无符号乘法
            XGpio_DiscreteWrite(&xgpio, 2, mul); // 显示到LED
        }
    }

    // 清除中断
    // Xil_Out32(XPAR_XINTC_0_BASEADDR + 0xc, 0x1);
    Xil_Out32(XPAR_AXI_GPIO_2_BASEADDR + 0x120, 0x1);
}

void swHandler(void){
    int sw;
    sw = XGpio_DiscreteRead(&xgpio, 1);
    if (data_ready == 0x1)
    {
        data1 = sw;
        data_ready |= 0x4;
        XGpio_DiscreteWrite(&xgpio, 2, sw); // 显示到LED
    }
    else if(data_ready == 0x7)
    {
        data2 = sw;
        data_ready |= 0x8;
        XGpio_DiscreteWrite(&xgpio, 2, sw); // 显示到LED
    }
}
```



## 实验结果

实验效果如下：

![](D:\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\计组实验\实验报告三\实验效果.png)
