"""global constants:
        INDENT: used place in indents in the generated code
        text_tree, text_reverse_tree: used for searching for elements by text dynamically"""



from html_ import HTML
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
    """
    all_nodes_in_order: list
    def __init__(self, tagname, parentNode = None, textContent = None):
        self.tagname = tagname
        self.childrenNodes = []
        self.parentNode = parentNode
        self.textContent = textContent
        self.classList = []
        self.id = None
        self.attributes = {}
        self.parentsWithUpdatingCache: list = []
        self.cached_children: list = []

    def appendChild(self, newChild: 'DomTree'):
        self.childrenNodes.append(newChild)
        for parent in self.parentsWithUpdatingCache:
            parent: DomTree
            parent.cached_children.append(newChild)

    def traverse(self, level=0):
        result = []
        indent_spaces = "    "*level
        result.append(f"{indent_spaces}{self.tagname = } {self.attributes = } at level {level}")
        for element in self.childrenNodes:
            element: DomTree
            result.extend(element.traverse(level=level+1))

        return result

    def __repr__(self):
        return f"{blue(self.tagname)} {self.id = } class={self.classList} {' '.join(yellow(f'{attr}={self.attributes[attr]}') for attr in self.attributes.keys())} {f'text = {green(self.textContent)}' if self.textContent else ''}"


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
                attributes = HTML.parse_attributes(pattern)
                if 'id' in attributes:
                    at.id = attributes['id']
                    del attributes['id']
                if 'class' in attributes:
                    at.classList = attributes['class'].split(" ")
                    del attributes['class']
                at.attributes = attributes
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
        template_top = f"{letter_using}{next(ng)}"

        if level == 0:
            print(f"{yellow('function')} create_element(){'{'}")
        print(f"{INDENT}{blue('const')} {template_top} = document.createElement('{self.tagname}')")

        for child_node in self.childrenNodes:
                child_node: DomTree

                if child_node.childrenNodes:
                    this_template_name: str = child_node.create_template(level+1)
                    print(f"{INDENT}{template_top}.appendChild({this_template_name})")

                template_new_inner_element: str = green(f"{letter_using}{next(ng)}")
                print(f"{INDENT}{blue('const')} = document.createElement('{child_node.tagname}')")
                if child_node.id:
                    print(f"{INDENT}{template_new_inner_element}.id = '{child_node.id}'")
                for cls in child_node.classList:
                    print(f"{INDENT}{template_new_inner_element}.classList.add('{cls}')")
                for attr_name, attr_value in child_node.attributes.items():
                    print(f"{INDENT}{template_new_inner_element}.setatribute('{attr_name}', '{attr_value}')")

                print(f"{INDENT}{template_top}.appendChild({template_new_inner_element})")

        return template_top



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

        parent: DomTree = node.parentNode
        all_similar_siblings = parent.querySelectorAll(query)
        if len(all_similar_siblings) == 1:
            return f"{parent.create_query()}.querySelector({query})"

        for index, element in enumerate(all_similar_siblings):
            if id(element) == id(node):
                return f"{parent.create_query()}.querySelectorAll({query})[{index}]"


    # def find_best_text_match(node, search_text: str):
    #     """recursively check children for best match"""
    #     greatest_match: int = 0
    #     best_node_matches = []
    #     for child_node in node.breadth_first_search_child_generator():
    #         child_node: DomTree
    #         if not child_node.textContent:
    #             continue
    #         comparing_against: str = child_node.textContent
    #         if len(comparing_against) < greatest_match:
    #             continue

    #             greatest_match = match_amount
    #             best_node_matches = [child_node]
    #         elif match_amount == greatest_match:
    #             best_node_matches.append(child_node)

    #     return best_node_matches


    @classmethod
    def find_by_text(cls, search_text: str) -> list[list['DomTree']]:
        text_tree_results: list[DomTree] = text_tree.getValueListOfBestMatches(search_text)
        text_reverse_tree_results: list[DomTree] = text_reverse_tree.getValueListOfBestMatches(search_text[::-1])

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


    @classmethod
    def find_by_text_in_order(cls, search_text: str, index_up_to = 0) -> list[list['DomTree']]:
        #!under construction
        resulting_node_combos = []

        text_tree_results: list[DomTree] = text_tree.getValueListOfBestMatches(search_text)

        for node in text_tree_results:
            node_document_index = DomTree.all_nodes_in_order.index(node)
            if node_document_index <= index_up_to:
                continue
            if node.textContent == search_text:
                resulting_node_combos.append()
            resulting_node_combos.extend(DomTree.find_by_text_in_order())

        return resulting_node_combos

    def recursive_parents(self) -> list[tuple]:
        results = []
        node = self
        index = 0
        while node.parentNode:
            node = node.parentNode
            results.append((index, node))
            index+=1
        return results

    def recursive_parents_enumerator(self):
        """works like an enumerator"""
        node = self
        index = 0
        while node.parentNode:
            node = node.parentNode
            yield (index, node)
            index+=1

    def breadth_first_search_child_generator(self):
        """works like an enumerator"""
        for child_node in self.childrenNodes:
            yield child_node


        for child_node in self.childrenNodes:
            child_node: DomTree
            for childs_child in child_node.breadth_first_search_child_generator():
                yield childs_child

    def depth_first_search_child_generator(self):
        """works like an enumerator"""
        for child_node in self.childrenNodes:
            child_node: DomTree
            yield child_node
            for childs_child in child_node.depth_first_search_child_generator():
                yield childs_child


    def get_closest_sharing_parent(*nodes: list['DomTree']) -> 'DomTree':
        """n*2 time and space complexity"""

        all_parents = {}
        for element in nodes:
            assert isinstance(element, DomTree) #because it is plausable to make a mistake and have it be None via an invalid selector...
            element: DomTree
            for index, parent in element.recursive_parents_enumerator():
                parent: DomTree
                if parent not in all_parents:
                    all_parents[parent] = [0, 0]
                all_parents[parent][0] += 1
                all_parents[parent][1] += index

        total_element_count = len(nodes)


        # part of higher order function
        def is_parent_of_all_elements(parent_as_a_key):
            value = all_parents[parent_as_a_key]
            number_of_children_here = value[0]

            return number_of_children_here == total_element_count


        sharing_parents: iter = list(filter(is_parent_of_all_elements, all_parents.keys()))

        closest_parent_distance = float('inf')
        closest_parent = None
        for parent in sharing_parents:
            distance: int = all_parents[parent][1]
            if distance < closest_parent_distance:
                closest_parent = parent
                closest_parent_distance = distance

        return closest_parent




    def search_for_element(self, tag_name=None, class_name=None, id=None, attributes = {}) -> 'DomTree':
        for node in self.childrenNodes:
            node: DomTree
            if node.tagname != tag_name:
                continue
            if (class_name and class_name not in node.classList):
                continue
            if (id and node.id != id):
                continue
            if any(node.attributes.get(atr) != attributes[atr] for atr in attributes):
                continue
            return node

        for node in self.childrenNodes:
            node: DomTree
            result_in_child = node.search_for_element(tag_name=tag_name, class_name=class_name, id=id, attributes=attributes)
            if result_in_child:
                return result_in_child

    def search_for_elements(self, tag_name=None, class_name=None, id=None, attributes={}) -> list['DomTree']:
        results = []
        for node in self.childrenNodes:
            node: DomTree
            if tag_name and node.tagname != tag_name:
                continue
            if class_name and class_name not in node.classList:
                continue
            if id and node.id != id:
                continue
            if any(node.attributes.get(atr) != attributes[atr] for atr in attributes):
                continue
            results.append(node)

        for node in self.childrenNodes:
            node: DomTree
            results.extend(node.search_for_elements(tag_name=tag_name, class_name=class_name, id=id, attributes=attributes))

        return results

    def best_common_selector(self, *others: list['DomTree']) -> str:
        assert all(isinstance(other, DomTree) for other in others)
        attributes = list(filter(lambda item: all(item[0] in other.attributes for other in others) and all(item[1] == other.attributes[item[0]] for other in others), self.attributes.items()))
        classList = list(filter(lambda class_name: all(class_name in other.classList  for other in others), self.classList))
        if all(self.tagname == other.tagname for other in others):
            tag_name = self.tagname
        else:
            tag_name = None


        closest_sharing_parent: 'DomTree' = self.get_closest_sharing_parent(self, *others)
        query = closest_sharing_parent.create_query() + f".search_for_elements({tag_name = }, {classList = }, None, {attributes = })"

        return query

    def next_sibling(self):
        parent: DomTree = self.parentNode
        if not parent:
            return None
        index_in_parent = parent.childrenNodes.index(self)
        if len(parent.childrenNodes) <= index_in_parent +1:
            return None
        return parent.childrenNodes[index_in_parent+1]

    def previous_sibling(self):
        parent: DomTree = self.parentNode
        if not parent:
            return None
        index_in_parent = parent.childrenNodes.index(self)
        if index_in_parent-1 > 0:
            return None
        return parent.childrenNodes[index_in_parent-11]

    def get_same_age_cousins_iterator(self):
        this_nodes_parent: DomTree = self.parentNode
        index = index(this_nodes_parent.childrenNodes, self)
        grand_parent: DomTree = this_nodes_parent.parentNode

        for child in grand_parent:
            child: DomTree
            family_of_grand_children = child.childrenNodes
            if child == this_nodes_parent:
                continue
            if len(family_of_grand_children) > index:
                yield family_of_grand_children[index]

    def get_same_age_cousins(self):
        this_nodes_parent: DomTree = self.parentNode
        index = index(this_nodes_parent.childrenNodes, self)
        grand_parent: DomTree = this_nodes_parent.parentNode
        list_of_cousins = []

        for child in grand_parent:
            child: DomTree
            family_of_grand_children = child.childrenNodes
            if child == this_nodes_parent:
                continue
            if len(family_of_grand_children) > index:
                list_of_cousins.append(family_of_grand_children[index])

        return list_of_cousins
