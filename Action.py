class Action:
    def __init__(self, name, led_pin, frequency):
        self.name = name
        self.led_pin = led_pin
        self.frequency = frequency

    def get_name(self):
        return self.name

    def get_led_pin(self):
        return self.led_pin

    def get_frequency(self):
        return self.frequency
