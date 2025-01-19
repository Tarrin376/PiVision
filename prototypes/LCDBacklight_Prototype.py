import time
import sys

if sys.platform == 'uwp':
    # Import SMBus library for Universal Windows Platform (UWP)
    import winrt_smbus as smbus
    # Initialize SMBus instance
    bus = smbus.SMBus(1)
else:
    # Import SMBus library for Linux
    import smbus
    # Import RPi.GPIO library for Raspberry Pi GPIO control
    import RPi.GPIO as GPIO
    # Get Raspberry Pi revision number
    rev = GPIO.RPI_REVISION
    # Check if the Raspberry Pi is a model 2 or 3
    if rev == 2 or rev == 3:
        # Initialize SMBus instance for Raspberry Pi model 2 or 3
        bus = smbus.SMBus(1)
    else:
        # Initialize SMBus instance for Raspberry Pi model 1
        bus = smbus.SMBus(0)

DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e
text = ""

def set_rgb(r, g, b):
    # Set RGB values for the display
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 1, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x08, 0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 4, r)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 3, g)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 2, b)

def text_command(cmd):
    # Send command to the text display
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, cmd)
    
def set_text(new_text):
    # If text is the same text on the LCD Backlight, ignore
    if text == new_text:
        return
    
    # Clear the display and prepare for new text
    text_command(0x01) # Clear display
    time.sleep(0.05)
    text_command(0x08 | 0x04) # Turn on display
    text_command(0x28) # 2 lines, 5x8 matrix
    time.sleep(0.05)

    count = 0
    row = 0
    
    # Iterate through each character in the text
    for c in new_text:
        # Handle newline characters or reaching the end of each row
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            text_command(0xc0) # Move to next row
            if c == '\n':
                continue
        count += 1
        # Write the character to the display
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))
    
    # Update the stored text
    text = new_text

if __name__ == "__main__":
    set_rgb(0, 128, 64)
    set_text("testing")
    time.sleep(5)
    set_text("")