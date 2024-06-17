from html_ import HTML
from domTree import DomTree


html_string = (
    "<body class='fuck'>\n"
    "    <nav class='fuck' id='fire'>\n"
    "        <div>\n"
    "            hello\n"
    "        </div>\n"
    "        <div class='fuck'>\n"
    "            hello you\n"
    "        </div>\n"
    "    </nav>\n"
       "    <nav class='side' id='figma'>\n"
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

print(html)

document: DomTree = DomTree.create_document_from(html)

print(document.atributes)



nav = document.search_for_element(tag_name='nav', class_name='fuck', id='fire')
div = document.search_for_element(tag_name='div', class_name='fuck')


cp = nav.best_common_selector(div)

print(cp)

# from domTree import text_tree


# text_tree.debug()


# print()
# print(f"{[[node.textContent for node in combo] for combo in DomTree.find_by_text('hellohelloyouyou')] = }")

