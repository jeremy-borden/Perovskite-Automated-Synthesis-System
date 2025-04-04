#include <Adafruit_MAX31856.h>
#include <Adafruit_MCP4725.h>

#define MAX_CS 10 // Chip Select for MAX31856
Adafruit_MAX31856 thermocouple = Adafruit_MAX31856(MAX_CS);
Adafruit_MCP4725 dac;
#define temperature_step 50 // maxmimum amount temp can be increased at once

float target_temperature = 0.0;

void setup() {
  Serial.begin(115200);
  

  if (!thermocouple.begin()) {
    Serial.println("MAX31856 not found. Check wiring!");
    while (1);
  }

  thermocouple.setThermocoupleType(MAX31856_TCTYPE_K);

  dac.begin(0x60); // Initialize DAC with I2C address 0x60
  dac.setVoltage(0, true);
  Serial.println("Arduino Ready");
}

void loop() {
  if (!Serial.available()){
    return;
  }
  // Read input
  String command = Serial.readStringUntil('\n');
  command.trim();

  if (command == "GET_TEMP") {
    float temperature = get_temperature();
    
    if (isnan(temperature)) {
      Serial.println("ERROR: NaN"); // Send error response
      return;
    } 

    Serial.print("TEMP: ");
    Serial.println(temperature);
    
  } else if (command.startsWith("SET_TEMP ")) {
    int last_target = target_temperature;
    target_temperature = command.substring(9).toFloat(); // Convert text after the space in "SET_TEMP " to a float
    // Clamp values between hotplate min and max
    if (target_temperature < 0){
      target_temperature = 0;
    }
    else if (target_temperature > 540){
      target_temperature = 540;
    }
    //0 to 500

    while (abs(target_temperature - last_target) > temperature_step)
    {
      if (target_temperature > last_target)
      {
        last_target += temperature_step;
      }
      else
      {
        last_target -= temperature_step;
      }
      set_temperature(last_target);
      Serial.print("TARGET SET: ");
      Serial.println(last_target);
      delay(200);
    }
    
    set_temperature(target_temperature);
    Serial.print("TARGET SET: ");
    Serial.println(target_temperature);


  }
  else {
    Serial.println("ERROR: Invalid Command");
  }

  delay(10);
}

float get_temperature(){
  float tc_value = thermocouple.readThermocoupleTemperature();
  return 0.8*tc_value;
}

void set_temperature(float temperature_c){
    int dac_value = map(int(temperature_c), 0, 540, 0, 4095); // Convert temp to DAC output
    dac.setVoltage(dac_value, false);
}


