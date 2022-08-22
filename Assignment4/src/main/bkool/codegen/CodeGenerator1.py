from Emitter import Emitter
from functools import reduce

from Frame import Frame
from abc import ABC
from Visitor import *
from AST import *

class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "i"+str(self.value)

class CName(Val):
    def __init__(self, value:str):
        self.value = value
    def __str__(self):
        return "c({})".format(self.value)

class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype
    def __str__(self):
        return "("+(",".join([str(i) for i in self.partype]) if self.partype else "")+"=>"+str(self.rettype)+")";

class Symbol:
    def __init__(self, isStatic:bool, name:str, mtype:MType, cname:CName, value=None, isConstant:bool=False):
        self.name = name
        self.mtype = mtype
        self.value = value
        self.cname = cname
        self.isStatic = isStatic
        self.isConstant = isConstant

    def __str__(self):
        return "Sym("+("s" if self.isStatic else "i")+("c" if self.isConstant else "")+","+self.name+","+str(self.mtype)+","+str(self.cname)+","+str(self.value)+")"


class CodeGenerator:
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [
            Symbol(True, "readInt", MType(list(), IntType()), CName(self.libName)),
            Symbol(True, "writeInt", MType([IntType()], VoidType()), CName(self.libName)),
            Symbol(True, "writeIntLn", MType([IntType()], VoidType()), CName(self.libName)),
            Symbol(True, "readFloat", MType(list(), FloatType()), CName(self.libName)),
            Symbol(True, "writeFloat", MType([FloatType()], VoidType()), CName(self.libName)),
            Symbol(True, "writeFloatLn", MType([FloatType()], VoidType()), CName(self.libName)),
            Symbol(True, "readBool", MType(list(), BoolType()), CName(self.libName)),
            Symbol(True, "writeBool", MType([BoolType()],VoidType()), CName(self.libName)),
            Symbol(True, "writeBoolLn", MType([BoolType()], VoidType()), CName(self.libName)),
            Symbol(True, "readStr", MType(list(), StringType()), CName(self.libName)),
            Symbol(True, "writeStr", MType([StringType()],VoidType()), CName(self.libName)),
            Symbol(True, "writeStrLn", MType([StringType()], VoidType()), CName(self.libName))
        ]

    def gen(self, ast, path):
        #ast: AST
        #dir_: String
        gl = self.init()
        gc = CodeGenVisitor(ast, gl, path)
        gc.visit(ast, None)


class SubBody():
    def __init__(self, frame, sym):
        self.frame = frame
        self.sym = sym


class Access():
    def __init__(self, cname: CName, frame:Frame=None, sym:List[Symbol]=None, isLeft:bool=True, isFirst:bool=False, isToCheckArray:bool=False, isLoad:bool=False):
        self.cname = cname
        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst
        self.isToCheckArray = isToCheckArray
        self.isLoad = isLoad

class CodeGenVisitor(BaseVisitor):
    def __init__(self, astTree, env:List[Symbol], path):
        self.astTree = astTree
        self.env = env
        self.path = path
        
    def findSym(self,name:str,cname:str,env:List[Symbol]=None):
        env = env if isinstance(env,List) else self.env
        result = next(
            filter(
                lambda sym: name == sym.name and (cname is None or cname == sym.cname.value), 
                env
            ),
            None
        ) 
        # print("findSym: <"+name+"> in <"+(cname if cname else "")+"> = " + str(result))
        return result   

    # def findSyms(self,name:str,cname:str,env:List[Symbol]=None):
    #     env = env if isinstance(env,List) else self.env
    #     result = filter(
    #             lambda sym: name == sym.name and (cname is None or cname == sym.cname.value), 
    #             env
    #         )
    #     print("findSyms: <"+name+"> in <"+(cname if cname else "")+"> = " + str([str(r) for r in result]))
    #     return result   
    
    def visitProgram(self, ast: Program, o):
        print("-"*10)
        # prepare for environment
        for classDecl in ast.decl:
            cname = CName(classDecl.classname.name)
            for mem in classDecl.memlist:
                
                if isinstance(mem,MethodDecl):
                    isStatic = type(mem.kind) == Static
                    mtype = MType([x.varType for x in mem.param], mem.returnType)
                    sym = Symbol(isStatic,mem.name.name,mtype,cname)
                    self.env.append(sym)
                elif isinstance(mem,AttributeDecl):
                    isStatic = type(mem.kind) == Static
                    if isinstance(mem.decl,VarDecl):
                        mtype = MType(None, mem.decl.varType)
                        sym = Symbol(isStatic,mem.decl.variable.name,mtype,cname,mem.decl.varInit,False)
                        self.env.append(sym)
                    if isinstance(mem.decl,ConstDecl):
                        mtype = MType(None, mem.decl.constType)
                        sym = Symbol(isStatic,mem.decl.constant.name,mtype,cname,mem.decl.value,True)
                        self.env.append(sym)
                        
        print([str(i) for i in self.env])
        # visit every class declaration                        
        for classDecl in ast.decl:
            print("[C]:"+classDecl.classname.name)
            self.visit(classDecl, None)
        
    def visitClassDecl(self, ast: ClassDecl, c):
        className = ast.classname.name
        filename = "{}/{}.j".format(self.path, className)
        ctxt = Access(CName(className))
        self.emit = Emitter(filename)
        
        # Opening
        self.emit.printout(
            self.emit.emitPROLOG(className, "java.lang.Object"))

        # First, visit fields
        hasStatic = False
        for ele in ast.memlist: 
            if isinstance(ele,AttributeDecl):
                if isinstance(ele.kind,Static) and isinstance(ele.decl,VarDecl):
                    hasStatic = True
                self.visit(ele, ctxt)
                
        # Then, generate default constructor
        self.genMETHOD(
            MethodDecl(
                Instance(),Id("<init>"),list(),None,Block([],[])
            ), ctxt, Frame("<init>", VoidType()), hasStatic
        )
        
        # Then, generate default Static init
        if hasStatic:
            self.genMETHOD(
                MethodDecl(
                    Static(), Id("<clinit>"),list(),None,Block([],[])
                ), ctxt, Frame("<clinit>", VoidType())                
            )
        
        # Finally, visit methods
        for ele in ast.memlist: 
            if isinstance(ele,MethodDecl):
                self.visit(ele, ctxt)
        
        # Ending
        self.emit.emitEPILOG()
        
    def visitAttributeDecl(self, ast:AttributeDecl, o: Access):
        ctxt = o
        return self.visit(ast.decl,ctxt)
    
    def visitVarDecl(self, ast:VarDecl, o:Access):
        ctxt = o
        frame = o.frame
        syms = o.sym
        print("Vardecl:"+ast.variable.name)
        if syms == None: # -> Attribute
            getSym = self.findSym(ast.variable.name,o.cname.value)
            typ = getSym.mtype.rettype
            if getSym.isStatic:
                emitCode = self.emit.emitATTRIBUTE(ast.variable.name,typ)
            else:
                emitCode = self.emit.emitINSTANCEFIELD(ast.variable.name,typ)
            
            if isinstance(emitCode,str) and (not "public" in emitCode):
                e = [] 
                for w in emitCode.split(" "):
                    e.append(w)
                    if ".field" in w:
                        e.append("public")
                emitCode = " ".join(e)
                        
            self.emit.printout(emitCode)
            
            return getSym
        else:            # -> Parram or Local var
            newIndex = frame.getNewIndex()
            self.emit.printout(
                self.emit.emitVAR(
                    newIndex, 
                    ast.variable.name, 
                    ast.varType, 
                    frame.getStartLabel(),
                    frame.getEndLabel(), 
                    frame
                )
            )
            # initVal, initType = self.visit(ast.varInit, ctxt)
            newSym = Symbol(False,ast.variable.name,MType(None,ast.varType),None,Index(newIndex))
            syms.append(newSym)
            
            # if isinstance(ast.varType,ArrayType) and ast.varInit is None:
            #     arrSize = ast.varType.size
            #     arrType = ast.varType.eleType
            #     print("-"*50)
            #     self.emit.printout(self.emit.emitInitNewLocalArray(newIndex,arrSize,arrType,frame))
            print("-"*50)
            self.handelAssign(ast.variable,ast.varInit,Access(ctxt.cname,ctxt.frame, ctxt.sym,ctxt.isLeft,isFirst=True))
            return newSym

    def visitConstDecl(self, ast:ConstDecl, o: Access):
        ctxt = o
        frame = ctxt.frame
        syms = ctxt.sym
        print("Constdecl:"+ast.constant.name)
        if syms == None: # attributes
            getSym = self.findSym(ast.constant.name,o.cname.value)
            valueStr = None
            if not type(getSym.mtype.rettype) in [ClassType, ArrayType]:
                valueStr = self.visit(ast.value,ctxt)
            typ = getSym.mtype.rettype
            if getSym.isStatic:
                emitCode = self.emit.emitATTRIBUTE(ast.constant.name,typ,True,valueStr)
            else:
                emitCode = self.emit.emitINSTANCEFIELD(ast.constant.name,typ,True,valueStr)
            
            if isinstance(emitCode,str) and (not "public" in emitCode):
                e = [] 
                for w in emitCode.split(" "):
                    e.append(w)
                    if ".field" in w:
                        e.append("public")
                emitCode = " ".join(e)
                        
            self.emit.printout(emitCode)
            
            return getSym
        else:            
            # -> Parram or Local var
            cValue = ast.value
            if isinstance(ast.constType, ClassType):
                
                newIndex = frame.getNewIndex()
                cValue = Index(newIndex)
                self.emit.printout(
                    self.emit.emitVAR(
                        newIndex, 
                        ast.constant.name, 
                        ast.constType, 
                        frame.getStartLabel(),
                        frame.getEndLabel(), 
                        frame
                    )
                )
            newSym = Symbol(False,ast.constant.name,MType(None,ast.constType),None,cValue, True)
            syms.append(newSym)
            
            self.handelAssign(ast.constant,ast.value,Access(ctxt.cname,ctxt.frame, ctxt.sym,ctxt.isLeft,isFirst=True))
            return newSym

    def visitMethodDecl(self, ast: MethodDecl, o: Access):
        frame = Frame(ast.name.name, ast.returnType)
        self.genMETHOD(ast, o, frame)

    def visitCallExpr(self, ast:CallExpr, o: Access):
        print("+CallExpr")
        ctxt = o
        return self.handleCall(ast.obj,ast.method,ast.param,ctxt,True)
    
    def visitCallStmt(self, ast: CallStmt, o: Access):
        print("+CallStmt")
        ctxt = o
        self.handleCall(ast.obj,ast.method,ast.param,ctxt,False)
    
    def handleCall(self, obj:Expr,method:Id,param:List[Expr],ctxt:Access,isExpr:bool):     
        frame = ctxt.frame
        nenv = ctxt.sym
        objCode, objType = self.visit(obj,Access(ctxt.cname,ctxt.frame,[],True))
        print(isinstance(objType,ClassType))
        if isinstance(objType,ClassType):
            sym = self.findSym(method.name, objType.classname.name)
            cname = sym.cname.value
            ctype = sym.mtype
            in_ = ("", list())
            for x in param:
                print(x)
                str1, typ1 = self.visit(x, Access(ctxt.cname,frame, nenv, False))
                in_ = (in_[0] + str1, in_[1].append(typ1))
            code = in_[0] + self.emit.emitINVOKESTATIC(cname+"/"+method.name, ctype, frame)
            
            if isExpr:
                return code, sym.mtype.rettype
            else:
                self.emit.printout(code)
    
    def visitIf(self, ast: If, o: Access):
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        expCode, expType = self.visit(ast.expr, Access(ctxt.cname,frame, nenv, False, True))
        self.emit.printout(expCode)

        labelT = frame.getNewLabel()  # true
        labelE = frame.getNewLabel()  # exit

        self.emit.printout(self.emit.emitIFTRUE(labelT, frame))

        hasReturnStmt = ast.elseStmt is not None and True in [self.visit(x, o) for x in ast.elseStmt] 
        if not hasReturnStmt:
            self.emit.printout(self.emit.emitGOTO(labelE, frame)) 

        self.emit.printout(self.emit.emitLABEL(labelT, frame))
        hasReturnStmt = True in [self.visit(x, o) for x in (ast.thenStmt if isinstance(ast.thenStmt,List) else [ast.thenStmt])] and hasReturnStmt


        self.emit.printout(self.emit.emitLABEL(labelE, frame))
        return hasReturnStmt
    
    def visitReturn(self, ast: Return, o: Access):
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        retType = frame.returnType
        if not type(retType) is VoidType:
            expCode, expType = self.visit(ast.expr, Access(ctxt.cname,frame, nenv, False, True))
            if type(retType) is FloatType and type(expType) is IntType:
                expCode = expCode + self.emit.emitI2F(frame)
            self.emit.printout(expCode)
        # self.emit.printout(self.emit.emitGOTO(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(retType, frame))
        return True
    
    def visitAssign(self, ast:Assign, o: Access):
        print("+VisitAssign")
        ctxt = o
        self.handelAssign(ast.lhs,ast.exp,ctxt)
        
    def handelAssign(self, lhs:Expr, rhs:Expr, o: Access):
        print("+HandelAssign")
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        
        isArray = self.visit(lhs,Access(ctxt.cname,frame, nenv, isToCheckArray=True))
        if rhs is None and not isArray:
            return
                
        if isinstance(lhs,ArrayCell):
            lhsLoadCode, _ = self.visit(lhs, Access(ctxt.cname,frame, nenv, True, isFirst=False, isLoad=True))
            print("Ll::\n",lhsLoadCode)
            self.emit.printout(lhsLoadCode)
    
        # code store
        lhsCode, lhsType = self.visit(lhs, Access(ctxt.cname,frame, nenv, True, isFirst=ctxt.isFirst))
        print("Ls::\n",lhsCode, lhsType)
        expCode, expType = self.visit(rhs, Access(ctxt.cname,frame, nenv, False)) if rhs is not None else \
            ("",lhsType)
        print("R::\n",expCode, expType)
        
        # print(expCode, expType)
        if type(lhsType) is FloatType and type(expType) is IntType:
            expCode = expCode + self.emit.emitI2F(frame)
        self.emit.printout(expCode)
        self.emit.printout(lhsCode)

    def genMETHOD(self, decl: MethodDecl, o: Access, frame: Frame,hasStatic=False):
        print("+Method:"+frame.name)
        ctxt = o
        className = ctxt.cname.value
        access = Access(ctxt.cname,frame,[])
        
        isStatic = type(decl.kind) == Static
        isInit = decl.returnType is None
        isMain = decl.name.name == "main" and len(decl.param) == 0 and \
            type(decl.returnType) is VoidType
        returnType = VoidType() if isInit else decl.returnType
        methodName = ("<clinit>" if isStatic else "<init>") if isInit else decl.name.name
        intype = [ArrayType(0, StringType())] if isMain else list(
            map(lambda x: x.varType, decl.param))
        mtype = MType(intype, returnType)

        self.emit.printout(
            self.emit.emitMETHOD(methodName, mtype, isStatic, frame))

        frame.enterScope(True) # reset lable =0
        glenv = access.sym

        # Generate code for parameter declarations
        if isInit and not isStatic:
            self.emit.printout(
                self.emit.emitVAR(
                    frame.getNewIndex(), 
                    "this", 
                    ClassType(Id(className)), 
                    frame.getStartLabel(), 
                    frame.getEndLabel(), 
                    frame
                )
            )
            this = Symbol(False,"this",MType(None,ClassType(Id(className)),),CName(Id(className)),Index(0))
            glenv.append(this)
        elif isInit and isStatic:
            pass
        
        elif isMain:
            self.emit.printout(
                self.emit.emitVAR(
                    frame.getNewIndex(), 
                    "args", 
                    ArrayType(0, StringType()), 
                    frame.getStartLabel(), 
                    frame.getEndLabel(), 
                    frame
                )
            )
        else:
            local = reduce(
                lambda env, ele: Access(ctxt.cname,frame, [self.visit(ele, env)]+
                                        env.sym), 
                decl.param, 
                Access(ctxt.cname,frame,[])
            )
            glenv = local.sym+glenv
            
        # Access method's body
        body = decl.body
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(),frame))

        if isInit and not isStatic:
            self.emit.printout(
                self.emit.emitREADVAR(
                    "this",
                    ClassType(Id(className)), 
                    0, 
                    frame)
            )
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
            
            filterSym = lambda sym: \
                isinstance(sym,Symbol) and \
                ((not hasStatic and not sym.isConstant) or not sym.isStatic) and \
                sym.cname.value == o.cname.value \
                and sym.mtype.partype == None
                    
            attributes = [sym for sym in self.env if filterSym(sym)]
            
            # print("__init")
            _ac = Access(access.cname,access.frame, access.sym,access.isLeft,isFirst=True)
            for attr in attributes:
                self.handelAssign(FieldAccess(Id("this"),Id(attr.name)), attr.value, _ac)
        
        if isInit and isStatic:
            filterSym = lambda sym: \
                isinstance(sym,Symbol) and \
                sym.isStatic and \
                sym.cname.value == o.cname.value and \
                sym.mtype.partype == None
                
            attributes = [sym for sym in self.env if filterSym(sym)]
            _ac = Access(access.cname,access.frame, access.sym,access.isLeft,isFirst=True)
            # print("__clinit")
            for attr in attributes:
                self.handelAssign(FieldAccess(Id(className),Id(attr.name)), attr.value, _ac)
                            
        # Generate code for statements           
        # print("<<<",[str(i) for i in glenv])
        glenv = reduce(
            lambda env, ele: Access(ctxt.cname,frame, env.sym if self.visit(ele, env) else [], isFirst=True), 
            body.decl,
            Access(ctxt.cname,frame,glenv)
        ).sym
        # self.emit.printout("--------------\n")
        # print("<<<",[str(i) for i in glenv])
        
        list(map(
            lambda x: self.visit(x, Access(ctxt.cname,frame, glenv)), 
            body.stmt
        ))
        
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
            
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        
        frame.exitScope()

    def visitFor(self, ast: For, o: Access):
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym

        exp1Code, _ = self.visit(ast.expr1, Access(frame, nenv, False, True))
        exp2Code, _ = self.visit(ast.expr2, Access(frame, nenv, False, True))
        lhsWCode, _ = self.visit(ast.id, Access(frame, nenv, True, True))  # Write code
        lhsRCode, _ = self.visit(ast.id, Access(frame, nenv, False, False))  # Read code

        labelS = frame.getNewLabel()  # label start
        labelE = frame.getNewLabel()  # label end

        # Init value
        self.emit.printout(exp1Code)
        self.emit.printout(lhsWCode)
        frame.enterLoop()
        # Loop
        self.emit.printout(self.emit.emitLABEL(labelS, frame))
        # 1. Condition
        self.emit.printout(lhsRCode)
        self.emit.printout(exp2Code)
        if ast.up:
            self.emit.printout(self.emit.emitIFICMPGT(labelE, frame))
        else:
            self.emit.printout(self.emit.emitIFICMPLT(labelE, frame))
        # 2. Statements
        hasReturnStmt = True in [self.visit(x, o) for x in (ast.loop.stmt if isinstance(ast.loop, Block) else [ast.loop])]
        self.emit.printout(self.emit.emitLABEL(frame.getContinueLabel(), frame))
        # 3. Update index
        self.emit.printout(lhsRCode)
        self.emit.printout(self.emit.emitPUSHICONST(1, frame))
        self.emit.printout(self.emit.emitADDOP('+' if ast.up else '-', IntType(), frame))
        self.emit.printout(lhsWCode)

        if not hasReturnStmt:
            self.emit.printout(self.emit.emitGOTO(labelS, frame))  # loop
        self.emit.printout(self.emit.emitLABEL(labelE, frame))
        self.emit.printout(self.emit.emitLABEL(frame.getBreakLabel(), frame))
        frame.exitLoop()
    
    def visitBinaryOp(self, ast: BinaryOp, o: Access):
        ctxt = o
        frame = ctxt.frame
        op = str(ast.op).lower()

        lCode, lType = self.visit(ast.left, ctxt)
        rCode, rType = self.visit(ast.right, ctxt)
        if op in ['+', '-', '*', '%', '\\', '/','<>', '=', '>', '<', '>=', '<=']:  # for number type
            mType = FloatType() if FloatType in [type(x) for x in [lType, rType]] else IntType()
            if op == '/': mType = FloatType()  # mergeType >= lType, rType
            if type(lType) is IntType and type(mType) != type(lType): lCode = lCode + self.emit.emitI2F(frame)
            if type(rType) is IntType and type(mType) != type(rType): rCode = rCode + self.emit.emitI2F(frame)
            if ['+', '-', '*', '\\', '/','%']:
                if op in ['+', '-']:
                    return lCode + rCode + self.emit.emitADDOP(op, mType, frame), mType
                if op in ['*', '/']:
                    return lCode + rCode + self.emit.emitMULOP(op, mType, frame), mType
                if op == '%':
                    return lCode + rCode + self.emit.emitMOD(frame), mType
            else:  # op to boolean: > <= = <>, ...
                return lCode + rCode + self.emit.emitREOP(op, mType, frame), BoolType()
        else:  # for boolean type
            mType = BoolType()
            if op == '||': return lCode + rCode + self.emit.emitOROP(frame), mType
            if op == '&&': return lCode + rCode + self.emit.emitANDOP(frame), mType
    
    def visitBinaryOp(self, ast: BinaryOp, o: Access):
        e1c, e1t = self.visit(ast.left, o)
        e2c, e2t = self.visit(ast.right, o)
        return e1c + e2c + self.emit.emitADDOP(ast.op, e1t, o.frame), e1t

    def visitNewExpr(self, ast: NewExpr, o: Access):
        print("+NewExpr")
        ctxt = o
        frame = o.frame
        
        lexeme = "{}/<init>".format(ast.classname.name)
        frame.push()
        code = self.emit.emitNEW(ast.classname.name)
        code += self.emit.emitDUP(frame)
        code += self.emit.emitINVOKESPECIAL(frame,lexeme,MType([],VoidType()))
        return code, ClassType(ast.classname)
        
    def visitId(self, ast:Id, o:Access):
            
        ctxt = o
        frame = ctxt.frame
        isLeft = ctxt.isLeft
        isFirst = ctxt.isFirst
        symEnv = ctxt.sym
        print("+Id:"+ast.name)
        # print("isFirst",isFirst)
        # print([str(i) for i in symEnv])
        # find in local env
        sym = self.findSym(ast.name,None,symEnv)
        # print(">>",sym)
        if sym is not None:
            emitType = sym.mtype.rettype
            
            if ctxt.isToCheckArray:
                return isinstance(emitType,ArrayType)
            if isinstance(sym.value,Index):                
                if sym.isStatic: 
                    if isLeft:
                        if isinstance(emitType,ArrayType):
                            # frame.push()
                            emitCode = ""
                            if isFirst:
                                # print("emitInitNewLocalArray")
                                emitCode = self.emit.emitInitNewStaticArray(None, emitType.size, emitType.eleType,frame)
                            else:
                                emitCode = "";
                            self.emit.printout(emitCode)
                        retCode = self.emit.emitPUTSTATIC(sym.cname.value + "/" + sym.name, emitType, frame)
                    else:
                        retCode = self.emit.emitGETSTATIC(sym.cname.value + "/" + sym.name, emitType, frame)
                else:
                    if isLeft:
                        frame.push()
                        if isinstance(emitType,ArrayType):
                            emitCode = ""
                            if isFirst:
                                # print("emitInitNewLocalArray")
                                emitCode = self.emit.emitInitNewLocalArray(sym.value, emitType.size, emitType.eleType,frame)
                            else:
                                emitCode = ""
                            self.emit.printout(emitCode)
                        retCode = self.emit.emitWRITEVAR(sym.name, emitType, sym.value.value, frame)
                    else:
                        
                        retCode = self.emit.emitREADVAR(sym.name, emitType, sym.value.value, frame)
                    
                return retCode, sym.mtype
            
            elif sym.value is not None:
                return self.visit(sym.value, ctxt)
        
        # find in global env
        sym = self.findSym(ast.name,ctxt.cname.value)
        if sym is not None:
            emitType = sym.mtype.rettype
            
            if ctxt.isToCheckArray:
                return isinstance(emitType,ArrayType)
            if not sym.isStatic:
                if isLeft:
                    if isFirst:
                        frame.push()
                    if type(emitType) in [ArrayType,ClassType] and isFirst:
                        frame.push()
                                                
                    if isinstance(emitType,ArrayType):
                        emitCode = ""
                        if isFirst:
                            # print("emitInitNewLocalArray")
                            emitCode = self.emit.emitInitNewLocalArray(sym.value, emitType.size, emitType.eleType,frame)
                        else:
                            emitCode = ""
                        self.emit.printout(emitCode)
                    fieldCode = self.emit.emitPUTFIELD(sym.name, emitType, frame)
                else:
                    fieldCode = self.emit.emitGETFIELD(sym.name, emitType, frame)
            else:
                if isLeft:
                    if isFirst:
                        frame.push()
                    if type(emitType) in [ArrayType,ClassType] and isFirst:
                        frame.push()
                    if isinstance(emitType,ArrayType):
                        emitCode = ""
                        if isFirst:
                            # print("emitInitNewLocalArray")
                            emitCode = self.emit.emitInitNewStaticArray(None,emitType.size, emitType.eleType,frame)
                        else:
                            emitCode = ""
                        self.emit.printout(emitCode)
                    fieldCode = self.emit.emitPUTSTATIC(sym.cname.value+"/"+sym.name, emitType, frame)
                else:
                    fieldCode = self.emit.emitGETSTATIC(sym.cname.value+"/"+sym.name, emitType, frame)
            
            return fieldCode, sym.mtype
             
        return "", ClassType(ast)
    
    def visitFieldAccess(self, ast: FieldAccess, o: Access):
        print("+FieldAccess:"+str(ast))        
        
        if o.isToCheckArray:
            return self.visit(ast.fieldname,o)
        
        ctxt = o
        frame = ctxt.frame  
        nenv = ctxt.sym
        isLeft = ctxt.isLeft
        
        objCode, objType = self.visit(ast.obj,Access(ctxt.cname, frame,nenv,False,isFirst=ctxt.isFirst)) # load 'this'
        if not ctxt.isLoad:
            self.emit.printout(objCode)
        if isinstance(objType,MType):
            objRettype = objType.rettype
            if isinstance(objRettype,ClassType):
                fieldCode, fieldType = self.visit(ast.fieldname, Access(CName(objRettype.classname.name),frame,nenv,isLeft, isFirst=ctxt.isFirst))
                fieldCode = reduce(
                    lambda e, w: e + " " + ((objRettype.classname.name+"/"+w) if w==ast.fieldname.name else w), 
                    fieldCode.split(" "),
                    ""
                ) # add <class-name>/
                
                return fieldCode, fieldType
        
        elif isinstance(objType,ClassType):
            print(objType)
            return self.visit(ast.fieldname, Access(CName(objType.classname.name),frame,nenv,isLeft, isFirst=ctxt.isFirst))
 
    def visitUnaryOp(self, ast: UnaryOp, o: Access):
        frame = o.frame
        op = ast.op
        bCode, bType = self.visit(ast.body, o)
        
        # if op is +, then no thing happens
        if op == '-':
            return bCode + self.emit.emitNEGOP(bType, frame), bType
        if op == '!': 
            return bCode + self.emit.emitNOT(bType, frame), bType
    
    def visitBreak(self, ast: Break, o: Access):
        ctxt = o
        frame = ctxt.frame
        self.emit.printout(self.emit.emitGOTO(frame.getBreakLabel(), frame))

    def visitContinue(self, ast: Continue, o: Access):
        ctxt = o
        frame = ctxt.frame
        self.emit.printout(self.emit.emitGOTO(frame.getContinueLabel(), frame))

    
    def visitArrayLiteral(self, ast:ArrayLiteral, o: Access):
          
        ctxt = o
        frame = ctxt.frame
        emitCode = ""
        eleType = None
        for i in range(0,len(ast.value)):
            emitCode += self.emit.emitDUP(frame) 
            emitCode += self.emit.emitPUSHICONST(i,frame) 
            eleCode, eleType = self.visit(ast.value[i],ctxt)
            emitCode += eleCode
            emitCode += self.emit.emitASTORE(eleType,frame)

        return emitCode, ArrayType(len(ast.value),eleType)

    def visitArrayCell(self, ast:ArrayCell, o:Access):   
        
        if o.isToCheckArray:
            return self.visit(ast.arr,o)
        ctxt = o
        frame = ctxt.frame
        # print("isleft", ctxt.isLeft)     
        if ctxt.isLeft == False:
            arrCode, arrType = self.visit(ast.arr,ctxt)
            indexCode, indexType = self.visit(ast.idx,ctxt)
            arrLoadCode = self.emit.emitALOAD(arrType.rettype.eleType if isinstance(arrType.rettype,ArrayType) else None,frame)
            return arrCode+indexCode+arrLoadCode, arrType
        else:
            # load
            if ctxt.isLoad:
                frame.pop()
                arrCode, arrType = self.visit(ast.arr,Access(ctxt.cname,ctxt.frame,ctxt.sym,False,ctxt.isFirst))
                indexCode, indexType = self.visit(ast.idx,ctxt)
                return arrCode+indexCode, arrType
            # store
            else:
                arrCode, arrType = self.visit(ast.arr,Access(ctxt.cname,ctxt.frame,ctxt.sym,False,ctxt.isFirst,isLoad=True))
                frame.push()
                arrStoreCode = self.emit.emitASTORE(arrType.rettype.eleType if isinstance(arrType.rettype,ArrayType) else None,frame)
                return arrStoreCode, arrType
                    
    def visitIntLiteral(self, ast: IntLiteral, o: Access):
        ctxt = o
        frame = ctxt.frame
        
        if ctxt is None or frame is None:
            return ast.value
        return self.emit.emitPUSHICONST(ast.value, frame), IntType()

    def visitFloatLiteral(self, ast: FloatLiteral, o: Access):
        ctxt = o
        frame = ctxt.frame
        
        if ctxt is None or frame is None:
            return str(ast.value)
        
        return self.emit.emitPUSHFCONST(str(ast.value), o.frame), FloatType()

    def visitBooleanLiteral(self, ast: BooleanLiteral, o: Access):
        ctxt = o
        frame = ctxt.frame
        
        if ctxt is None or frame is None:
            return str(int(ast.value))
        
        return self.emit.emitPUSHICONST(str(ast.value).lower(), o.frame), BoolType()

    def visitStringLiteral(self, ast: StringLiteral, o: Access):
        ctxt = o
        frame = ctxt.frame
        
        if ctxt is None or frame is None:
            return ast.value
        
        return self.emit.emitPUSHCONST(ast.value, StringType(), o.frame), StringType()
