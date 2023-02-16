import ast
import json
import sys
import re
import random 
import string

vardict = {}
   
def node_to_string(node): 

    if isinstance(node, ast.Module):
        return body_to_string(node.body)

    elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
        
        vararg = False
        kwargs = False
        args = node.args.args + node.args.kwonlyargs
        if node.args.vararg != None:
            vararg = True
        if node.args.kwarg != None:
            kwargs = True
        
        if isinstance(node, ast.FunctionDef):
            ret = 'define the function ' + identifier_to_string(node.name) + ', that takes {} arguments'.format(len(node.args.args))
        else:
            ret = 'define the asynchronous function ' + identifier_to_string(node.name) + ', that takes {} arguments'.format(len(node.args.args))

        if len(args) != 0:
            ret += ': '
            for i,a in enumerate(args):
                if i == 0:
                    ret += node_to_string(a)

                elif i == len(node.args.args)-1:
                    ret += ' and ' + node_to_string(a) 

                else:
                    ret += ', ' + node_to_string(a)
            if vararg:
                if kwargs:
                    ret += '. It also takes keyword and non-keyword arguments' 
                else:
                    ret += '. It also takes keyword arguments'
            elif kwargs:
                ret += '. It also takes non-keyword arguments'
     
        ret += '.\nThen, ' + body_to_string(node.body)
   
        return ret

    elif isinstance(node, ast.arg):
        if node.arg == 'self':
            return 'the instance of the class'
        else:
            return 'the variable \'' + identifier_to_string(node.arg) + '\''
    
    elif isinstance(node, ast.Name):
        return '\'' + identifier_to_string(node.id) + '\''
        
    elif isinstance(node, ast.Constant):
        if type(node.value) == 'str':
            if len(node.value) < 50 and '\n' not in node.value and '\r' not in node.value:
                return node.value 
            else:
                return 'a long string'
        else:
            return str(node.value) 

    elif isinstance (node, ast.Expr):
        
        if isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                #remove comments
                return ''
                #return 'INISTRING \'' + node.value.value + '\' FSTRING' 
            else: 
                return str(node.value.value)
        else:
            return node_to_string(node.value)
    
    elif isinstance(node, ast.IfExp):
        return node_to_string(node.body) + ' if ' + node_to_string(node.test) + ' else ' + node_to_string(node.orelse)

    elif isinstance(node, ast.If):
        ret = 'if ' + node_to_string(node.test) + ', then ' + body_to_string(node.body)
        if len(node.orelse) != 0:
            ret += 'else, ' + body_to_string(node.orelse)
   
        return ret

    elif isinstance(node, ast.Compare):
        
        ret = node_to_string(node.left)

        if len(node.ops) > 1:
            
            for i,op in enumerate(node.ops):
                if i == 0:
                    ret += ' ' + node_to_string(op) + ' ' + node_to_string(node.comparators[i])
                else:
                    ret += ' and ' + node_to_string(node.comparators[i-1]) + ' ' + node_to_string(op) + ' ' + node_to_string(node.comparators[i]) 
        
        elif len(node.ops) == 1:
            ret += ' ' + node_to_string(node.ops[0]) + ' ' + node_to_string(node.comparators[0])
            
        return ret    

    elif isinstance(node, ast.Eq):
        return 'is equal to'

    elif isinstance(node, ast.NotEq):
        return 'is not equal to'

    elif isinstance(node, ast.Lt):
        return 'is less than'

    elif isinstance(node, ast.LtE):
        return 'is less than or equal to'

    elif isinstance(node, ast.Gt):
        return 'is greater than'

    elif isinstance(node, ast.GtE):
        return 'is greater than or equal to'

    elif isinstance(node, ast.Is):
        return 'is'

    elif isinstance(node, ast.IsNot):
        return 'is not'

    elif isinstance(node, ast.In):
        return 'is in'

    elif isinstance(node, ast.NotIn):
        return 'is not in'

    elif isinstance(node, ast.Assign):

        ret = 'assign to '
        for i,t in enumerate(node.targets):
            if i == 0:
                ret += node_to_string(t)
            elif i == len(node.targets)-1:
                ret += ' and ' + node_to_string(t)
            else:
                ret += ', ' + node_to_string(t)
        
        if isinstance(node.value, ast.Call):
            return ret + ' the result of \`' + node_to_string(node.value) + '\`'
        else:
            return ret + ' the value of ' + node_to_string(node.value)      
    
    elif isinstance(node, ast.AnnAssign):

        ret = 'assign to '
        for i,t in enumerate(node.targets):
            if i == 0:
                ret += node_to_string(t)
            elif i == len(node.targets)-1:
                ret += ' and ' + node_to_string(t)
            else:
                ret += ', ' + node_to_string(t)
        if isinstance(node.value, ast.Call):
            ret += ' the result of \`' + node_to_string(node.value) + '\`'
        else:
            ret += ' the value of ' + node_to_string(node.value)

        return ret + ', and annote it to be of type ' + node_to_string(node.annotation)   


    elif isinstance(node, ast.NamedExpr):
        return 'assign to ' + node_to_string(node.target) + ' the value of ' + node_to_string(node.value)

    elif isinstance(node, ast.Call):
        ret = 'a call to the function ' + node_to_string(node.func)
            
        if len(node.args) != 0 or len(node.keywords) != 0:    
            ret += ', called with arguments ' + args_to_string(node.args, node.keywords)
        
        return ret

    elif isinstance(node, ast.Starred):
        return 'the starred variable ' + node_to_string(node.value)

    elif isinstance(node, ast.Attribute):
        return 'the attribute ' + identifier_to_string(node.attr) + ' of the object ' + node_to_string(node.value)
    
    elif isinstance(node, ast.With) or isinstance(node, ast.AsyncWith):
        ret = 'with '
        for i, item in enumerate(node.items):
            if i == 0:
                ret += node_to_string(item)
            elif i == len(node.items)-1:
                ret += ' and ' + node_to_string(item)
            else:
                ret += ', ' + node_to_string(item)
                
        ret += ', then ' + body_to_string(node.body)
        return ret

    elif isinstance(node, ast.withitem):
        return node_to_string(node.context_expr) + ' as ' + node_to_string(node.optional_vars)
    
    elif isinstance(node, ast.For) or isinstance(node, ast.AsyncFor):
        ret = 'do the following: ' + body_to_string(node.body)
        ret += ', and repeat for each ' + node_to_string(node.target) + ' in ' + node_to_string(node.iter)
        if len(node.orelse) > 0:
            ret += ', else ' + body_to_string(node.orelse)
        return ret 
    
    elif isinstance(node, ast.While):
        ret = 'do the following: ' + body_to_string(node.body)
        ret += ', and repeat while ' + node_to_string(node.test)
        if len(node.orelse) > 0:
            ret += ', else ' + body_to_string(node.orelse)
        return ret    

    elif isinstance(node, ast.Break):
        return 'terminate the loop'

    elif isinstance(node, ast.Continue):
        return 'continue the loop'

    elif isinstance(node, ast.Tuple):
        ret = ''
        for i,v in enumerate(node.elts):
            if i == 0:
                ret += node_to_string(v)
            else:
                ret += ', ' + node_to_string(v)
        return ret        

    elif isinstance(node, ast.List):
        ret = 'a list composed by '
        for i,v in enumerate(node.elts):
            if i == 0:
                ret += node_to_string(v)
            elif i == len(node.elts)-1:
                ret += ' and ' + node_to_string(v)
            else:
                ret += ', ' + node_to_string(v)

        return ret
    
    elif isinstance(node, ast.Set):
        ret = 'a set composed by '
        for i,v in enumerate(node.elts):
            if i == 0:
                ret += node_to_string(v)
            elif i == len(node.elts)-1:
                ret += ' and ' + node_to_string(v)
            else:
                ret += ', ' + node_to_string(v)

        return ret

    elif isinstance(node, ast.Dict):
        
        if len(node.keys)==0:
            ret = 'an empty dictionary'
        else:
            ret = 'a dictionary having '
            for i,k in enumerate(node.keys):
                if i == 0:
                    ret += node_to_string(k)
                elif i == len(node.keys)-1:
                    ret += ' and ' + node_to_string(k)
                else:
                    ret += ', ' + node_to_string(k)
            ret += ' as keys, with values '
            for i,k in enumerate(node.values):
                if i == 0:
                    ret += node_to_string(k)
                elif i == len(node.values)-1:
                    ret += ' and ' + node_to_string(k)
                else:
                    ret += ', ' + node_to_string(k)
            ret += ', respectively'

        return ret

    elif isinstance(node, ast.Del) or isinstance(node, ast.Delete):
        ret = 'delete the variables '
        for i,k in enumerate(node.targets):
            if i == 0:
                ret += node_to_string(k)
            elif i == len(node.targets)-1:
                ret += ' and ' + node_to_string(k)
            else:
                ret += ', ' + node_to_string(k)
        return ret
            
    elif isinstance(node, ast.FormattedValue):
        ret = node_to_string(node.value) + ' formatted as '
        if node.conversion == 115:
            ret += 'a string'
        elif node.conversion == 114:
            ret += 'a repr'
        elif node.conversion == 97:
            ret += 'ascii'
        else:
            'nothing'

        return ret

    elif isinstance(node, ast.JoinedStr):
        return 'a formatted string'
    
    elif isinstance(node, ast.UnaryOp):
        return node_to_string(node.op) + ' ' + node_to_string(node.operand)

    elif isinstance(node, ast.UAdd):
        return 'plus'

    elif isinstance(node, ast.USub):
        return 'minus'

    elif isinstance(node, ast.Not):
        return 'not'

    elif isinstance(node, ast.Invert):
        return 'the inverse of'

    elif isinstance(node, ast.BinOp):
        return 'the ' + node_to_string(node.op) + ' between ' + node_to_string(node.left) + ' and ' + node_to_string(node.right)

    elif isinstance(node, ast.Add):
        return 'sum'

    elif isinstance(node, ast.Sub):
        return 'subtraction'

    elif isinstance(node, ast.Mult):
        return 'multiplication'

    elif isinstance(node, ast.Div):
        return 'division'

    elif isinstance(node, ast.FloorDiv):
        return 'floor division'

    elif isinstance(node, ast.Mod):
        return 'module'

    elif isinstance(node, ast.Pow):
        return 'power'

    elif isinstance(node, ast.LShift):
        return 'left shift'

    elif isinstance(node, ast.RShift):
        return 'right shift'

    elif isinstance(node, ast.BitOr):
        return 'bitwise or'

    elif isinstance(node, ast.BitXor):
        return 'bitwise xor'

    elif isinstance(node, ast.And):
        return 'bitwise and'

    elif isinstance(node, ast.MatMult):
        return 'matrix multiplication'

    elif isinstance(node, ast.BoolOp):
        ret = node_to_string(node.values[0])
        for i in range(1,len(node.values)):
            ret += ' ' + node_to_string(node.op) + ' ' + node_to_string(node.values[i])

        return ret    

    elif isinstance(node, ast.And):
        return 'and'

    elif isinstance(node, ast.Or):
        return 'or'
    
    elif isinstance(node, ast.Subscript):
        return 'the sequence ' + node_to_string(node.value) + ' in positions ' + node_to_string(node.slice)
    
    elif isinstance(node, ast.Slice):
        return 'from ' + node_to_string(node.lower) + ' to ' + node_to_string(node.upper)

    elif isinstance(node, ast.ListComp) or isinstance(node, ast.SetComp) or isinstance(node, ast.GeneratorExp):
        return 'the sequence ' + node_to_string(node.elt) + ' ' + generators_to_string(node.generators)
    
    elif isinstance(node, ast.DictComp):
        
        ret = 'a dictionary having as keys all the ' + node_to_string(node.key) + ' ' + generators_to_string(node.generators)
        ret += ', each corresponding to the value ' + node_to_string(node.value)

        return ret

    elif isinstance(node, ast.comprehension):
        ret = 'for ' + node_to_string(node.target) + ' in ' + node_to_string(node.iter) 
        if len(node.ifs) > 0:
            for i,t in enumerate(node.ifs):
                if i == len(node.ifs)-1:
                    ret += node_to_string(t)
                else:
                    ret *= node_to_string(t) + ' '

        return ret            

    elif isinstance(node, ast.AugAssign):
        ret = 'assign to ' + node_to_string(node.target) + ' the value of ' 
        ret += node_to_string(node.target) + ' ' + node_to_string(node.op) + ' ' + node_to_string(node.value)
        return ret

    elif isinstance(node, ast.Raise):
        return 'raise the exception ' + node_to_string(node.exc) + ' from ' + node_to_string(node.cause)

    elif isinstance(node, ast.Assert):
        return 'assert that ' + node_to_string(node.test)  
    
    elif isinstance(node, ast.Pass):
        return 'do nothing'

    elif isinstance(node, ast.Import):
        ret = 'import '
        for i,a in enumerate(node.names):
            if i == 0:
                ret += node_to_string(a)
            elif i == len(node.targets)-1:
                ret += ' and ' + node_to_string(a)
            else:
                ret += ', ' + node_to_string(a)

        return ret        

    elif isinstance(node, ast.ImportFrom):            
        ret = 'from ' + node.module + ' import '
        for i,a in enumerate(node.names):
            if i == 0:
                ret += node_to_string(a)
            elif i == len(node.targets)-1:
                ret += ' and ' + node_to_string(a)
            else:
                ret += ', ' + node_to_string(a)
        return ret  

    elif isinstance(node, ast.alias):
        ret = identifier_to_string(node.name)
        if node.asname != None:
            ret += ' ' + identifier_to_string(node.asname)

        return ret

    elif isinstance(node, ast.Lambda):
        return 'LAMBDAFUN'

    elif isinstance(node, ast.Yield):
        return 'yield ' + node_to_string(node.value)

    elif isinstance(node, ast.YieldFrom):
        return 'yield from ' + node_to_string(node.value)

    elif isinstance(node, ast.Try): #or isinstance(node, ast.TryStar):
        ret = 'try the following: ' + body_to_string(node.body)
        
        if len(node.handlers) > 1:
            ret += ', and if an error occurs handle the following exceptions: ' + body_to_string(node.handlers)
        else:
            ret += ', and if an error occurs handle the following exception: ' + node_to_string(node.handlers[0])
        
        if node.orelse != None:
            if len(node.orelse) > 0:
                ret += ', otherwise, if there are no errors, do: ' + body_to_string(node.orelse)
        
        if node.finalbody != None:
            if len(node.finalbody) > 0:    
                ret += ', anyhow do: ' + body_to_string(node.orelse)

        return ret        

    elif isinstance(node, ast.ExceptHandler):
        return node_to_string(node.type)

    elif isinstance(node, ast.Global):
        ret = 'define the variable'
        if len(node.names) > 1:
            ret += 's'

        for n in node.names:
            ret += ' ' + identifier_to_string(n)

        return ret + ' as global'

    elif isinstance(node, ast.Nonlocal):
        ret = 'define the variable'
        if len(node.names) > 1:
            ret += 's'

        for n in node.names:
            ret += ' ' + identifier_to_string(n)

        return ret + ' as non local'

    elif isinstance(node, ast.Await):
        return 'await that ' + body_to_string(node.body)

    elif isinstance(node, ast.Return):
        return 'return ' + node_to_string(node.value)

    elif isinstance(node, ast.keyword):
        return 'the keyword argument ' + node_to_string(node.value)
    else:
        #print('not implemented node: ',type(node))
        return 'NOTIMPNODE'

def generators_to_string(generators):
    ret = ''
    for i,g in enumerate(generators):
        if i != len(generators)-1:
            ret += node_to_string(g) + ' and '
    return ret        


def identifier_to_string(identifier):

    abbrv = {
        'abbr':'abbreviation',
        'abs':'absolute value',
        'ack':'acknowledgement',
        'addr':'address',
        'alloc':'allocate',
        'arg':'argument',
        'arr':'array',
        'attr':'attribute',
        'auth':'authentication',
        'avg':'average',
        'bin':'binary',
        'bool':'boolean',
        'buf':'buffer',
        'cfg':'configuration',
        'ch':'channel',
        'char':'character',
        'chr':'character',
        'clr':'clear',
        'cmd':'command',
        'cmp':'compare',
        'cnt':'counter',
        'concat':'concatenate',
        'config':'configuration',
        'col':'column',
        'cpy':'copy',
        'dec':'decimal',
        'dict':'dictionary',
        'diff':'difference',
        'dir':'directory',
        'disp':'display',
        'doc':'document',
        'env':'environment',
        'eq':'equal',
        'err':'error',
        'eval':'evaluate',
        'exe':'executable',
        'exec':'execute',
        'expr':'expression',
        'float':'floating point number',
        'fun':'function',
        'func':'function',
        'fig':'figure',
        'hex':'hexadecimal',
        'hdr':'header',
        'i':'iterator i',
        'id':'identifier',
        'idx':'index',
        'img':'image',
        'info':'information',
        'init':'initialize',
        'ins':'insert',
        'int':'integer',
        'j':'iterator j',
        'k':'iterator k',
        'lib':'library',
        'len':'length',
        'max':'maximum',
        'mem':'memory',
        'mid':'middle',
        'min':'minimum',
        'misc':'miscellaneous',
        'msg':'message',
        'num':'number',
        'obj':'object',
        'opt':'optional',
        'param':'parameter',
        'pos':'position',
        'pow':'power',
        'prev':'previous',
        'proc':'process',
        'prt':'print',
        'ptrp':'ointer',
        'rand':'random',
        'rem':'remove',
        'res':'result',
        'ret':'return',
        'rgx':'regular expression', 
        'regex':'regular expression',
        'seq':'sequence',
        'sqrts':'quare root',
        'src':'source',
        'stat':'statistics',
        'std':'standard',
        'stdin':'standard input',
        'stderr':'standard error',
        'stdout':'standard output',
        'str':'string',
        'temp':'temporary', 
        'tmp':'temporary',
        'txt':'text',
        'usr':'user',
        'util':'utility',
        'val':'value',
        'var':'variable',
        'vars':'variables',
        'vec':'vector'
        }

    #split snake case
    if '_' in identifier:
        snake = re.split('_+', identifier)
    else:
        snake = [identifier]
     
    #split camel case
    camel = []
    for s in snake:
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', s)
        camel += [m.group(0).lower() for m in matches]

    ret = ''
    for s in camel:
        if s in abbrv.keys():
            ret += abbrv[s] + ' '
        else:
            ret += s + ' '
    
    return ret[:-1]
"""
def identifier_to_string(identifier):
    
    if identifier not in vardict.keys():
        letters = string.ascii_lowercase
        vardict[identifier] = ''.join(random.choice(letters) for i in range(7))

    return vardict[identifier]
"""
def body_to_string(body):
    ret = ''
    for i,stmt in enumerate(body):
            if i == 0:
                ret += node_to_string(stmt)
            elif i == (l := len(body))-1 and l != 1:
                ret += '. Finally, ' + node_to_string(stmt) + '.\n'
            else:
                ret += '. ' + node_to_string(stmt)
    return ret

def args_to_string(args, keywords):
    ret = ''
    if len(args) != 0:
        
        for i,a in enumerate(args):
            if i == 0:
                ret += 'the variable ' + node_to_string(a)
            elif i == len(args)-1:
                ret += ' and the variable ' + node_to_string(a)
            else: 
                ret += ', ' + node_to_string(a)
        
        if len(keywords) != 0:
            ret += ', along with keyword arguments: '    
            for i,a in enumerate(keywords):
                if i == 0:
                    ret += 'the variable ' + node_to_string(a)
                elif i == len(args)-1:
                    ret += ' and the variable ' + node_to_string(a)
                else:
                    ret += ', ' + node_to_string(a)
    else:
        for i,a in enumerate(keywords):
            if i == 0:
                ret += 'the keyword arguments ' + node_to_string(a)
            elif i == len(args)-1:
                ret += ' and ' + node_to_string(a)
            else:
                ret += ', ' + node_to_string(a)
    return ret
     
if __name__ == '__main__':
    
    ds = sys.argv[1]
    #parse_json(ds)

    with open('{}_py_fun'.format(ds),'r') as f:
        pys = f.readlines()
    
    with open('{}_py_en'.format(ds)) as p:
        doc = p.readlines()
    
    print(len(doc), len(pys))

    assert len(doc) == len(pys)

    for i in range(len(pys)):
        try:
            pt = ast.parse(pys[i].encode('utf-8').decode('unicode-escape'))
            #print(ast.dump(pt, indent=4))
            pseudopy = node_to_string(pt)
            
            with open('pseudoRndStories/{}/'.format(ds) + str(i) + '.story', 'w') as s:
                s.write(pseudopy)
                s.write('\n@highlight\n\n')
                s.write(doc[i])

        except:
            print('failed while parsing function', i)
    
