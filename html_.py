class HTML:
    def __init__(self, arguments):
        pass

    @classmethod
    def get_html_tag_list(cls, html_string):
        html_tag_list = []
        current = []
        for index, char in enumerate(html_string):
            if char == " " or char == "\n":
                continue
            if char == "<":
                if current:
                    html_tag_list.append(''.join(current))
                    current.clear()
            current.append(char)
            if char == ">":
                if current:
                    html_tag_list.append(''.join(current))
                    current.clear()

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


