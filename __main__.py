from html_ import HTML
from domTree import DomTree


html_string = (
    "<body class='hello'>\n"
    "    <nav class='fuck' id='fire' data='team' it='hello'>\n"
    "        <div>hello</div>\n"
    "        <div class='fuck' it='hello'>hi</div>\n"
    "    </nav>\n"
       "    <nav class='side' id='figma'>\n"
            "fuck"
    "        <div>\n"
    "            hello\n"
    "        </div>\n"
    "        <div>you</div>\n"
    "    </nav>\n"

    "</body>"
)

print(f"{html_string = }")






html = HTML.get_html_tag_list(html_string)

print(html)

document: DomTree = DomTree.create_document_from(html)


DomTree.all_nodes_in_order = [child for child in document.breadth_first_search_child_generator()]

print(document.atributes)



div = document.search_for_element(tag_name='div', class_name='fuck')
another_div = document.search_for_elements(tag_name='div')[-1]


print(f"{div = }")
print(f"{another_div = }")


print(div.create_template())

bcs = div.best_common_selector(another_div)

print(f"{bcs = }")


matching_text_elements: list[list[DomTree]] = document.find_by_text("hellofuck")






tested_selector = document.querySelector('body').search_for_elements(tag_name = 'div')

print(f"{tested_selector = }")




