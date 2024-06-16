from html_ import HTML
from domTree import DomTree


html_string = (
    "<body>\n"
    "    <nav>\n"
    "        <div>\n"
    "            hello\n"
    "        </div>\n"
    "        <div>\n"
    "            hello you\n"
    "        </div>\n"
    "    </nav>\n"
       "    <nav>\n"
            "fuck"
    "        <div>\n"
    "            hello\n"
    "        </div>\n"
    "        <div>\n"
    "            you\n"
    "        </div>\n"
    "    </nav>\n"

    "</body>"
) 








html = HTML.get_html_tag_list(html_string)

document: DomTree = DomTree.create_document_from(html)





from domTree import text_tree


text_tree.debug()


print()
print(f"{[[node.textContent for node in combo] for combo in DomTree.find_by_text('hellohelloyouyou')] = }")

