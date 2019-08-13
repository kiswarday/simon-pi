import RPi.GPIO as GPIO
import time
from Action import Action
from random import choice

colors = ['red', 'blue', 'yellow', 'green']
sequence = []

red_button = 25
red_led = 7
red_frequency = 1000

blue_button = 24
blue_led = 20
blue_frequency = 1500

yellow_button = 23
yellow_led = 16
yellow_frequency = 2000

green_button = 18
green_led = 8
green_frequency = 2500

start_button = 21
start_frequency = 2700
end_frequency = 800

buzzer_pin = 12

time_available = 3


def setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(red_button, GPIO.IN)
    GPIO.setup(blue_button, GPIO.IN)
    GPIO.setup(yellow_button, GPIO.IN)
    GPIO.setup(green_button, GPIO.IN)
    GPIO.setup(start_button, GPIO.IN)

    GPIO.setup(red_led, GPIO.OUT)
    GPIO.setup(blue_led, GPIO.OUT)
    GPIO.setup(yellow_led, GPIO.OUT)
    GPIO.setup(green_led, GPIO.OUT)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    global buzzer
    buzzer = GPIO.PWM(buzzer_pin, 1)


def run():
    sequence.clear()

    is_game_active = True
    while is_game_active:
        time.sleep(1)
        create_action()
        play_sequence()
        is_game_active = guess_sequence()
    end_game()


def end_game():
    for i in range(3):
        GPIO.output(red_led, GPIO.HIGH)
        GPIO.output(blue_led, GPIO.HIGH)
        GPIO.output(yellow_led, GPIO.HIGH)
        GPIO.output(green_led, GPIO.HIGH)
        play_buzzer(end_frequency, 0.2)

        GPIO.output(red_led, GPIO.LOW)
        GPIO.output(blue_led, GPIO.LOW)
        GPIO.output(yellow_led, GPIO.LOW)
        GPIO.output(green_led, GPIO.LOW)
        time.sleep(0.1)


def create_action():
    color = choice(colors)
    pin_led = globals()[color+'_led']
    frequency = globals()[color+'_frequency']
    a = Action(color, pin_led, frequency)
    sequence.append(a)


def play_sequence():
    for element in sequence:
        play_action(element.get_led_pin(), element.get_frequency())


def play_action(led_pin, frequency):
    GPIO.output(led_pin, GPIO.HIGH)
    play_buzzer(frequency, 0.5)
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.1)


def play_buzzer(frequency, duration):
    buzzer.ChangeFrequency(frequency)
    buzzer.start(50)
    time.sleep(duration)
    buzzer.stop()


def guess_sequence():
    tmp_sequence = sequence[:]
    time_limit = time.time() + time_available

    while time.time() < time_limit:
        if len(tmp_sequence) == 0:
            return True

        if GPIO.input(red_button) == GPIO.LOW:
            play_action(red_led, red_frequency)
            action = tmp_sequence.pop(0)
            if action.get_name() != 'red':
                return False
            time_limit = time.time() + time_available
        elif GPIO.input(blue_button) == GPIO.LOW:
            play_action(blue_led, blue_frequency)
            action = tmp_sequence.pop(0)
            if action.get_name() != 'blue':
                return False
            time_limit = time.time() + time_available
        elif GPIO.input(yellow_button) == GPIO.LOW:
            play_action(yellow_led, yellow_frequency)
            action = tmp_sequence.pop(0)
            if action.get_name() != 'yellow':
                return False
            time_limit = time.time() + time_available
        elif GPIO.input(green_button) == GPIO.LOW:
            play_action(green_led, green_frequency)
            action = tmp_sequence.pop(0)
            if action.get_name() != 'green':
                return False
            time_limit = time.time() + time_available

    return False


def destroy():
    GPIO.output(red_led, GPIO.LOW)
    GPIO.output(blue_led, GPIO.LOW)
    GPIO.output(yellow_led, GPIO.LOW)
    GPIO.output(green_led, GPIO.LOW)
    GPIO.output(buzzer_pin, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    print('Program is starting...')
    print('Idle...')
    try:
        while True:
            if GPIO.input(start_button) == GPIO.LOW:
                play_buzzer(start_frequency, 0.3)
                run()
                print('Game finished')
                print('Idle...')
    except KeyboardInterrupt:
        destroy()
        print('Resources released')
