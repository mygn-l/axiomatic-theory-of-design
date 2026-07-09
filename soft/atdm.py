"""
    Since the world is infinite but computers have finite storage, this program only works inside "human thought" as defined in ATDM.
"""

from __future__ import annotations
from collections.abc import Callable

class ATDM_Object:
    def __init__(self, name: str, *args: any):
        self.name = name

        self.elements = set()
        for x in args:
            self.elements.add(x)

        self.children = set()
        self.parent = None
    
    def equals(self, obj: ATDM_Object):
        return self.elements == obj.elements
    
    def unequal(self, obj: ATDM_Object):
        return not self.equals(obj)
    
    def get_union(self, name: str, *args: ATDM_Object):
        union = ATDM_Object(name)
        union.insert_child(self)
        for obj in args:
            union.insert_child(obj)
        return union
    
    def insert_child(self, obj: ATDM_Object):
        self.children.add(obj)
        obj.parent = self

    def remove_child(self, obj: ATDM_Object):
        if obj in self.children:
            obj.parent = None
            self.children.remove(obj)
    
    def get_level(self, level: int, current_level: int = 0):
        objects = set()
        if current_level == level:
            objects.add(self)
        else:
            for child in self.children:
                objects = objects.union(child.get_level(level, current_level + 1))
        return objects
    
    def get_children(self):
        return self.get_level(1)
    
    def is_primitive(self):
        return len(self.children) == 0
    
    def get_elements(self):
        elements = set()
        elements = elements.union(self.elements)
        for child in self.children:
            elements = elements.union(child.get_elements())
        return elements
    
    def structure(self):
        struct = ATDM_Object("structure of " + self.name)
        relation = Relation(self, self)
        struct.elements = self.elements.union(relation.elements)
        return struct

class Product(ATDM_Object):
    def __init__(self, name: str, properties: set[tuple[str, any]]):
        super().__init__(name, properties)
        self.elements = properties
    
    def get_union(self, name: str, *args: Product):
        prod_union = Product(name, set())
        prod_union.insert_child(self)
        for prod in args:
            prod_union.insert_child(prod)
        return prod_union

    def get_property(self, name: str):
        properties = super().get_elements()
        for property in properties:
            if property[0] == name:
                return property
    
    def get_own_properties(self):
        return self.elements
    
    def update_property(self, name: str, value: any):
        targeted_product = self.delete_property(name)
        targeted_product.elements.add((name, value))
    
    def delete_property(self, name: str):
        product = self.search_from_property(name)
        to_remove = None
        for property in product.elements:
            if property[0] == name:
                to_remove = property
                break
        if to_remove:
            product.elements.remove(to_remove)
        return product
    
    def search_from_name(self, name: str):
        if self.name == name:
            return self
        for child in self.children:
            result = child.search_from_name(name)
            if result:
                return result
    
    def search_from_property(self, name: str):
        for property in self.elements:
            if property[0] == name:
                return self
        for child in self.children:
            result = child.search_from_property(name)
            if result:
                return result
    
    def path(self):
        current = self
        nodes = []
        while current:
            nodes.append(current.name)
            current = current.parent
        return "/".join(reversed(nodes))

class Relation(ATDM_Object):
    def __init__(self, obj1: ATDM_Object, obj2: ATDM_Object):
        super().__init__("")
        for x in obj1.elements:
            for y in obj2.elements:
                self.elements.add((x, y))

class Nature_Prime(ATDM_Object):
    def __init__(self, *args: ATDM_Object):
        super().__init__("Nature")
        for obj in args:
            self.elements = self.elements.union(obj.get_elements())

class Environment(ATDM_Object):
    def __init__(self, product: Product, nature: Nature_Prime):
        super().__init__("Environment")
        self.elements = nature.get_elements().difference(product.get_elements())
        self.properties = self.elements

class Actions(Relation):
    def __init__(self, product: Product, environment: Environment):
        super().__init__(environment, product)

class Responses(Relation):
    def __init__(self, product: Product, environment: Environment):
        super().__init__(product, environment)

class Performances(Relation):
    def __init__(self, actions: Actions, responses: Responses):
        super().__init__(actions, responses)

class Specifications(ATDM_Object):
    def __init__(self, *args: tuple[str, Callable[[any], int]]):
        super().__init__()
        for named_func in args:
            self.elements.add(named_func)
        self.specifications = self.elements

    def evaluate(self, product: Product):
        for named_func in self.specifications:
            property_name = named_func[0]
            matching_property = product.get_property(property_name)
            if matching_property:
                is_satisfied = named_func[1](matching_property[1])
                if is_satisfied == 0:
                    return 0
                elif is_satisfied == -1:
                    return -1
            else:
                return 0
        return 1

# special type of specification where you check the range of a number
class Num_Range_Specification(Specifications):
    def __init__(self, name: str, minimum: float, maximum: float):
        super().__init__((name, lambda x : 1 if (x >= minimum and x <= maximum) else 0))

# special type of specification where you simply check for equality
class Equality_Specification(Specifications):
    def __init__(self, name: str, value: any):
        super().__init__((name, lambda x : 1 if (x == value) else 0))
