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




html = HTML.get_html_tag_list(html_string)


document: DomTree = DomTree.create_document_from(html)


DomTree.all_nodes_in_order = [child for child in document.breadth_first_search_child_generator()]


















