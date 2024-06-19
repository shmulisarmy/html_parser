from html_ import HTML
from domTree import DomTree


html_string = (
    "<body class='fuck'>\n"
    "    <nav class='fuck' id='fire' data='team' it='hello'>\n"
    "        <div>hello</div>\n"
    "        <div class='fuck' it='hello'>fuck</div>\n"
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

print(document.atributes)



div = document.search_for_element(tag_name='div', class_name='fuck')
another_div = document.search_for_elements(tag_name='div')[-1]


print(f"{div = }")
print(f"{another_div = }")


print(div.create_template())

bcs = div.best_common_selector(another_div)

print(f"{bcs = }")


matching_text_elements: list[list[DomTree]] = document.find_by_text("hellofuck")



first_matching_text_elements: list[DomTree] = matching_text_elements[0]

print(f"{first_matching_text_elements = }")

best_common_selector = first_matching_text_elements[0].best_common_selector(*first_matching_text_elements[1:])



print(f"{best_common_selector = }")



tested_selector = document.querySelector('body').search_for_elements(tag_name = 'div')

print(f"{tested_selector = }")


# print(f"{[node for node in document.depth_first_search_child_generator()]}")