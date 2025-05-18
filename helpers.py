def get_html_and_css(html_file, css_file, data=None):
    try:
        with open(f'templates/{html_file}.html', 'r', encoding='utf-8') as f_html:
            html = f_html.read()
    except FileNotFoundError:
        return f"<h1>Error: HTML file '{html_file}.html' not found.</h1>"

    try:
        with open(f'static/css/{css_file}.css', 'r', encoding='utf-8') as f_css:
            css = f_css.read()
    except FileNotFoundError:
        css = ""

    injected_html = html.replace("</head>", f"<style>{css}</style>\n</head>")


    if data and isinstance(data, dict):
        for key, value in data.items():
            injected_html = injected_html.replace(f"{{{{ {key} }}}}", str(value))

    return injected_html
