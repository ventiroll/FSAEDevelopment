/*
 * SDSU Aztec Electric Racing (AER)
 * Micro-ROS Demo Firmware for STM32 NUCLEO-G474RE
 *
 * Receives /control/command from Jetson demo node
 * Converts target_velocity_mps to 0-5V DAC analog signal for Cascadia Motion CM200 Inverter
 */

#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <aer_interfaces/msg/control_cmd.h>

#include "main.h"
#include "dac.h"

#define MAX_SPEED_MPS      5.0f   // Max speed corresponding to 4.5V / 90% throttle
#define DAC_MAX_DIGITAL    4095   // 12-bit DAC (0 to 4095 = 0.0V to 3.3V, op-amp scaled to 0-5V)

rcl_subscription_t subscriber;
aer_interfaces__msg__ControlCmd msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

void set_inverter_dac(float velocity_mps) {
    if (velocity_mps < 0.0f) velocity_mps = 0.0f;
    if (velocity_mps > MAX_SPEED_MPS) velocity_mps = MAX_SPEED_MPS;

    // Linear mapping: 0.0 m/s -> 0.0V (0 counts), 5.0 m/s -> 4.5V (3686 counts)
    float throttle_fraction = velocity_mps / MAX_SPEED_MPS;
    uint32_t dac_value = (uint32_t)(throttle_fraction * 3686.0f);

    // Update DAC1 Channel 1 Output
    HAL_DAC_SetValue(&hdac1, DAC_CHANNEL_1, DAC_ALIGN_12B_R, dac_value);
}

void control_callback(const void * msvin) {
    const aer_interfaces__msg__ControlCmd * cmd = (const aer_interfaces__msg__ControlCmd *)msvin;

    if (cmd->emergency_stop) {
        set_inverter_dac(0.0f);
        return;
    }

    set_inverter_dac(cmd->target_velocity_mps);
}

void setup_microros() {
    allocator = rcl_get_default_allocator();
    rclc_support_init(&support, 0, NULL, &allocator);
    rclc_node_init_default(&node, stm32_inverter_bridge, , &support);

    rclc_subscription_init_default(
        &subscriber,
        &node,
        ROSIDL_GET_MSG_TYPE_SUPPORT(aer_interfaces, msg, ControlCmd),
        /control/command
    );

    rclc_executor_init(&executor, &support.context, 1, &allocator);
    rclc_executor_add_subscription(&executor, &subscriber, &msg, &control_callback, ON_NEW_DATA);
}

int main(void) {
    HAL_Init();
    SystemClock_Config();
    MX_GPIO_Init();
    MX_DAC1_Init();

    setup_microros();

    while (1) {
        rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10));
    }
}
