import os
import sys
import traceback

from h2o_wave import Q, ui
from h2o_wave.core import expando_to_dict


async def handle_crash(q: Q, app_name, card_name):
    """Pretty page to show if the app crashes."""
    q.page.drop()

    error_msg_items = [
        ui.text_xl("Error!"),
        ui.text_l(
            "Apologies for the inconvenience. "
            f"Please refresh your browser to restart {app_name}. "
        ),
        ui.text_xs("⠀"),
    ]
    error_report_items = [
        ui.text(
            "To report this crash, please send an email to [cloud-feedback@h2o.ai](cloud-feedback@h2o.ai) "
            "with the following information:"
        ),
        ui.text_xs("⠀"),
        ui.text_l(app_name),
    ]
    type_, value_, traceback_ = sys.exc_info()
    stack_trace = traceback.format_exception(type_, value_, traceback_)
    stack_trace_items = [ui.text("**Stack Trace**")] + [
        ui.text(f"`{x}`") for x in stack_trace
    ]
    q_args = [f"{k}: {v}" for k, v in expando_to_dict(q.args).items()]
    q_args_str = "#### q.args\n```\n" + "\n".join(q_args) + "\n```"
    q_args_items = [ui.text_m(q_args_str)] + [ui.text_xs("⠀")]
    error_report_items.extend(q_args_items + stack_trace_items)
    error_report = [
        ui.expander(
            name="error_report",
            label="Report this error",
            expanded=False,
            items=error_report_items,
        )
    ]
    error_items = error_msg_items + error_report + [ui.text_xs("⠀")] * 2
    q.page[card_name] = ui.form_card(box="1 1 -1 -1", items=error_items)

    q.app.crash_report = (
        "#### Stack Trace\n" + "```\n" + "".join(stack_trace) + "\n```\n" + q_args_str
    )
    print(q.app.crash_report)

    await q.page.save()


def switch_themes(q: Q):
    """Change the app from light to dark mode"""
    if q.client.dark_mode:
        q.page["header"].commands[0].label = "Dark Mode"
        q.page["header"].commands[0].icon = "ClearNight"
        q.page["meta"].theme = "light"
        q.client.dark_mode = False
    else:
        q.page["header"].commands[0].label = "Light Mode"
        q.page["header"].commands[0].icon = "Sunny"
        q.page["meta"].theme = "neon"
        q.client.dark_mode = True


def ui_table_from_df(df, name: str, n=10):
    """Create a Wave UI table from a pandas dataframe with no clickable rows"""
    n = min(n, len(df))

    table = ui.table(
        name=name,
        columns=[
            ui.table_column(name=str(x), label=str(x), sortable=True, filterable=True, link=False)
            for x in df.columns.values
        ],
        rows=[
            ui.table_row(
                name=str(i), cells=[str(df[col].values[i]) for col in df.columns.values]
            )
            for i in range(n)
        ],
    )
    return table


def html_python_code(file_to_display):
    """Create code-colored text as html based on python standards"""

    from pygments import highlight
    from pygments.formatters.html import HtmlFormatter
    from pygments.lexers import get_lexer_by_name

    local_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(local_dir, file_to_display)) as f:
        contents = f.read()

    py_lexer = get_lexer_by_name("python")
    html_formatter = HtmlFormatter(full=True, style="xcode")
    code = highlight(contents, py_lexer, html_formatter)

    return code
