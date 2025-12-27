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
}

void LEDManager::clear(const Clear& clear)
{
    Serial.println("Clearing LEDs");
    FastLED.clear();
    FastLED.show();
}

void LEDManager::setLEDs(const SetLEDs& setLEDs)
{
    Serial.println("Setting LEDs");
    FastLED.clear();
    for (int i = 0; i < setLEDs.pixels_count; i++)
    {
        const Color& pixel = setLEDs.pixels[i];
        d_leds[i] = CRGB(pixel.red, pixel.green, pixel.blue);
    }
    FastLED.show();
}
