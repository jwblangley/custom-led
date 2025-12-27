#ifndef LED_MANAGER
#define LED_MANAGER

#include <Arduino.h>
#include <led.pb.h>
#include <FastLED.h>

#define LED_PIN     16
#define NUM_LEDS    50
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB

class LEDManager
{
    public:
    LEDManager();
    ~LEDManager();

    void init();
    void clear(const Clear& clear);
    void setLEDs(const SetLEDs& setLEDs);

    private:
    CRGB d_leds[NUM_LEDS];
};

#endif
