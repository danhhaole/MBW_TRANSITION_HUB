import re
from bs4 import BeautifulSoup

def convert_html_for_facebook(html):
    if not html:
        return ""

    # --- replace common html blocks ---
    html = re.sub(r"<br\s*/?>", "\n", html)
    html = html.replace("<li>", "• ").replace("</li>", "\n")
    html = html.replace("<p>", "").replace("</p>", "\n\n")

    # <strong> ... </strong>
    html = re.sub(r"<strong>(.*?)</strong>", r"**\1**", html)

    # <a href="">text</a> → text
    html = re.sub(r'<a [^>]+>(.*?)</a>', r"\1", html)

    # remove all remaining html
    text = BeautifulSoup(html, "html.parser").get_text()

    # cleanup
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
