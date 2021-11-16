from tkf import App
from hubstore.misc.theme import get_theme
from hubstore.view.main import Main


def main():
    # The App
    app = App()
    # Title
    app.title = "Hubstore"
    # Geometry
    app.geometry = "900x550+0+0"
    # Resizable
    app.resizable = (False, False)
    # Set theme
    app.theme = get_theme()
    # Set view
    app.view = Main(app)
    # Center the window
    app.center()
    # Lift off !
    app.start()


if __name__ == "__main__":
    main()
