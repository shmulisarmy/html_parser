import re


class HTML:
    def __init__(self, arguments):
        pass

    @classmethod
    def get_html_tag_list(cls, html_string):
        html_tag_list = []
        inside_arrows = []
        for index, char in enumerate(html_string):
            if  char == "\n":
                continue
            if not inside_arrows and char == " ":
                continue
            if char == "<":
                if inside_arrows:
                    html_tag_list.append(''.join(inside_arrows))
                    inside_arrows.clear()
            inside_arrows.append(char)
            if char == ">":
                if inside_arrows:
                    html_tag_list.append(''.join(inside_arrows))
                    inside_arrows.clear()

        return html_tag_list

    # @classmethod
    # def str_type(cls, string):
    #     """_class='navbar'"""
    #     if string[0] == "<" and string[-1] == ">":
    #         if string[1] == "/":
    #             Type = "endTag"
    #             _content = string[2:-1]
    #         else:
    #             Type = "tag"
    #             string: list
    #             _content = string[1:]
            
    #         in_string = False
    #         index = 0
    #         while True:
    #             char = string[index]
    #             if char == "_":
    #                 while string[index] != '_':
    #                     index += 1
    #             if char == "'" or char == '"':
    #                 in_string = not in_string
    #             index += 1

    @classmethod
    def str_type(cls, string):
        if string[0] == "<" and string[-1] == ">":
            if string[1] == "/":
                Type = "endTag"
                _content = string[2:-1]
            else:
                Type = "tag"
                string: list
                _content = string[1:-1]
            
        else:
            Type = "text"
            _content = string
        
        return (Type, _content)
    
    @classmethod
    def parse_attributes(cls, attribute_string):
        attributes = {}
        # Regex to find attributes in the form key="value"
        attr_re = re.compile(r"(\w+)='([^']*)'")
        for match in attr_re.findall(attribute_string):
            attributes[match[0]] = match[1]
        return attributes


e = HTML.parse_attributes("id='hey' class='school'")


print(e)