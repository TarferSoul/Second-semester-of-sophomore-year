/* 
 * wasbhedr.c
 *
 *  Created on: 2024年5月21日
 *      Author: Lenovo
 */
#include "stdio.h"
#include <stdio.h>
#include "xil_io.h"
#include "xgpio_l.h"
#include "xtmrctr_l.h"
#include "xintc_l.h"
#include "xil_printf.h"
#include "xspi_l.h"

float timePeriod = 1.6 * 100000000 - 2;
int counter = 1;
uint16_t voltageLevel;

void toggleSwitchHandler();
void timeExpiredHandler();
void setupTimer();
void customInterruptServiceRoutine() __attribute__((interrupt_handler));

int main()
{
    // SPI configuration address
    Xil_Out32(XPAR_AXI_QUAD_SPI_1_BASEADDR + XSP_CR_OFFSET, XSP_CR_ENABLE_MASK | XSP_CR_MASTER_MODE_MASK | XSP_CR_CLK_POLARITY_MASK);
    Xil_Out32(XPAR_AXI_QUAD_SPI_1_BASEADDR + XSP_SSR_OFFSET, 0xfffffffe);
    Xil_Out32(XPAR_SPI_1_BASEADDR + XSP_SSR_OFFSET, 0x0); // ?
    Xil_Out32(XPAR_SPI_1_BASEADDR + XSP_DTR_OFFSET, 0x0);

    setupTimer();

    // switch configuration
    Xil_Out32(XPAR_AXI_GPIO_0_BASEADDR + XGPIO_TRI_OFFSET, 0xffff);
    Xil_Out32(XPAR_AXI_GPIO_0_BASEADDR + XGPIO_IER_OFFSET, XGPIO_IR_CH1_MASK);
    Xil_Out32(XPAR_AXI_GPIO_0_BASEADDR + XGPIO_GIE_OFFSET, XGPIO_GIE_GINTR_ENABLE_MASK);

    // interrupt controller configuration
    Xil_Out32(XPAR_AXI_INTC_0_BASEADDR + XIN_IMR_OFFSET, 0x20);
    Xil_Out32(XPAR_AXI_INTC_0_BASEADDR + XIN_IER_OFFSET, XPAR_AXI_GPIO_0_IP2INTC_IRPT_MASK | XPAR_AXI_TIMER_0_INTERRUPT_MASK);
    Xil_Out32(XPAR_AXI_INTC_0_BASEADDR + XIN_MER_OFFSET, XIN_INT_MASTER_ENABLE_MASK | XIN_INT_HARDWARE_ENABLE_MASK);

    microblaze_enable_interrupts();

    return 0;
}

void toggleSwitchHandler()
{
    unsigned int switchState = 0;
    switchState = Xil_In16(XPAR_AXI_GPIO_0_BASEADDR + XGPIO_DATA_OFFSET);
    //set timePeriod:
    timePeriod = switchState;
    if (timePeriod == 0)
    {
        timePeriod = 1;
    }
    else
    {
        timePeriod = timePeriod / 10; // s
        timePeriod = timePeriod * 100000000 - 2;
        setupTimer();
    }

    // Clear interrupt
    Xil_Out32(XPAR_AXI_GPIO_0_BASEADDR + XGPIO_ISR_OFFSET, Xil_In32(XPAR_AXI_GPIO_0_BASEADDR + XGPIO_ISR_OFFSET));
}

void timeExpiredHandler()
{
    // Read and output voltage
    voltageLevel = Xil_In16(XPAR_AXI_QUAD_SPI_1_BASEADDR + XSP_DRR_OFFSET) % 0x8000;
    int calculatedVoltage;
    calculatedVoltage = voltageLevel * 3300 / 0xfff / 2;
    counter = -counter;

    xil_printf("The current voltage is %d mV    \n", calculatedVoltage, counter);
    //
    Xil_Out32(XPAR_SPI_1_BASEADDR + XSP_DTR_OFFSET, 0x0);
    Xil_Out32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TCSR_OFFSET, Xil_In32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TCSR_OFFSET)); // Clear timer interrupt
}

void setupTimer()
{
    // Timer initialization
    Xil_Out32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TCSR_OFFSET, Xil_In32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TCSR_OFFSET) & ~XTC_CSR_ENABLE_TMR_MASK); // Write TCSR
    Xil_Out32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TLR_OFFSET, timePeriod);
    Xil_Out32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TCSR_OFFSET, Xil_In32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TCSR_OFFSET) | XTC_CSR_LOAD_MASK); // Load count
    Xil_Out32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TCSR_OFFSET, (Xil_In32(XPAR_AXI_TIMER_0_BASEADDR + XTC_TCSR_OFFSET) & ~XTC_CSR_LOAD_MASK) |
             XTC_CSR_ENABLE_TMR_MASK | XTC_CSR_AUTO_RELOAD_MASK | XTC_CSR_ENABLE_INT_MASK | XTC_CSR_DOWN_COUNT_MASK);
    // Start timing with auto-reload, interrupt enabled, and counting down
}

void customInterruptServiceRoutine()
{
    int interruptStatus;
    interruptStatus = Xil_In32(XPAR_AXI_INTC_0_BASEADDR + XIN_ISR_OFFSET);

    if ((interruptStatus & XPAR_AXI_TIMER_0_INTERRUPT_MASK) == XPAR_AXI_TIMER_0_INTERRUPT_MASK)
    {
        timeExpiredHandler();
    }

    if ((interruptStatus & XPAR_AXI_GPIO_0_IP2INTC_IRPT_MASK) == XPAR_AXI_GPIO_0_IP2INTC_IRPT_MASK)
    {
        toggleSwitchHandler();
    }
    Xil_Out32(XPAR_AXI_INTC_0_BASEADDR + XIN_IAR_OFFSET, interruptStatus);
}