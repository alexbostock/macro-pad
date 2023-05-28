import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import time

# mic: cmd shift m
# camera: cmd shift o
# hang up: cmd shift h

keyboard_mapping = {
    (0, 0): Keycode.U,
    (1, 0): Keycode.I,
    (2, 0): Keycode.O,
    (0, 1): Keycode.J,
    (1, 1): Keycode.K,
    (2, 1): Keycode.L,
    (0, 2): Keycode.M,
    (1, 2): Keycode.COMMA,
    (2, 2): Keycode.PERIOD,
}

cc_mapping = {
    #(0, 0): ConsumerControlCode.BRIGHTNESS_DECREMENT,
    #(1, 0): ConsumerControlCode.BRIGHTNESS_INCREMENT,
    #(0, 1): ConsumerControlCode.VOLUME_DECREMENT,
    #(1, 1): ConsumerControlCode.MUTE,
    #(2, 1): ConsumerControlCode.VOLUME_INCREMENT,
}

columns = list(map(lambda pin: digitalio.DigitalInOut(pin), [board.GP27, board.GP21, board.GP19]))
for column in columns:
    column.switch_to_output()

rows = list(map(lambda pin: digitalio.DigitalInOut(pin), [board.GP28, board.GP17, board.GP16]))
for row in rows:
    row.switch_to_input(digitalio.Pull.DOWN)

pressed_keys = set()

keyboard = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

while True:
    for column_index, column in enumerate(columns):
        column.value = True

        for row_index, row in enumerate(rows):
            coords = (column_index, row_index)
            
            if row.value:
                if coords not in pressed_keys:
                    pressed_keys.add(coords)
                    if coords in keyboard_mapping:
                        keyboard.press(keyboard_mapping[coords])
                    if coords in cc_mapping:
                        cc.press(cc_mapping[coords])
            else:
                if coords in pressed_keys:
                    pressed_keys.remove(coords)
                    if coords in keyboard_mapping:
                        keyboard.release(keyboard_mapping[coords])
                    if coords in cc_mapping:
                        cc.release()

        column.value = False
        time.sleep(0.01)
