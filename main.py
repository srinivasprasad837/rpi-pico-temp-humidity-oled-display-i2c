from machine import Pin, I2C
from time import sleep
import dht
import ssd1306

class DHTSensor:
    def __init__(self, pin, i2c_scl, i2c_sda):
        self.sensor = dht.DHT11(Pin(pin))
        self.led = machine.Pin('LED', machine.Pin.OUT)
        self.i2c = machine.SoftI2C(scl=machine.Pin(i2c_scl), sda=machine.Pin(i2c_sda))
        
        devices = self.i2c.scan()
        if devices:
            print("I2C devices found:", [hex(device) for device in devices])
            if 0x3C in devices:
                print('its')
                self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
                print('running')
            else:
                raise Exception("SSD1306 display not found at address 0x3C")
        else:
            raise Exception("No I2C devices found")
    
    def read_sensor(self):
        try:
            
            sleep(1)  # Delay between readings
            self.sensor.measure()  # Measure temperature and humidity
            temp = self.sensor.temperature()  # Get temperature in Celsius
            hum = self.sensor.humidity()  # Get humidity in percentage
            
            # Print the temperature and humidity
            print('Temperature:', temp, 'C')
            print('Humidity:', hum, '%')
            
            # Display data on OLED
            self.display_oled(temp, hum)
            
            return temp, hum
        
        except OSError as e:
            # Print detailed error message
            print('Failed to read sensor:', e)
            return None, None

    def toggle_led(self, state):
        self.led.value(state)

    def display_oled(self, temp, hum):
        try:
            self.oled.fill(0)  # Clear the display
            
            # Define box dimensions and text positions
            box_width = 120
            box_height = 40
            box_x = (self.oled.width - box_width) // 2
            box_y = (self.oled.height - box_height) // 2

            # Draw the box
            self.oled.rect(box_x, box_y, box_width, box_height, 1)

            # Display temperature and humidity inside the box
            temp_text = f"Temp: {temp}C"
            hum_text = f"Humidity: {hum}%"
            line_height = 20  # Adjust for spacing between lines
            self.oled.text(temp_text, box_x + 5, box_y + 5)
            self.oled.text(hum_text, box_x + 5, box_y + 5 + line_height)

            self.oled.show()  # Update the display

        except Exception as e:
            print('Failed to update OLED display:', e)

# Initialize the sensor and display
sensor = DHTSensor(pin=22, i2c_scl=13, i2c_sda=12)



# Continuously read the sensor and display it
while True:
    # Initialize the onboard LED
   sensor.toggle_led(1)
   sensor.read_sensor()
   sensor.toggle_led(0)
   sleep(1)
