"""global constants:
        INDENT: used place in indents in the generated code
        text_tree, text_reverse_tree: used for searching for elements by text dinamicly"""



from html_ import HTML
# from collections import defaultdict
from custom_packages.searchTree import SearchTree
import re
from colors import blue, green, yellow


INDENT = "  "
text_tree = SearchTree()
text_reverse_tree = SearchTree()



class DomTree:
    def __init__(self, tagname, parentNode = None, textContent = None):
        self.tagname = tagname
        self.childrenNodes = []
        self.parentNode = parentNode
        self.textContent = textContent
        self.classList = []
        self.id = None

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
        return f"{blue(self.tagname)} {self.id = } class={self.classList} {' '.join(yellow(f'{attr}={self.atributes[attr]}') for attr in self.atributes.keys())}"
            

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
                atributes = HTML.parse_attributes(pattern)
                if 'id' in atributes:
                    at.id = atributes['id']
                    del atributes['id']
                if 'class' in atributes:
                    at.classList = atributes['class'].split(" ")
                    del atributes['class']
                at.atributes = atributes
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
                print(f"{INDENT}const {content} = document.createElement('{content}')")
                print(f"{INDENT}{previus_element.tagname}.appendChild({content})")
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
    
    def recursive_parrents(self) -> list[tuple]:
        results = []
        node = self
        index = 0
        while node.parentNode:
            node = node.parentNode
            results.append((index, node))
            index+=1
        return results

    def recursive_parrents_enumerater(self):
        """works like an enumerater"""
        node = self
        index = 0
        while node.parentNode:
            node = node.parentNode
            yield (index, node)
            index+=1
    
    
    def get_closest_sharing_parrent(*nodes: list['DomTree']) -> 'DomTree':
        """n*2 time and space complexity"""

        all_parrents = {}
        for element in nodes:
            assert isinstance(element, DomTree) #because it is plausable to make a mistake and have it be None via an invalid selector...
            element: DomTree
            for index, parrent in element.recursive_parrents_enumerater():
                parrent: DomTree
                if parrent not in all_parrents:
                    all_parrents[parrent] = [0, 0]
                all_parrents[parrent][0] += 1
                all_parrents[parrent][1] += index

        total_element_count = len(nodes)


        # part of higher order function
        def is_parrent_of_all_elements(parrent_as_a_key):
            value = all_parrents[parrent_as_a_key]
            number_of_children_here = value[0]

            return number_of_children_here == total_element_count


        sharing_parrents: iter = list(filter(is_parrent_of_all_elements, all_parrents.keys()))

        closest_parrent_distance = float('inf')
        closest_parrent = None
        for parrent in sharing_parrents:
            distance: int = all_parrents[parrent][1] 
            if distance < closest_parrent_distance:
                closest_parrent = parrent
                closest_parrent_distance = distance

        return closest_parrent




    def search_for_element(self, tag_name=None, class_name=None, id=None, atributes = {}) -> 'DomTree':
        print(f"{atributes = }")
        for node in self.childrenNodes:
            node: DomTree
            if node.tagname != tag_name:
                continue
            print(f"{node.atributes = }")
            if (class_name and class_name not in node.classList):
                continue
            if (id and node.id != id):
                continue
            if any(node.atributes.get(atr) != atributes[atr] for atr in atributes):
                continue
            return node
        
        for node in self.childrenNodes:
            node: DomTree
            result_in_child = node.search_for_element(tag_name=tag_name, class_name=class_name, id=id, atributes=atributes)
            if result_in_child:
                return result_in_child
            
    def search_for_elements(self, tag_name=None, class_name=None, id=None, atributes={}) -> list['DomTree']:
        results = []
        for node in self.childrenNodes:
            node: DomTree
            if tag_name and node.tagname != tag_name:
                continue
            if class_name and class_name not in node.classList:
                continue
            if id and node.id != id:
                continue
            if any(node.atributes.get(atr) != atributes[atr] for atr in atributes):
                continue
            results.append(node)
        
        for node in self.childrenNodes:
            node: DomTree
            results.extend(node.search_for_elements(tag_name=tag_name, class_name=class_name, id=id, atributes=atributes))

        return results
    
    def best_common_selector(self, *others: list['DomTree']) -> str:
        atributes = list(filter(lambda item: all(item[0] in other.atributes for other in others) and all(item[1] == other.atributes[item[0]] for other in others), self.atributes.items()))
        classList = list(filter(lambda class_name: all(class_name in other.classList  for other in others), self.classList))
        if all(self.tagname == other.tagname for other in others):
            tag_name = self.tagname
        else:
            tag_name = None


        closest_sharing_parrent: 'DomTree' = self.get_closest_sharing_parrent(self, *others)
        query = closest_sharing_parrent.create_query() + f".search_for_elements({tag_name = }, {classList = }, None, {atributes = })"

        return query   

                


            


def char_match_amount(a: str, b: str) -> int|bool:
    chars_that_match: int = 0
    for index in range(max(len(a), len(b))):
        if a[index] == b[index]:
            chars_that_match += 1
        else:
            return char_match_amount
    return True
