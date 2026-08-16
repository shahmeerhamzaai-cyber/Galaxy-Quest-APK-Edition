from kivy.app import App
from kivy.uix.label import Label
from galaxy_quest import main



class GalaxyQuest(App):
    def build(self):
        return Label(
            text="Galaxy Quest 🚀",
            font_size=40
        )


if __name__ == "__main__":
    main()