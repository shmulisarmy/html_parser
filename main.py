from html_ import HTML
from domTree import DomTree


html_string = (
    "<body class='fuck'>\n"
    "    <nav class='fuck' id='fire' data='team' it='hello'>\n"
    "        <div>\n"
    "            hello\n"
    "        </div>\n"
    "        <div class='fuck' it='hello'>\n"
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



div = document.search_for_element(tag_name='div', class_name='fuck')
another_div = document.search_for_elements(tag_name='div')[-1]




# cp: DomTree = nav.get_closest_sharing_parrent(div)

# print(f"{cp.create_query() = }")
bcs = div.best_common_selector(another_div)

print(f"{bcs = }")


# print(f"{document.querySelector('body').search_for_elements(tag_name = None, class_name = 'fuck', id = None) = }")