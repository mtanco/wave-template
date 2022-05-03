from h2o_wave import Q, app, handle_on, main, on, ui
from loguru import logger

from .usecase_config import UsecaseConfiguration
from .utils import title_format
from .wave_utils import handle_crash, html_python_code, switch_themes

UC = UsecaseConfiguration()


@app("/")
async def serve(q: Q):
    """This function will route the user based on how they have interacted with the application."""
    logger.info("Handling user interaction.")

    try:
        # Sets up the application
        if not q.client.initialized:
            await initialize_new_client(q)

        # Handles all button clicks
        await handle_on(q)

        # Saves content to the screen
        await q.page.save()
    except Exception as ex:
        logger.error(ex)
        await handle_crash(q, app_name=UC.app_title, card_name="crash")


async def initialize_new_client(q: Q):
    """This function will setup the app for any browser who has not been here before."""
    if not q.user.initialized:
        await initialize_new_user(q)
    logger.info("Initializing client.")

    render_base_ui(q)

    q.client.active_cards = []

    q.client.dark_mode = not UC.dark_mode
    switch_themes(q)

    await overview(q)

    q.client.initialized = True


async def initialize_new_user(q: Q):
    """
    This function will setup the app for any user who has not been here before.
    """
    if not q.app.initialized:
        await initialize_app(q)
    logger.info("Initializing user.")

    q.user.initialized = True


async def initialize_app(q: Q):
    """
    This function will setup the app with any information that should be shared across all users
    """
    logger.info("Initializing app.")

    q.app.initialized = True


def render_base_ui(q: Q):
    """Creating the base ui components of this application."""
    q.page["meta"] = ui.meta_card(
        box="",
        title=UC.app_title,
        tracker=ui.tracker(type=ui.TrackerType.GA, id=UC.app_ga),
        layouts=[
            ui.layout(
                breakpoint="xl",
                width="1200px",
                height="100vh",
                zones=[
                    ui.zone("header"),
                    ui.zone("commands"),
                    ui.zone("full_content", size="1"),
                    ui.zone("footer"),
                ],
            )
        ],
    )
    q.page["header"] = ui.header_card(
        box="header",  # Using the grid-based layout to put each card in a specific location
        title=UC.app_title,
        subtitle=UC.app_subtitle,
        image=UC.app_image,
        items=[ui.menu(items=[ui.command(name="color_theme")])],
        #commands=[ui.command(name="color_theme")],
        nav=[
            ui.nav_group(
                label="",
                items=[
                    ui.nav_item("overview", "Overview", icon="HomeSolid"),
                    ui.nav_item("source_code", "App Code", icon="Code"),
                ],
            )
        ],
    )
    q.page["footer"] = ui.footer_card(
        box="footer", caption="Made with 💛️ using [H2O Wave](https://wave.h2o.ai)."
    )


@on()
async def color_theme(q: Q):
    """Handle the user request to change from dark to light mode, or vice versa."""
    logger.info("Changing the theme.")
    switch_themes(q)


@on()
async def overview(q: Q):
    """
    Handle the user request to see the overview page UI objects.
    The information on this page is use-case specific.
    """
    prepare_new_page(q, "overview")

    q.page["overview"] = ui.form_card(
        box="full_content",
        items=[],
    )
    q.client.active_cards.append("overview")


@on()
async def source_code(q: Q):
    """
    Handle the user request to see the source code page UI objects.
    """
    prepare_new_page(q, "source_code")

    html_code = html_python_code("app.py")

    q.page["source_code"] = ui.frame_card(
        box="full_content",
        title="Application Code",
        content=html_code
    )

    q.client.active_cards.append("source_code")


def prepare_new_page(q: Q, page_name: str):
    """Common tasks that run any time the users switches pages they want to view."""
    logger.info(f"On the {page_name} page.")

    for c in q.client.active_cards:
        del q.page[c]
    q.client.active_cards = []

    q.page["meta"].title = UC.app_title + " - " + title_format(page_name)
