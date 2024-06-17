from html_ import HTML
from custom_packages.searchTree import SearchTree
import re



text_tree = SearchTree()
text_reverse_tree = SearchTree()



class DomTree:
    def __init__(self, tagname, parentNode = None, textContent = None):
        self.tagname = tagname
        self.childrenNodes = []
        self.parentNode = parentNode
        self.textContent = textContent
        self.atributes = {}

    def traverse(self, level=0):
        result = []
        indent_spaces = "    "*level
        result.append(f"{indent_spaces}{self.tagname = } {self.atributes = } at level {level}")
        for element in self.childrenNodes:
            element: DomTree
            result.extend(element.traverse(level=level+1))

        return result
    
    def __repr__(self):
        return '\n'.join(self.traverse())
            

    @classmethod
    def create_document_from(cls, html_node_list: list['DomTree']):
        begin = 0
        end = len(html_node_list)-1

        document = DomTree("document")
        at = document

        while begin < end:
            html_node = html_node_list[begin]
            Type, content = HTML.str_type(html_node)
            if Type == "tag":
                previus_element = at
                find_tag_name_pattern = re.compile("\w+")
                tag_name: str = find_tag_name_pattern.match(content).group(0)
                at = DomTree(tag_name, previus_element)
                previus_element.childrenNodes.append(at)
                pattern = re.match(r"(\w+)(.*)", content).group(0)
                at.atributes = HTML.parse_attributes(pattern)
            elif Type == "endTag":
                at = at.parentNode
            else:
                at.textContent = content
                text_tree.insertWithValue(content, at)
                text_reverse_tree.insertWithValue(content[::-1], at)

                


            begin += 1

        return document
    
    @classmethod
    def create_template(cls, html_node_list):
        begin = 0
        end = len(html_node_list)-1

        document = DomTree("document")
        at = document

        print(f"function create_element(){'{'}")

        while begin < end:
            html_node = html_node_list[begin]
            Type, content = HTML.str_type(html_node)
            if Type == "tag":
                previus_element = at
                at = DomTree(content, previus_element)
                previus_element.childrenNodes.append(at)
                print(f"    const {content} = document.createElement('{content}')")
                print(f"    {previus_element.tagname}.appendChild({content})")
            elif Type == "endTag":
                at = at.parentNode


            begin += 1

    
    def querySelector(self, query: str):
        for node in self.childrenNodes:
            node: DomTree
            if node.tagname == query:
                return node
            
        for node in self.childrenNodes:
            queried_node = node.querySelector(query)
            if queried_node:
                return queried_node
            
    def querySelectorAll(self, query: str):
        results = []
        for node in self.childrenNodes:
            node: DomTree
            if node.tagname == query:
                results.append(node)
            
        for node in self.childrenNodes:
            results.extend(node.querySelectorAll(query))

        return results


    def create_query(node):
        """returns a string of the best query to make in order to get the node element"""
        query: str = node.tagname
        if not node.parentNode:
            return node.tagname
        
        parrent: DomTree = node.parentNode
        all_similar_siblings = parrent.querySelectorAll(query)
        if len(all_similar_siblings) == 1:
            return f"{parrent.create_query()}.querySelector({query})"

        for index, element in enumerate(all_similar_siblings):
            if id(element) == id(node):
                return f"{parrent.create_query()}.querySelectorAll({query})[{index}]"

    # def find_by_text(node, search_text: str):
    #     greatest_match: int = 0
    #     best_node_matchs = []
    #     for child_node in node.childrenNodes:
    #         child_node: DomTree
    #         comparing_against: str = child_node.textContent
    #         if len(comparing_against) < greatest_match:
    #             continue
    #         char_match_amount = char_match_amount(search_text, comparing_against)
    #         if char_match_amount > greatest_match:
    #             greatest_match = char_match_amount
    #             best_node_matchs = [node]
    #         elif char_match_amount == greatest_match:
    #             best_node_matchs.append(node)

    # @classmethod
    # def find_by_text(cls, search_text: str):
    #     text_tree_results = sorted(text_tree.getValueListOfBestMatchest(search_text), key = lambda node: len(node.textContent), reverse=True)
    #     text_reverse_tree_results = sorted(text_reverse_tree.getValueListOfBestMatchest(search_text[::-1]), key = lambda node: len(node.textContent), reverse=True)


    #     index_ = 0
    #     reverses_index_ = 0

    #     best_match = None

    #     while True:
    #         if len(text_tree_results[index_].textContent) + len(text_tree_results[index_].textContent) < len(search_text):
    #             best_match = [text_reverse_tree_results[index_], text_tree_results[index_].textContent]
    #         else:
    #             smaller_current = min(len(text_reverse_tree_results[index_].textContent), len(text_reverse_tree_results[reverses_index_].textContent))


    @classmethod
    def find_by_text(cls, search_text: str) -> list['DomTree']:
        text_tree_results = text_tree.getValueListOfBestMatchest(search_text)
        text_reverse_tree_results = text_reverse_tree.getValueListOfBestMatchest(search_text[::-1])


        print(f"{[node.textContent for node in text_tree_results] = }")
        print(f"{[node.textContent for node in text_reverse_tree_results] = }")

        resulting_node_combos = []

        for index_, current_text in enumerate(text_tree_results):
            for textContent, current_reverse in enumerate(text_reverse_tree_results):
                if len(current_text.textContent) + len(current_reverse.textContent) > len(search_text):
                    continue
                middle_text = search_text[len(current_text.textContent):-len(current_reverse.textContent)] 
                if not middle_text:
                    resulting_node_combos.append([current_text, current_reverse])
                else:
                    middle_results = DomTree.find_by_text(middle_text)
                    resulting_node_combos.extend([current_text + inner_combo + current_reverse for inner_combo in middle_results])

        return resulting_node_combos
    
    def recursive_parrents(self):
        """works like an enumerater"""
        node = self
        index = 0
        while node.parentNode:
            node = node.parentNode
            yield (index, node)
            index+=1
    
    def get_closest_sharing_parrent(self, other) -> 'DomTree':
        best_pair: ['DomTree']|None = None
        closest_dom_distance = float('inf')
        for index, parrent in self.recursive_parrents():
            for other_index, other_parrent in other.recursive_parrents():
                if parrent == other_parrent:
                    current_dom_distance = index+other_index
                    if current_dom_distance < closest_dom_distance:
                        best_pair = [parrent, other_parrent]
                        closest_dom_distance = current_dom_distance

        return best_pair
                    


            
        

                


            


def char_match_amount(a: str, b: str) -> int|bool:
    chars_that_match: int = 0
    for index in range(max(len(a), len(b))):
        if a[index] == b[index]:
            chars_that_match += 1
        else:
            return char_match_amount
    return True

        
