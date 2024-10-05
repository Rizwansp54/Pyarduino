#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include "driver/gpio.h"
#include "esp_rom_gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "soc/gpio_num.h"
#include "soc/gpio_struct.h"

void app_main(void)
{
    // Set GPIO 22 as input with pull-up enabled
    gpio_set_direction(GPIO_NUM_22, GPIO_MODE_INPUT);
    gpio_set_pull_mode(GPIO_NUM_22, GPIO_PULLUP_ONLY);

    // Set GPIO 26 as output (for the LED)
    //esp_rom_gpio_pad_select_gpio(GPIO_NUM_5);
    gpio_set_direction(GPIO_NUM_5, GPIO_MODE_OUTPUT);
 
    while (1)
    {
        // Check if the button is pressed (low signal)
        if (gpio_get_level(GPIO_NUM_22))
            gpio_set_level(GPIO_NUM_5, 0);  // Turn off LED
        else
            gpio_set_level(GPIO_NUM_5, 1);  // Turn on LED

        // Delay for 10 ms
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        
    }   
}