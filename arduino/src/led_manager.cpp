#include "led_manager.h"

#include <Arduino.h>

LEDManager::LEDManager(const int numLEDs) : d_numLEDs(numLEDs)
{
}

LEDManager::~LEDManager()
{
}

void LEDManager::clear(const Clear& clear)
{
    Serial.println("Clearing LEDs");
}

void LEDManager::setLEDs(const SetLEDs& setLEDs)
{
    Serial.println("Setting LEDs");
}
