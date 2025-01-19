try:
    import time
    import os
    import threading
    import keyboard
    from serial.serialposix import Serial
    from LCDBacklight import LCDBacklight
    from Camera import Camera
    from dotenv import load_dotenv
    from flask import Flask, render_template
except ImportError as err:
    print("Failed to import modules. Error: %s" % err)

app = Flask(__name__)


class Main:
    def __init__(self):
        self.lcd_backlight = LCDBacklight()
        self.camera = Camera(self.lcd_backlight)
        
        # Open a serial port connection to receive data from the arduino
        self.serial = Serial(os.environ.get("SERIAL_PORT"), 9600, timeout=0.2)
        self.exit_flag = False
    
    def preview_loop(self):
        while True:
            # If the user pressed 'q', stop the camera preview
            if keyboard.is_pressed("q"):
                self.camera.camera.stop_preview()
                self.exit_flag = True
            
            time.sleep(0.1)
    
    def process_image(self):
        try:
            image = self.camera.parse_image()
            text = self.camera.read_image_text(image)
            self.camera.write_image_text(text)
        except Exception as err:
            self.lcd_backlight.set_text(str(err))
            time.sleep(5)
            self.lcd_backlight.set_text("")
    
    def run(self):
        # Thread to check if the user has pressed 'q' to quit camera preview
        preview_thread = threading.Thread(target=self.preview_loop)
        preview_thread.setDaemon(True)
        preview_thread.start()
        
        while True:
            # Reset the LCD backlight text and start camera preview
            self.lcd_backlight.set_text("")
            self.camera.camera.start_preview()
            
            # Reset exit flag and zoom
            self.exit_flag = False
            self.camera.reset_zoom()
            
            while True:
                # If the user pressed 'q', exit
                if self.exit_flag:
                    break
                
                # The data array from the arduino
                data = self.serial.readline().strip().decode().split(" ")
                
                # If not all sensor and actuator data is present, continue
                if len(data) < 3:
                    continue
                
                # The light intensity in the environment (0-10)
                light = int(data[1])
                # State of the joystick (1 for zoom-in, -1 for zoom-out, and 0)
                joystick_val = int(data[2])
                # Update the camera zoom
                self.camera.update_zoom(joystick_val)
      
                # If light intensity is too low, give a warning message to the user
                if light < 5:
                    self.lcd_backlight.set_text(f"Light must be {((5 - light) / 5) * 100}% brighter.")
                    self.lcd_backlight.set_rgb(241, 0, 7)
                    continue
                
                self.lcd_backlight.set_rgb(0, 128, 64)
                # If the camera has been manually zoomed in, show percentage
                if self.camera.zoom > 0:
                    self.lcd_backlight.set_text(f"Zoom: {int(self.camera.zoom * 100)}%")
                else:
                    self.lcd_backlight.set_text("")
                
                # If the LED button has been pressed, extract text from the image
                if data[0] == "0":
                    self.process_image()
                    break
            
            self.lcd_backlight.set_text("Press enter to continue")
            input("")
            self.lcd_backlight.set_text("")

@app.route("/")
def index():
    return render_template("index.html")
    
def run_main_app():
    # Run main app loop
    main_app = Main()
    main_app.run()

if __name__ == "__main__":
    load_dotenv()
    main_app_thread = threading.Thread(target=run_main_app)
    main_app_thread.setDaemon(True)
    main_app_thread.start()
    app.run()
    

    