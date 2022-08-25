import toml
from h2o_wave import Q, app, handle_on, main, on, ui
from loguru import logger

from .wave_utils import clear_cards, html_python_code, standard_app_layout


@app("/")
async def serve(q: Q):
    """
    Handle all client interactions with this app such as visits, button clicks, and triggered events
    """
    logger.info("Handling user interaction")

    if not q.client.initialized:
        initialize_client(q)

    if not await handle_on(q):
        await home(q)

    await q.page.save()


def initialize_client(q: Q):
    """
    Setup steps and variables that are needed for each individual browser tab
    """
    if not q.user.initialized:
        initialize_user(q)

    logger.info("Initializing client")

    standard_app_layout(q)

    q.client.cards = []

    q.client.initialized = True


def initialize_user(q: Q):
    """
    Setup steps and variables that are shared across all browser tabs of this user
    """
    if not q.app.initialized:
        initialize_app(q)

    logger.info("Initializing user")
    q.user.initialized = True


def initialize_app(q: Q):
    """
    Setup steps and variables that are shared across all users of this app
    """
    logger.info("Initializing app")
    q.app.toml = toml.load("app.toml")
    q.app.initialized = True


@on()
async def home(q: Q):
    """
    Prepare and display the home page
    """
    logger.info("Setting up home page")
    clear_cards(q)

    q.page["overview"] = ui.form_card(
        box="content",
        items=[],
    )
    q.client.cards.append("overview")


@on()
async def source_code(q: Q):
    """
    Handle the user request to see the source code page UI objects.
    """
    logger.info("Setting up source code page")
    clear_cards(q)

    q.page["source_code"] = ui.frame_card(
        box="content", title="App Code", content=html_python_code("app.py")
    )
    q.client.cards.append("source_code")
