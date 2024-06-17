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



print(document)


first_div = document.querySelector("div")
second_div = document.querySelectorAll("div")[-1]




print(first_div.get_closest_sharing_parrent(second_div))

# from domTree import text_tree


# text_tree.debug()


# print()
# print(f"{[[node.textContent for node in combo] for combo in DomTree.find_by_text('hellohelloyouyou')] = }")

