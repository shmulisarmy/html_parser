import unittest
from src.html_ import HTML
from src.domTree import DomTree




class Tests(unittest):
    def __init__(self):
        pass
    def __setup__(self):
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
        html_list = HTML.get_html_tag_list(html_string)


        self.document: DomTree = DomTree.create_document_from(html_list)

    def test_multiple(self):
        assert self.document.atributes == {}


        div = self.document.search_for_element(tag_name='div', class_name='fuck')
        assert div
        assert 'fuck' in div.classList
        another_div = self.document.search_for_elements(tag_name='div')[-1]
        assert another_div
        assert another_div.tagname == 'div'

        bcs = div.best_common_selector(another_div)

        assert bcs

        # assert another_div.childOf(bcs)

def test():
    print("this is a teset")
    assert False