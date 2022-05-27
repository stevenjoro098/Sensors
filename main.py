from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock

from plyer import accelerometer
from plyer import gyroscope, compass, battery, vibrator, notification

Window.size = (320, 600)


class Home(Screen):
    pass


class NotificationView(Screen):
    def get_notifier(self):
        notification_title = self.ids.notification_title.text
        notification_message = self.ids.notification_message.text
        notification.notify(title=notification_title, message=notification_message, ticker='New Message',
                            app_icon='asset/crab.ico', toast=True)


class VibratorView(Screen):
    repeat = 5

    def get_vibration(self):
        time = self.ids.vibrate_time.text
        repeat_pattern = self.ids.repeat_.active
        # print(time)
        if time != '':
            if repeat_pattern:
                vibrator.vibrate(time=time, repeat=self.repeat)
            else:
                vibrator.vibrate(time=time)
        else:
            self.ids.vibrate_time.hint_text = 'Please Enter time'


class BatteryView(Screen):
    def get_battery(self):
        print("Call Battery Method")
        batt = battery.status
        self.ids.percentage.text = str(batt['percentage']) + "%"
        if batt['isCharging']:
            self.ids.charging.text = "Charging"
            self.ids.charging.color = 0, 1, 0, 1
            self.ids.charging.icon = 'battery-charging'
        else:
            self.ids.charging.text = "Not Charging"
            self.ids.charging.color = 1, 1, 0, 1
            self.ids.charging.icon = 'battery-charging-outline'


class CompassView(Screen):
    def do_toggle(self):
        try:
            compass.enable()
            Clock.schedule_interval(self.get_compass, 1 / 20.)
        except:
            compass.disable()
            Clock.unschedule(self.get_compass)

    def get_compass(self):
        if compass.enable():
            comps = compass.field()
            self.ids.compass_x_axis.text = "X-Axis: " + comps[0]
            self.ids.compass_y_axis.text = "Y-Axis: " + comps[1]
            self.ids.compass_z_axis.text = "Z-Axis: " + comps[2]

        else:
            print('Error')

    def disable_compass(self):
        compass.disbale()
        Clock.unschedule(self.get_compass)


class Gyro(Screen):
    def do_toggle(self):
        self.sensorEnabled = False
        try:
            if not self.sensorEnabled:
                gyroscope.enable()
                Clock.schedule_interval(self.get_gyroscope, 1 / 20.)
                self.sensorEnabled = True
            else:
                gyroscope.disable()
                Clock.unschedule(self.get_gyroscope)
                self.sensorEnabled = False
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.gyroscope_title.text = status

    def get_gyroscope(self, dt):
        gyroscope.enable()
        if gyroscope.enable():
            gyro = gyroscope.rotation
            self.ids.xaxis.text = 'X-Axis: ' + gyro[0]
            self.ids.yaxis.text = 'Y-Axis: ' + gyro[1]
            self.ids.zaxis.text = 'Z-Axis: ' + gyro[2]
        else:
            self.ids.gyroscope_title.text = 'Gyroscope Disabled'

    def disable_gyro(self):
        gyroscope.disable()
        Clock.unschedule(self.get_gyroscope)


class SensorsApp(MDApp):

    def build(self):
        return Builder.load_file('main.kv')

    def do_toggle(self):
        self.sensorEnabled = False
        try:
            if not self.sensorEnabled:
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Accelerometer"
            else:
                accelerometer.disable()
                Clock.unschedule(self.get_acceleration)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start Accelerometer"
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.accel_status.text = status

    def get_acceleration(self, dt):
        val = accelerometer.acceleration[:3]

        if not val == (None, None, None):
            self.ids.x_label.text = "X: " + str(val[0])
            self.ids.y_label.text = "Y: " + str(val[1])
            self.ids.z_label.text = "Z: " + str(val[2])


if __name__ == '__main__':
    SensorsApp().run()
