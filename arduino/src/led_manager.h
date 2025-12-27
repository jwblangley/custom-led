#ifndef LED_MANAGER
#define LED_MANAGER

#include <led.pb.h>

class LEDManager
{
    public:
    LEDManager(int numLEDs);
    ~LEDManager();

    void clear(const Clear& clear);
    void setLEDs(const SetLEDs& setLEDs);

    private:
    const int d_numLEDs;
};

#endif
