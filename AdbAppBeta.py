import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
import subprocess

kivy.require('2.0.0')

class ADBControlApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.language = 'en'
        self.selected_device = None
        self.translations = {
            'en': {
                'connect': 'Connect',
                'disconnect': 'Disconnect',
                'list_devices': 'List Devices',
                'send': 'Send',
                'swipe': 'Swipe',
                'touch': 'Touch',
                'enter_ip': 'Enter IP (e.g., 192.168.111.xxx)',
                'enter_command': 'Enter ADB shell command',
                'output': 'Output will be shown here.',
                'buttons': {
                    "Brightness Up": "Brightness Up",
                    "Brightness Down": "Brightness Down",
                    "Volume Up": "Volume Up",
                    "Volume Down": "Volume Down",
                    "Power": "Power",
                    "Home": "Home",
                    "Assistant": "Assistant",
                    "Back": "Back",
                    "Menu": "Menu",
                    "Search": "Search",
                    "Swipe Up": "Swipe Up",
                    "Swipe Down": "Swipe Down",
                    "Swipe Left": "Swipe Left",
                    "Swipe Right": "Swipe Right",
                    "Touch": "Touch"
                }
            },
            'pl': {
                'connect': 'Połącz',
                'disconnect': 'Rozłącz',
                'list_devices': 'Lista urządzeń',
                'send': 'Wyślij',
                'swipe': 'Przesuń',
                'touch': 'Dotknij',
                'enter_ip': 'Wprowadź IP (np. 192.168.111.xxx)',
                'enter_command': 'Wprowadź polecenie ADB',
                'output': 'Wynik zostanie pokazany tutaj.',
                'buttons': {
                    "Brightness Up": "Jasność w górę",
                    "Brightness Down": "Jasność w dół",
                    "Volume Up": "Głośność w górę",
                    "Volume Down": "Głośność w dół",
                    "Power": "Zasilanie",
                    "Home": "Strona główna",
                    "Assistant": "Asystent",
                    "Back": "Wstecz",
                    "Menu": "Menu",
                    "Search": "Szukaj",
                    "Swipe Up": "Przesuń w górę",
                    "Swipe Down": "Przesuń w dół",
                    "Swipe Left": "Przesuń w lewo",
                    "Swipe Right": "Przesuń w prawo",
                    "Touch": "Dotknij"
                }
            },
            'de': {
                'connect': 'Verbinden',
                'disconnect': 'Trennen',
                'list_devices': 'Geräte auflisten',
                'send': 'Senden',
                'swipe': 'Wischen',
                'touch': 'Berühren',
                'enter_ip': 'IP eingeben (z.B. 192.168.111.xxx)',
                'enter_command': 'ADB-Befehl eingeben',
                'output': 'Ausgabe wird hier angezeigt.',
                'buttons': {
                    "Brightness Up": "Helligkeit erhöhen",
                    "Brightness Down": "Helligkeit verringern",
                    "Volume Up": "Lautstärke erhöhen",
                    "Volume Down": "Lautstärke verringern",
                    "Power": "Energie",
                    "Home": "Startseite",
                    "Assistant": "Assistent",
                    "Back": "Zurück",
                    "Menu": "Menü",
                    "Search": "Suche",
                    "Swipe Up": "Nach oben wischen",
                    "Swipe Down": "Nach unten wischen",
                    "Swipe Left": "Nach links wischen",
                    "Swipe Right": "Nach rechts wischen",
                    "Touch": "Berühren"
                }
            },
            'ru': {
                'connect': 'Подключить',
                'disconnect': 'Отключить',
                'list_devices': 'Список устройств',
                'send': 'Отправить',
                'swipe': 'Свайп',
                'touch': 'Коснуться',
                'enter_ip': 'Введите IP (например, 192.168.111.xxx)',
                'enter_command': 'Введите команду ADB',
                'output': 'Результат будет показан здесь.',
                'buttons': {
                    "Brightness Up": "Увеличить яркость",
                    "Brightness Down": "Уменьшить яркость",
                    "Volume Up": "Увеличить громкость",
                    "Volume Down": "Уменьшить громкость",
                    "Power": "Питание",
                    "Home": "Домой",
                    "Assistant": "Ассистент",
                    "Back": "Назад",
                    "Menu": "Меню",
                    "Search": "Поиск",
                    "Swipe Up": "Свайп вверх",
                    "Swipe Down": "Свайп вниз",
                    "Swipe Left": "Свайп влево",
                    "Swipe Right": "Свайп вправо",
                    "Touch": "Коснуться"
                }
            }
        }
        self.ip_address = TextInput(hint_text=self.translations[self.language]['enter_ip'], multiline=False, size_hint=(None, 1), width=200)
        self.output_label = Label(size_hint_y=None, height=200, text=self.translations[self.language]['output'])
        self.device_spinner = Spinner(text='Select Device', values=[], size_hint=(None, None), size=(200, 44))

    def update_language(self, spinner, text):
        self.language = text
        self.ip_address.hint_text = self.translations[self.language]['enter_ip']
        self.cmd_input.hint_text = self.translations[self.language]['enter_command']
        self.output_label.text = self.translations[self.language]['output']
        self.connect_btn.text = self.translations[self.language]['connect']
        self.disconnect_btn.text = self.translations[self.language]['disconnect']
        self.list_devices_btn.text = self.translations[self.language]['list_devices']
        self.send_btn.text = self.translations[self.language]['send']
        self.swipe_btn.text = self.translations[self.language]['swipe']
        self.touch_btn.text = self.translations[self.language]['touch']
        for btn, label in zip(self.command_buttons, self.translations[self.language]['buttons'].values()):
            btn.text = label

    def connect_adb(self, ip):
        try:
            result = subprocess.run(['adb', 'connect', ip], check=True, capture_output=True, text=True)
            self.output_label.text = result.stdout
        except subprocess.CalledProcessError as e:
            self.output_label.text = f"Error connecting to {ip}: {e}"

    def disconnect_adb(self):
        try:
            result = subprocess.run(['adb', 'disconnect'], check=True, capture_output=True, text=True)
            self.output_label.text = result.stdout
        except subprocess.CalledProcessError as e:
            self.output_label.text = f"Error disconnecting: {e}"

    def list_devices(self):
        try:
            result = subprocess.run(['adb', 'devices', '-l'], check=True, capture_output=True, text=True)
            self.output_label.text = result.stdout
            devices = [line.split()[0] for line in result.stdout.splitlines() if 'device' in line and not line.startswith('List')]
            self.device_spinner.values = devices
            if devices:
                self.device_spinner.text = devices[0]
                self.selected_device = devices[0]
        except subprocess.CalledProcessError as e:
            self.output_label.text = f"Error listing devices: {e}"

    def send_adb_command(self, command):
        if self.selected_device:
            command = f"adb -s {self.selected_device} shell {command}"
        else:
            command = f"adb shell {command}"
        try:
            result = subprocess.run(command.split(), check=True, capture_output=True, text=True)
            self.output_label.text = result.stdout
        except subprocess.CalledProcessError as e:
            self.output_label.text = f"Error executing command: {e}"

    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Language selection
        language_spinner = Spinner(
            text='en',
            values=('en', 'pl', 'de', 'ru'),
            size_hint=(None, None),
            size=(100, 44)
        )
        language_spinner.bind(text=self.update_language)
        layout.add_widget(language_spinner)

        # Connection controls
        connection_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.connect_btn = Button(text=self.translations[self.language]['connect'], size_hint=(None, 1), width=100)
        self.connect_btn.bind(on_press=lambda instance: self.connect_adb(self.ip_address.text))
        self.disconnect_btn = Button(text=self.translations[self.language]['disconnect'], size_hint=(None, 1), width=100)
        self.disconnect_btn.bind(on_press=lambda instance: self.disconnect_adb())
        self.list_devices_btn = Button(text=self.translations[self.language]['list_devices'], size_hint=(None, 1), width=100)
        self.list_devices_btn.bind(on_press=lambda instance: self.list_devices())
        connection_layout.add_widget(self.ip_address)
        connection_layout.add_widget(self.connect_btn)
        connection_layout.add_widget(self.disconnect_btn)
        connection_layout.add_widget(self.list_devices_btn)
        layout.add_widget(connection_layout)

        # Device selection
        layout.add_widget(self.device_spinner)

        # Scrollable area for buttons
        scrollview = ScrollView(size_hint=(1, None), size=(400, 300))
        button_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))

        self.command_buttons = []
        buttons = {
            "Brightness Up": "input keyevent 221",
            "Brightness Down": "input keyevent 220",
            "Volume Up": "input keyevent 24",
            "Volume Down": "input keyevent 25",
            "Power": "input keyevent 26",
            "Home": "input keyevent 3",
            "Assistant": "input keyevent 219",
            "Back": "input keyevent 4",
            "Menu": "input keyevent 1",
            "Search": "input keyevent 84",
            "Swipe Up": "input swipe 500 1000 500 500",
            "Swipe Down": "input swipe 500 500 500 1000",
            "Swipe Left": "input swipe 1000 500 500 500",
            "Swipe Right": "input swipe 500 500 1000 500",
            "Touch": "input tap 500 500"
        }

        for label, command in buttons.items():
            btn = Button(text=self.translations[self.language]['buttons'][label], size_hint_y=None, height=40)
            btn.bind(on_press=lambda instance, cmd=command: self.send_adb_command(cmd))
            button_layout.add_widget(btn)
            self.command_buttons.append(btn)

        scrollview.add_widget(button_layout)
        layout.add_widget(scrollview)

        # Custom swipe and touch options
        custom_swipe_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.swipe_start_x = TextInput(hint_text='Start X', multiline=False, size_hint=(None, 1), width=80)
        self.swipe_start_y = TextInput(hint_text='Start Y', multiline=False, size_hint=(None, 1), width=80)
        self.swipe_end_x = TextInput(hint_text='End X', multiline=False, size_hint=(None, 1), width=80)
        self.swipe_end_y = TextInput(hint_text='End Y', multiline=False, size_hint=(None, 1), width=80)
        self.swipe_btn = Button(text=self.translations[self.language]['swipe'], size_hint=(None, 1), width=100)
        self.swipe_btn.bind(on_press=lambda instance: self.send_adb_command(
            f"input swipe {self.swipe_start_x.text} {self.swipe_start_y.text} {self.swipe_end_x.text} {self.swipe_end_y.text}"
        ))
        custom_swipe_layout.add_widget(self.swipe_start_x)
        custom_swipe_layout.add_widget(self.swipe_start_y)
        custom_swipe_layout.add_widget(self.swipe_end_x)
        custom_swipe_layout.add_widget(self.swipe_end_y)
        custom_swipe_layout.add_widget(self.swipe_btn)
        layout.add_widget(custom_swipe_layout)

        custom_touch_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.touch_x = TextInput(hint_text='X', multiline=False, size_hint=(None, 1), width=80)
        self.touch_y = TextInput(hint_text='Y', multiline=False, size_hint=(None, 1), width=80)
        self.touch_btn = Button(text=self.translations[self.language]['touch'], size_hint=(None, 1), width=100)
        self.touch_btn.bind(on_press=lambda instance: self.send_adb_command(
            f"input tap {self.touch_x.text} {self.touch_y.text}"
        ))
        custom_touch_layout.add_widget(self.touch_x)
        custom_touch_layout.add_widget(self.touch_y)
        custom_touch_layout.add_widget(self.touch_btn)
        layout.add_widget(custom_touch_layout)

        # Command line input
        cmd_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.cmd_input = TextInput(hint_text=self.translations[self.language]['enter_command'], multiline=False)
        self.send_btn = Button(text=self.translations[self.language]['send'], size_hint=(None, 1), width=100)
        self.send_btn.bind(on_press=lambda instance: self.send_adb_command(self.cmd_input.text))
        cmd_layout.add_widget(self.cmd_input)
        cmd_layout.add_widget(self.send_btn)

        layout.add_widget(cmd_layout)

        # Output label
        layout.add_widget(self.output_label)

        # Mini keyboard
        keyboard_layout = GridLayout(cols=10, spacing=5, size_hint_y=None)
        keyboard_layout.bind(minimum_height=keyboard_layout.setter('height'))
        keys = "1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
        for key in keys:
            btn = Button(text=key, size_hint_y=None, height=40)
            btn.bind(on_press=lambda instance, k=key: self.send_adb_command(f"input text '{k}'"))
            keyboard_layout.add_widget(btn)

        layout.add_widget(keyboard_layout)

        return layout

if __name__ == '__main__':
    ADBControlApp().run()