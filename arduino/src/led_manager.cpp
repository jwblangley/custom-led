#include "led_manager.h"

LEDManager::LEDManager()
{
}

LEDManager::~LEDManager()
{
}

void LEDManager::init()
{
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(d_leds, NUM_LEDS)
           .setCorrection(TypicalLEDStrip);

    FastLED.setBrightness(50);

    d_leds[0] = CRGB::Red;
    FastLED.show();
}

void LEDManager::clear(const Clear& clear)
{
    Serial.println("Clearing LEDs");
}

void LEDManager::setLEDs(const SetLEDs& setLEDs)
{
    Serial.println("Setting LEDs");
}
