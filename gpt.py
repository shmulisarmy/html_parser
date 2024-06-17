
import re

class HTML:
    @classmethod
    def parse_attributes(cls, attribute_string):
        attributes = {}
        # Regex to find attributes in the form key="value", key='value', or key=value
        attr_re = re.compile(r'(\w+)=["\']?([^"\'>\s]+)["\']?')
        for match in attr_re.findall(attribute_string):
            attributes[match[0]] = match[1]
        return attributes

    @classmethod
    def str_type(cls, string):
        if string[0] == "<" and string[-1] == ">":
            if string[1] == "/":
                Type = "endTag"
                _content = string[2:-1]
                attributes = {}
            else:
                Type = "tag"
                # Extract the tag and attributes
                tag_content = string[1:-1]
                tag_match = re.match(r"(\w+)(.*)", tag_content)
                _content = tag_match.group(1)
                print(f"{tag_match.group(2) = }")
                attributes = cls.parse_attributes(tag_match.group(2))
        else:
            Type = "text"
            _content = string
            attributes = {}
        
        return (Type, _content, attributes)

