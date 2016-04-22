import metapy

class JSONTreeVisitor(metapy.parser.Visitor):

    def visit_leaf(self, leaf_node):
        return {'tag': leaf_node.category(), 'word': leaf_node.word()}

    def visit_internal(self, node):
        result = {'tag': node.category(), 'children': []}
        node.each_child(lambda n: result['children'].append(n.accept(self)))
        return result
