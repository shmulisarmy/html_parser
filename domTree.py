"""global constants:
        INDENT: used place in indents in the generated code
        text_tree, text_reverse_tree: used for searching for elements by text dinamicly"""



from html_ import HTML
from utils import char_match_amount
# from collections import defaultdict
from custom_packages.searchTree import SearchTree
import re
from string import ascii_uppercase

from colors import blue, green, yellow
from utils import infinite_number_generator

ascii_uppercase = (letter for letter in ascii_uppercase)


INDENT = "  "
text_tree = SearchTree()
text_reverse_tree = SearchTree()



class DomTree:
    """params:
            cached_children: usefull for an element that will get many queries (may it be querySelectorAll or one of the text match finders) where order doesnt matter"""
    def __init__(self, tagname, parentNode = None, textContent = None):
        self.tagname = tagname
        self.childrenNodes = []
        self.parentNode = parentNode
        self.textContent = textContent
        self.classList = []
        self.id = None
        self.atributes = {}
        self.parrentsWithUpdatingCache: list = []
        self.cached_children: list = []

    def appendChild(self, newChild: 'DomTree'):
        self.childrenNodes.append(newChild)
        for parrent in self.parrentsWithUpdatingCache:
            parrent: DomTree
            parrent.cached_children.append(newChild)

    def place_child_in_cache(self, newChild: 'DomTree'):
        self.cached_children.append(newChild)
        newChild.parrentsWithUpdatingCache.append(self)
        

    def traverse(self, level=0):
        result = []
        indent_spaces = "    "*level
        result.append(f"{indent_spaces}{self.tagname = } {self.atributes = } at level {level}")
        for element in self.childrenNodes:
            element: DomTree
            result.extend(element.traverse(level=level+1))

        return result
    
    def __repr__(self):
        return f"{blue(self.tagname)} {self.id = } class={self.classList} {' '.join(yellow(f'{attr}={self.atributes[attr]}') for attr in self.atributes.keys())} {f'text = {green(self.textContent)}' if self.textContent else ''}"
            

    @classmethod
    def create_document_from(cls, html_node_list: list['DomTree']):
        begin_index: int = 0
        ending_index: int = len(html_node_list)-1

        document = DomTree("document")
        at: DomTree = document

        while begin_index < ending_index:
            html_node: DomTree = html_node_list[begin_index]
            Type, content = HTML.str_type(html_node)
            if Type == "tag":
                previus_element = at
                find_tag_name_pattern = re.compile("\w+")
                tag_name: str = find_tag_name_pattern.match(content).group(0)
                at = DomTree(tag_name, previus_element)
                previus_element.appendChild(at)
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
                text_reverse_tree.insertWithValue(content[::-1].strip(), at)




            begin_index += 1

        return document

    def create_template(self, level = 0):
        letter_using: str = next(ascii_uppercase)
        ng = infinite_number_generator()
        tempalate_top = f"{letter_using}{next(ng)}"

        if level == 0:
            print(f"{yellow('function')} create_element(){'{'}")
        print(f"{INDENT}{blue('const')} {tempalate_top} = document.createElement('{self.tagname}')")

        for child_node in self.childrenNodes:
                child_node: DomTree

                if child_node.childrenNodes:
                    this_template_name: str = child_node.create_template(level+1)
                    print(f"{INDENT}{tempalate_top}.appendChild({this_template_name})")

                template_new_inner_element: str = green(f"{letter_using}{next(ng)}")
                print(f"{INDENT}{blue('const')} = document.createElement('{child_node.tagname}')")
                if child_node.id:
                    print(f"{INDENT}{template_new_inner_element}.id = '{child_node.id}'")
                for cls in child_node.classList:
                    print(f"{INDENT}{template_new_inner_element}.classList.add('{cls}')")
                for attr_name, attr_value in child_node.atributes.items():
                    print(f"{INDENT}{template_new_inner_element}.setatribute('{attr_name}', '{attr_value}')")

                print(f"{INDENT}{tempalate_top}.appendChild({template_new_inner_element})")

        return tempalate_top
           

    
    def querySelector(self, query: str):
        for node in self.breadth_first_search_child_generator():
            node: DomTree
            if node.tagname == query:
                return node
            
                
    def querySelectorAll(self, query: str):
        results = []
        for node in self.breadth_first_search_child_generator():
            node: DomTree
            if node.tagname == query:
                results.append(node)
            
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


    def find_best_text_match(node, search_text: str):
        """recursively check children for best match"""
        greatest_match: int = 0
        best_node_matchs = []
        for child_node in node.breadth_first_search_child_generator():
            child_node: DomTree
            if not child_node.textContent:
                continue
            comparing_against: str = child_node.textContent
            if len(comparing_against) < greatest_match:
                continue
            match_amount = char_match_amount(search_text, comparing_against)
            print(f"{greatest_match = } {match_amount = }")
            if match_amount > greatest_match:
                greatest_match = match_amount
                best_node_matchs = [child_node]
            elif match_amount == greatest_match:
                best_node_matchs.append(child_node)

        return best_node_matchs


    @classmethod
    def find_by_text(cls, search_text: str) -> list[list['DomTree']]:
        text_tree_results: list[DomTree] = text_tree.getValueListOfBestMatches(search_text)
        text_reverse_tree_results: list[DomTree] = text_reverse_tree.getValueListOfBestMatches(search_text[::-1])

        print(f"{[node.textContent for node in text_tree_results] = }")
        print(f"{[node.textContent for node in text_reverse_tree_results] = }")

        resulting_node_combos = []

        for index_, text_tree_results_current_node in enumerate(text_tree_results):
            for textContent, text_reverse_tree_results_current_node in enumerate(text_reverse_tree_results):
                if len(text_tree_results_current_node.textContent) + len(text_reverse_tree_results_current_node.textContent) > len(search_text):
                    continue
                middle_text = search_text[len(text_tree_results_current_node.textContent):-len(text_reverse_tree_results_current_node.textContent)] 
                if not middle_text:
                    resulting_node_combos.append([text_tree_results_current_node, text_reverse_tree_results_current_node])
                elif text_tree.isWord(middle_text):
                    resulting_node_combos.append([text_tree_results_current_node, text_tree.getValue(middle_text), text_reverse_tree_results_current_node])
                else:
                    middle_results = DomTree.find_by_text(middle_text)
                    for result in middle_results:
                        r = [text_tree_results_current_node, text_reverse_tree_results_current_node]
                        r.extend(result)
                        resulting_node_combos.append(r)


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

    def breadth_first_search_child_generator(self):
        """works like an enumerater"""
        for child_node in self.childrenNodes:
            yield child_node

        
        for child_node in self.childrenNodes:
            child_node: DomTree
            for childs_child in child_node.breadth_first_search_child_generator():
                yield childs_child

    def depth_first_search_child_generator(self):
        """works like an enumerater"""
        for child_node in self.childrenNodes:
            child_node: DomTree
            yield child_node        
            for childs_child in child_node.depth_first_search_child_generator():
                yield childs_child
    
    
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
        print(f"{others = }")
        assert all(isinstance(other, DomTree) for other in others)
        atributes = list(filter(lambda item: all(item[0] in other.atributes for other in others) and all(item[1] == other.atributes[item[0]] for other in others), self.atributes.items()))
        classList = list(filter(lambda class_name: all(class_name in other.classList  for other in others), self.classList))
        if all(self.tagname == other.tagname for other in others):
            tag_name = self.tagname
        else:
            tag_name = None


        closest_sharing_parrent: 'DomTree' = self.get_closest_sharing_parrent(self, *others)
        query = closest_sharing_parrent.create_query() + f".search_for_elements({tag_name = }, {classList = }, None, {atributes = })"

        return query   
    
    def next_sibling(self):
        parrent: DomTree = self.parentNode
        if not parrent:
            return None
        index_in_parrent = parrent.childrenNodes.index(self)
        if len(parrent.childrenNodes) <= index_in_parrent +1:
            return None
        return parrent.childrenNodes[index_in_parrent+1]
    
    def previous_sibling(self):
        parrent: DomTree = self.parentNode
        if not parrent:
            return None
        index_in_parrent = parrent.childrenNodes.index(self)
        if index_in_parrent-1 > 0:
            return None
        return parrent.childrenNodes[index_in_parrent-11]

    def get_same_age_cousins_iterator(self):
        this_nodes_parrent: DomTree = self.parentNode
        index = index(this_nodes_parrent.childrenNodes, self)
        grand_parrent: DomTree = this_nodes_parrent.parentNode

        for child in grand_parrent:
            child: DomTree
            family_of_grand_children = child.childrenNodes
            if child == this_nodes_parrent:
                continue
            if len(family_of_grand_children) > index:
                yield family_of_grand_children[index] 

    def get_same_age_cousins(self):
        this_nodes_parrent: DomTree = self.parentNode
        index = index(this_nodes_parrent.childrenNodes, self)
        grand_parrent: DomTree = this_nodes_parrent.parentNode
        list_of_cousins = []

        for child in grand_parrent:
            child: DomTree
            family_of_grand_children = child.childrenNodes
            if child == this_nodes_parrent:
                continue
            if len(family_of_grand_children) > index:
                list_of_cousins.append(family_of_grand_children[index])

        return list_of_cousins