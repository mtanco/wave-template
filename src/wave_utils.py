import hashlib
import os

from h2o_wave import Q, ui


def ui_table_from_df(df, name: str, n=10):
    """
    Create a Wave UI table from a pandas dataframe with no clickable rows
    """
    n = min(n, len(df))

    table = ui.table(
        name=name,
        columns=[
            ui.table_column(
                name=str(x), label=str(x), sortable=True, filterable=True, link=False
            )
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


def html_python_code(file_to_display: str) -> str:
    """
    Create code-colored text as html based on python standards
    """

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


def clear_cards(q: Q) -> None:
    """
    Remove cards from the UI to prepare for a new user view
    """
    for c in q.client.cards:
        del q.page[c]
    q.client.cards = []


def standard_app_layout(q: Q):
    q.page["meta"] = ui.meta_card(
        box="",
        title=f"{q.app.toml['App']['Title']} | H2O.ai",
        theme="light",
        icon="https://cloud.h2o.ai/logo.svg",
        script=heap_analytics(
            userid=q.auth.subject,
            user_properties=f"{{version: '{q.app.toml['App']['Version']}', product: '{q.app.toml['App']['Title']}'}}",
        ),
        layouts=[
            # xs: portrait phones, s: landscape phones, m: tablets, l: desktop, xl: large desktop
            ui.layout(
                breakpoint="xs",
                height="100vh",
                zones=[ui.zone("device-not-supported")],
            ),
            ui.layout(
                breakpoint="l",
                height="100vh",
                max_width="1200px",
                zones=[
                    ui.zone(name="header"),
                    ui.zone(name="content", size="1"),
                    ui.zone(name="footer"),
                ],
            ),
        ],
    )

    q.page["device-not-supported"] = ui.form_card(
        box="device-not-supported",
        items=[
            ui.text_xl(
                "This app was built desktop; it is not available on mobile or tablets."
            )
        ],
    )

    q.page["header"] = ui.header_card(
        box="header",
        title=f"{q.app.toml['App']['Title']} v{q.app.toml['App']['Version']}",
        subtitle=q.app.toml["App"]["Description"],
        image="https://cloud.h2o.ai/logo.svg",
        items=[ui.menu(items=[ui.command(name="source_code", label="Source Code")])],
    )

    q.page["footer"] = ui.footer_card(
        box="footer",
        caption='Made with 💛 using <a href="https://wave.h2o.ai" target="_blank">H2O Wave</a>.',
    )


def heap_analytics(userid, user_properties=None) -> ui.inline_script:
    script = """
window.heap=window.heap||[],heap.load=function(e,t){window.heap.appid=e,window.heap.config=t=t||{};var r=document.createElement("script");r.type="text/javascript",r.async=!0,r.src="https://cdn.heapanalytics.com/js/heap-"+e+".js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(r,a);for(var n=function(e){return function(){heap.push([e].concat(Array.prototype.slice.call(arguments,0)))}},p=["addEventProperties","addUserProperties","clearEventProperties","identify","resetIdentity","removeEventProperty","setEventProperties","track","unsetEventProperty"],o=0;o<p.length;o++)heap[p[o]]=n(p[o])};
heap.load("1090178399");  
    """

    if (
        userid is not None
    ):  # is OIDC Enabled? we do not want to identify all non-logged in users as "none"
        identity = hashlib.sha256(userid.encode()).hexdigest()
        script += f"heap.identify('{identity}');"

    if user_properties is not None:
        script += f"heap.addUserProperties({user_properties})"

    return ui.inline_script(content=script)
