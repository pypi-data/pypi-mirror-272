这是一个基于tree-sitter编译工具进行静态程序分析的demo, 并使用可视化工具graphviz，能够生成抽象语法树AST、函数调用图CG。
tree-sitter网址：https://tree-sitter.github.io/tree-sitter/

## 环境配置
确保已经安装了graphviz，在windows上，官网https://www.graphviz.org/ 下载graphviz之后，配置环境变量为安装路径下的bin文件夹，例如D:\graphviz\bin\，注意末尾的'\\'不能省略，如果是linux上，运行下面命令安装：
```
sudo apt-get install graphviz graphviz-doc
```
接着运行
```
pip install -r requirements.txt
```

## 生成AST树
AST.py能够生成AST树以及tokens，首先构造类，参数为代码语言，目前tree-sitter能够编译的语言都能够生成。
```
ast = AST('c')
```
接着运行下面代码可以显示AST树
```
ast.see_tree(code, view=True)
```
![AST](https://github.com/rebibabo/TSA/assets/80667434/6d1aae84-3c46-4978-844e-6006e8623718)

运行完成之后，会在当前目录下生成ast_tree.pdf，为可视化的ast树，可以通过设置参数view=False在生成pdf文件的同时不查看文件，pdf=False不生成可视化的pdf文件，设置参数filename="filename"来更改输出文件的名称。
获得代码的tokens可以运行下面的代码，返回值为token的列表。
```
ast.tokenize(code)
#['int', 'main', '(', ')', '{', 'int', 'abc', '=', '1', ';', 'int', 'b', '=', '2', ';', 'int', 'c', '=', 'a', '+', 'b', ';', 'while', '(', 'i', '<', '10', ')', '{', 'i', '++', ';', '}', '}']
```



## 生成CG
File.py继承自AST.py，能够生成函数调用图，运行下面代码能够生成单个项目的CG图
```
file = File("path to project")
file.see_cg(code, view=True)
```
生成项目目录所有文件的CG图：
```
dir = Dir('path to project')
```
生成CG图样例：
![捕获](https://github.com/rebibabo/static_program_analysis_by_tree_sitter/assets/80667434/b7dd8037-984e-4bea-920d-d3bdd1b4f8fe)



