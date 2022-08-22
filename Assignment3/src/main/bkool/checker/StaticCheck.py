
"""
 * @author nhphung
 * @extended by: ngthquocminh
"""
from types import FunctionType
from AST import * 
from Visitor import *
from typing import List, Tuple
from StaticError import *



class Utils:
    def lookup(self,name,lst,func):
        for x in lst:
            if name == func(x):
                return x
        return None


class MType:
    def __init__(self,partype:List[Type],rettype:Type):
        self.partype = partype
        self.rettype = rettype

class SymbolVar:
    def __init__(self,name:str,mtype:MType,kind:Kind,static=False,value=None):
        self.name = name
        self.mtype = mtype
        self.kind = kind
        self.value = value
        self.static = static
"""
class B {}
class A {
    int a = 1;
    int foo(int,string) { B b new B(); }
}
"""
class Scope:
    def __init__(self,ctx,scope):
        self.ctx:AST = ctx
        self.outer:Scope = scope # None for highest scope
        self.env:List[Symbol] = []
    
    def get_sympol(self,name:str,deep:bool=True,searcher = lambda s,n:s.name==n) -> Symbol:
        current = self
        while current:
            for s in current.env:
                if searcher(s,name):
                    return s
            if deep:
                current = current.outer
        return None

class Tool:
    @staticmethod
    def lookup(name,lst,func):
        return Utils().lookup(name,lst,func)

    @staticmethod
    def checkRedeclare(listSym:List[Symbol],scope:Scope):
        for i in range(0,len(listSym)):
            sym = listSym[i]
            if Tool.lookup(sym.name,scope.env + listSym[0:i],lambda n:n.name):
                raise Redeclared(sym.kind,sym.name)


class StaticChecker(BaseVisitor):

    def __init__(self,ast):
        self.ast = ast
        self.globalScope = Scope(Program([]),None)

    def visit(self,ast:AST,param):
        return ast.accept(self,param)

    def check(self):
        io_scope = Scope(ClassDecl(Id("io"),[]),self.globalScope)
        static = True
        io_scope.env = [
            Symbol("readInt",MType([],IntType()), Method(), static),
            Symbol("writeInt",MType([IntType()],VoidType()), Method(), static),
            Symbol("writeIntLn",MType([IntType()],VoidType()), Method(), static),
            Symbol("readFloat",MType([],FloatType()), Method(), static),
            Symbol("writeFloat",MType([FloatType()],VoidType()), Method(), static),
            Symbol("writeFloatLn",MType([FloatType()],VoidType()), Method(), static),
            Symbol("readBool",MType([],BoolType()), Method(), static),
            Symbol("writeBool",MType([BoolType()],VoidType()), Method(), static),
            Symbol("writeBoolLn",MType([BoolType()],VoidType()), Method(), static),
            Symbol("readStr",MType([],StringType()), Method(), static),
            Symbol("writeStr",MType([StringType()],VoidType()), Method(), static),
            Symbol("writeStrLn",MType([StringType()],VoidType()), Method(), static)
        ]
        io_class = Symbol("io",MType([],ClassType(Id("io"))),Class(),io_scope)
        return self.visit(self.ast,[io_class])

    def visitProgram(self, ast:Program, buildIn:List[Symbol]):
        self.globalScope.env.extend(buildIn)

        newSymList = [
            Symbol(
                c.classname.name,
                MType([],ClassType(c.classname)),
                Class(),False,Scope(c,self.globalScope)
            ) for c in ast.decl
        ]
        
        Tool.checkRedeclare(newSymList, self.globalScope)
        self.globalScope.env.extend(newSymList)
        
        for c in ast.decl:
            if c.parentname:
                parentSym:Symbol = self.globalScope.get_sympol(c.parentname.name)
                if parentSym==None:
                    raise Undeclared(Class(),c.parentname.name)
                # check type here ...
                classScope:Scope = self.globalScope.get_sympol(c.classname.name).value
                classScope.outer = parentSym.value


        deep_visit = [self.visit(c,self.globalScope) for c in ast.decl]

        return "x" 

    def visitClassDecl(self, ast:ClassDecl, outerScope:Scope):
        classSym:Symbol = outerScope.get_sympol(ast.classname.name)

        classScope = Scope(ast,outerScope)

        newSymList = []
        for mem in ast.memlist:
            if isinstance(mem,AttributeDecl):
                if isinstance(mem.decl,ConstDecl):
                    s = Symbol(mem.decl.constant.name,MType([],mem.decl.constType),Constant(),None)
                if isinstance(mem.decl,VarDecl):

                    s = Symbol(mem.decl.variable.name,MType([],mem.decl.varType),Attribute(),None)
            if isinstance(mem,MethodDecl):
                s = Symbol(
                    mem.name.name,
                    MType([p.varType for p in mem.param],mem.returnType),
                    Method(),
                    True if isinstance(mem.kind,Static) else False
                )
            newSymList.append(s)

        Tool.checkRedeclare(newSymList,classScope)
        classScope.env = newSymList

        deep_visit = [self.visit(mem,classScope) for mem in ast.memlist]

        classSym.value = classScope
        return #Symbol(ast.classname,MType([],ClassType(Id(ast.classname))),Class(),None)

    def visitMethodDecl(self, ast:MethodDecl, classScope:Scope):
        return 

    def visitAttributeDecl(self, ast:AttributeDecl, classScope:Scope):
        
        return self.visit(ast.decl,classScope)
        
    def visitVarDecl(self, ast:VarDecl, scope):
        if ast.varInit:
            self.checkAssign(ast.varType,ast.varInit,scope,False)
        return None

    def visitConstDecl(self, ast:ConstDecl, scope:Scope):
        if str(ast.constType) == str(VoidType()):
            raise TypeMismatchInConstant(ast)

        if ast.value is None:
            raise IllegalConstantExpression(None)
        
        val = self.visit(ast.value,scope) # type
        if self.checkType(ast.constType,val) == False:
            raise TypeMismatchInConstant(ast)

        return None
    
    def checkType(self,typ:Type,val:Type):
        if str(typ) == str(val):
            return True
        if str(typ) == str(FloatType()) and str(val) == str(IntType()):
            return True

        if isinstance(typ,ClassType) and isinstance(val,ClassType):
            valScope:Scope = self.globalScope.get_sympol(val.classname).value
            iter = valScope.outer            
            while iter:
                if isinstance(iter.ctx,ClassDecl) and iter.ctx.classname.name == typ.classname:
                    return True
                iter = iter.outer
        return False


    def checkAssign(self,typ:Type,val:Expr,scope:Scope,constant:bool):
        valTyp = self.visit(val)


        if constant:
            ""
        else:
            ""
        return

    def visitBinaryOp(self, ast, param):
        return None

    def visitUnaryOp(self, ast, param):
        return None

    def visitCallExpr(self, ast, param):
        return None

    def visitNewExpr(self, ast, param):
        return None

    def visitId(self, ast, param):
        return None

    def visitArrayCell(self, ast, param):
        return None

    def visitFieldAccess(self, ast, param):
        return None

    def visitBlock(self, ast, param):
        return None

    def visitIf(self, ast, param):
        return None

    def visitFor(self, ast, param):
        return None

    def visitContinue(self, ast, param):
        return None

    def visitBreak(self, ast, param):
        return None

    def visitReturn(self, ast, param):
        return None

    def visitAssign(self, ast, param):
        return None

    def visitCallStmt(self, ast, param):
        return None

    def visitSelfLiteral(self, ast, param):
        return None 

    def visitArrayLiteral(self, ast, param):
        return None 

    def visitIntType(self, ast, param):
        return None

    def visitFloatType(self, ast, param):
        return None

    def visitBoolType(self, ast, param):
        return None

    def visitStringType(self, ast, param):
        return None

    def visitVoidType(self, ast, param):
        return None

    def visitArrayType(self, ast, param):
        return None

    def visitClassType(self, ast, param):
        return None

    def visitIntLiteral(self, ast, param):
        return None

    def visitFloatLiteral(self, ast, param):
        return None

    def visitBooleanLiteral(self, ast, param):
        return None

    def visitStringLiteral(self, ast, param):
        return None

    def visitNullLiteral(self, ast, param):
        return None

    def visitStatic(self, ast, param):
        return None

    def visitInstance(self, ast, param):
        return None

