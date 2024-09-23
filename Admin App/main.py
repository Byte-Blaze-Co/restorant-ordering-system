from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


class Sidebar(BoxLayout):
    def __init__(self, **kwargs):
        super(Sidebar, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 0.2

        # Add buttons for menu
        self.add_widget(Button(text="Dashboard"))
        self.add_widget(Button(text="Gelir Analizi", on_press=self.switch_to_income))
        self.add_widget(Button(text="Ürün Yönetimi"))

    def switch_to_income(self, instance):
        app = App.get_running_app()
        app.root.current = "income_screen"


class IncomeScreen(Screen):
    def __init__(self, **kwargs):
        super(IncomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Add the title
        layout.add_widget(Label(text="Gelir Analizi", font_size=24))

        # Add a mock chart (LineChart could be implemented or a custom graph)
        chart_layout = BoxLayout(size_hint_y=0.4)
        chart_layout.add_widget(Label(text="[Mock Chart]", font_size=18))
        layout.add_widget(chart_layout)

        # Add a table of income data
        income_table = GridLayout(cols=4, size_hint_y=None)
        income_table.bind(minimum_height=income_table.setter('height'))
        headers = ['Ay', 'Gelir', 'Gider', 'Net Kar']

        # Add table headers
        for header in headers:
            income_table.add_widget(Label(text=header, bold=True))

        # Add sample data
        data = [
            ['Ocak', '₺10,000', '₺4,000', '₺6,000'],
            ['Şubat', '₺8,000', '₺3,500', '₺4,500'],
            ['Mart', '₺12,000', '₺5,000', '₺7,000']
        ]

        for row in data:
            for col in row:
                income_table.add_widget(Label(text=col))

        # Add table to scrollview in case of larger datasets
        scroll = ScrollView(size_hint=(1, 0.6))
        scroll.add_widget(income_table)
        layout.add_widget(scroll)

        self.add_widget(layout)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='horizontal')

        # Sidebar menu
        layout.add_widget(Sidebar())

        # Main area content
        main_content = BoxLayout(orientation='vertical')
        main_content.add_widget(Label(text="Hoşgeldiniz! Yönetim Paneli"))

        layout.add_widget(main_content)
        self.add_widget(layout)


class AdminApp(App):
    def build(self):
        # Screen manager for switching between screens
        sm = ScreenManager()

        # Add screens to the manager
        sm.add_widget(MainScreen(name="main_screen"))
        sm.add_widget(IncomeScreen(name="income_screen"))

        return sm


if __name__ == "__main__":
    AdminApp().run()
