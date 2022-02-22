op_rules = {
    '+': (int,int),
    '-': (int,int),
    '*': (int,int),
    '/': (int,int),
    '+.': (float,float),
    '-.': (float,float),
    '*.': (float,float),
    '/.': (float,float),
    '>': (int,bool),
    '=': (int,bool),
    '>.': (float,bool),
    '=.': (float,bool),
    '=b': (bool,bool),
    '>b': (bool,bool),
    '!': (bool,bool),
    '&&': (bool,bool),
    '||': (bool,bool),
    'i2f': (int,float),
    'floor': (float,int),
}

a = dict()

class Scope:
    def __init__(self):
        self.outer:Scope = None
        self.env:dict[str,type] = {}
    
    def assign_type(self,n,t):
        current = self
        while current:
            if n in current.env:
                current.env[n] = t
                return True
            current = current.outer
        return False

    def get(self,n:str,r=None):
        current = self
        while current:
            if n in current.env:
                return current.env[n]
            current = current.outer
            
        if r!=None:
            return r
        raise Exception("Not found ",n)
        
    
class StaticCheck(Visitor):

    def visitProgram(self,ctx:Program,o):
        scope = Scope()
        for dec in ctx.decl:
            self.visit(dec,scope)
        for stmt in ctx.stmts:    
            self.visit(stmt,scope)
        
    def visitVarDecl(self,ctx:VarDecl,o):
        is_inner = True
        if ctx.name in o.env:
            raise Redeclared(ctx)
        o.env[ctx.name] = None
        
    def visitAssign(self,ctx:Assign,o):
        r = self.visit(ctx.rhs, o) # visit RHS first
        l = self.visit(ctx.lhs, o)

        if r is None:
            if type(ctx.rhs)==Id:
                if l is not None:
                    o.assign_type(ctx.rhs.name,l)
                    return
                raise TypeCannotBeInferred(ctx)
            raise TypeMismatchInStatement(ctx)
            
        if l is None:
            o.assign_type(ctx.lhs.name,r)
            return
        
        if l != r:
            raise TypeMismatchInStatement(ctx)
            
    def visitBlock(self,ctx:Block,o):
        scope = Scope()
        scope.outer = o
            
        for dec in ctx.decl:
            self.visit(dec,scope)
        for stmt in ctx.stmts:    
            self.visit(stmt,scope)
    
    def visitBinOp(self,ctx:BinOp,o):
        leftType = ctx.e1.accept(self, o)
        rightType = ctx.e2.accept(self, o)
        if ctx.op in op_rules:
            _accept, _return = op_rules[ctx.op]
            if leftType is None:
                leftType = _accept
                o.assign_type(ctx.e1.name,_accept)
            if rightType is None:
                rightType = _accept
                o.assign_type(ctx.e2.name,_accept)
            if leftType is _accept and rightType is _accept:
                return _return
        
        raise TypeMismatchInExpression(ctx)
                
    def visitUnOp(self,ctx:UnOp,o):
        ele = ctx.e.accept(self,o)
        if ctx.op in op_rules:
            _accept, _return = op_rules[ctx.op]

            if ele is None:
                o.assign(ctx.e.name,_accept)
                return _return
                
            if ele is _accept:
                return _return
            
        raise TypeMismatchInExpression(ctx)

    def visitIntLit(self,ctx:IntLit,o):
        return int

    def visitFloatLit(self,ctx,o):
        return float

    def visitBoolLit(self,ctx,o):
        return bool

    def visitId(self,ctx,o):
        t = o.get(ctx.name,"nil")
        if t != "nil":
            return t
        raise UndeclaredIdentifier(ctx.name)