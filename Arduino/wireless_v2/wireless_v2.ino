//#include <Adafruit_INA219.h>

int comInt;  
#include <Servo.h>
#include <Wire.h>

#include <Adafruit_INA219.h>

#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

Adafruit_INA219 ina219;

float shuntvoltage = 0;
float busvoltage = 0;
float current_mA = 0;
float loadvoltage = 0;
long time,lasttime;
int ref_angle=0;
int ref_roll=0;
int roll=0;
int heading_angle=0;
int Ms=100;
Servo rudder;  // create servo object to control a servo
Servo sail;
int pos_rudder=90;
int pos_sail=160;

void move_rudder(){
  if(30<=pos_rudder && pos_rudder<=123){
    rudder.write(pos_rudder);
    
  }
}
void move_sail(){
  if(90<=pos_sail && pos_sail<=210){
    sail.write(pos_sail);
    
  }
}


 

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

Adafruit_BNO055 bno = Adafruit_BNO055(55);

/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

/**************************************************************************/
/*
    Display some basic info about the sensor status
*/
/**************************************************************************/
void displaySensorStatus(void)
{
  /* Get the system status values (mostly for debugging purposes) */
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  /* Display the results in the Serial Monitor */
  Serial.println("");
  Serial.print("System Status: 0x");
  Serial.println(system_status, HEX);
  Serial.print("Self Test:     0x");
  Serial.println(self_test_results, HEX);
  Serial.print("System Error:  0x");
  Serial.println(system_error, HEX);
  Serial.println("");
  delay(500);
}
void set_zero_angle(){
  sensors_event_t event;
  bno.getEvent(&event);
  ref_angle = event.orientation.x, 4;
  ref_roll=event.orientation.z, 4;
  Serial.print("x");
}

/**************************************************************************/
/*
    Display sensor calibration status
*/
/**************************************************************************/
void displayCalStatus(void)
{
  /* Get the four calibration values (0..3) */
  /* Any sensor data reporting 0 should be ignored, */
  /* 3 means 'fully calibrated" */
  uint8_t system, gyro, accel, mag;
  system = gyro = accel = mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  /* The data should be ignored until the system calibration is > 0 */
  Serial.print("\t");
  if (!system)
  {
    Serial.print("! ");
  }

  /* Display the individual values */
  Serial.print("Sys:");
  Serial.print(system, DEC);
  Serial.print(" G:");
  Serial.print(gyro, DEC);
  Serial.print(" A:");
  Serial.print(accel, DEC);
  Serial.print(" M:");
  Serial.print(mag, DEC);
}

void setup() {  
  
  rudder.attach(4);
  sail.attach(5);
  Serial.begin(57600);
  
  uint32_t currentFrequency;
  ina219.begin(); 
  while(1){
    if(bno.begin())
    {
      /* There was a problem detecting the BNO055 ... check your connections */
      break;
//      while(1);
//      delay(100);
    }
    else{
      Serial.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
      bno.begin();
    }
  }

  delay(100);
  displaySensorDetails();

  /* Optional: Display current status */
  displaySensorStatus();

  bno.setExtCrystalUse(true);
  while(Serial.read()>= 0){}//clear serialbuffer  
}  
void sendmess(){
  sensors_event_t event;
  bno.getEvent(&event);
  heading_angle = event.orientation.x, 4;
  heading_angle-=(int)(ref_angle);
  roll= event.orientation.z, 4;
  roll-= (int)(ref_roll);
  if (ref_angle!=0){
    heading_angle=-heading_angle;}
 
  if (heading_angle<0){
    heading_angle+=360;
  }
  /* Display the floating point data */
//  Serial.println("X: ");

//  Serial.print("\tY: ");
//  Serial.print(event.orientation.y, 4);
//  Serial.println("\tZ: ");
//  Serial.print(event.orientation.z, 4);

  /* Optional: Display calibration status */
//  displayCalStatus();

//
//  /* Optional: Display sensor status (debug only) */
//  //displaySensorStatus();
//
//  /* Optional: Display calibration status */
//  displayCalStatus();
  shuntvoltage = ina219.getShuntVoltage_mV();
  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  loadvoltage = busvoltage + (shuntvoltage / 1000);

  Serial.print(heading_angle);  Serial.print(",");
  Serial.print(roll);
  Serial.print(","); Serial.print(busvoltage); 
//  Serial.print(","); Serial.print(shuntvoltage);
//  Serial.print(","); Serial.print(loadvoltage);
  Serial.print(","); Serial.println(current_mA); 
  }
void loop() { 
//  sendmess();
  
  
  time=millis();//去现在时间(ms)
  if(time-lasttime>=Ms){
    lasttime=time;
    sendmess();
    Serial.flush();
  }
 
  char command=Serial.read();
  if(command==byte(',')){   
      comInt = Serial.parseInt();     
      pos_rudder=comInt/100;
      pos_sail=comInt%100*1.5+50;
      move_rudder();
      move_sail();
    }  
  else if(command==byte('r')){
    set_zero_angle();
  }
  
    // clear serial buffer  

}  

