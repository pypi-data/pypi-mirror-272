from CGenr.AST import *

def get_identifiers(node):
    call_nodes = []
    if node.child_count == 0:
        return call_nodes
    for child in node.children:
        if child.type == 'identifier': # 找到函数调用节点
            call_nodes.append(child)
        else:
            call_nodes.extend(get_identifiers(child))
    return call_nodes

class Function:             #函数分析
    def __init__(self, node):
        self.type = text(node.child_by_field_name('type'))
        while node.type != 'function_declarator':       #找到函数声名
            node = node.child_by_field_name('declarator')
        self.name = text(node.child_by_field_name('declarator')) #函数名
        paramters = node.child_by_field_name('parameters')       #参数 
        self.signature = {'return': self.type, 'name': self.name, 'parameters': {}} 
        #函数签名(基本信息：自身返回值类型，名字，参数列表)
        self.id = node.start_point[0]   #函数的id，应该是用来标识函数的
        for param in paramters.children:        #获取参数列表
            if text(param) not in [',', '(', ')']:
                type = text(param.child_by_field_name('type'))
                name = text(param.child_by_field_name('declarator'))
                self.signature['parameters'][name] = type

    def __eq__(self, other):    #判断两个函数是否相等
        return self.signature == other.signature

    def __str__(self):          #返回函数签名
        return str(self.signature)

class CG(AST):
    def __init__(self, language):
        super().__init__(language)
        self.node_set = {}  # 存放每一个节点的信息
        self.cg = []  # 存放每一个函数的CFG图
        self.funcs = {}

    def create_cg(self, root_node):
        func_def_nodes = {}  
        for child in root_node.children:    # 先找到所有的函数定义节点
            if child.type == 'function_definition':     
                func_info = Function(child)     # 获取函数信息
                func_def_nodes[func_info.name] = child
                self.funcs[func_info.name] = func_info
        for node in func_def_nodes: # 再依次遍历每一个函数中调用的函数
            func_node = func_def_nodes[node]
            ids = get_identifiers(func_node)
            cg_call_nodes = set()
            for id in ids:
                id_name = text(id)
                if id_name in func_def_nodes:
                    cg_call_nodes.add(self.funcs[id_name].id)
            self.cg.append((Function(func_node), cg_call_nodes))
        return self.cg

    def see_cg(self, code_path, filename='CG', pdf=True, view=False):
        code = r'{}'.format(open(code_path, 'r', encoding='utf-8').read())
        tree = self.parser.parse(bytes(code, 'utf8'))
        root_node = tree.root_node
        CG = self.create_cg(root_node)
        dot = Digraph(comment=filename)
        for node in CG:
            dot.node(str(node[0].id), shape='rectangle', label=node[0].name, fontname='fangsong')
            for call_node in node[1]:
                if str(node[0].id) != str(call_node):
                    dot.edge(str(node[0].id), str(call_node))
        if pdf:
            dot.render(filename, view=view, cleanup=True)
            

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    
    cg = CG('cpp')
    cg.see_cg('练习6-3.cpp', view=True)
