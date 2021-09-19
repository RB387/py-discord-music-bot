import toml
from constants import CONFIG_PATH
from dotenv import load_dotenv

from lib.app import App
from lib.core.injector import DependencyInjector


def main():
    load_dotenv()
    config = toml.load(CONFIG_PATH)

    injector = DependencyInjector(config)

    app = App(injector)
    app.run()


if __name__ == '__main__':
    main()
