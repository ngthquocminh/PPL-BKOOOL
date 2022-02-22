from BKOOLVisitor import BKOOLVisitor
from BKOOLParser import BKOOLParser
from AST import *

class ASTGeneration(BKOOLVisitor):
    def visitProgram(self,ctx:BKOOLParser.ProgramContext):
        return Program([ClassDecl(Id(ctx.ID().getText()),[self.visit(ctx.member())])])
                        

    def visitMember(self,ctx:BKOOLParser.MemberContext):
        return MethodDecl(Static(),Id(ctx.ID().getText()),[],VoidType(),Block([],[self.visit(ctx.body())]))

    def visitBody(self,ctx:BKOOLParser.BodyContext):
        return CallStmt(Id(ctx.ID(0).getText()),Id(ctx.ID(1).getText()),[self.visit(ctx.exp())])
  
    def visitExp(self,ctx:BKOOLParser.ExpContext):
        if ctx.getChildCount() == 3:
            return BinaryOp('+',IntLiteral(int(ctx.INTLIT(0).getText())),IntLiteral(int(ctx.INTLIT(1).getText())))
        else:
            return IntLiteral(int(ctx.INTLIT(0).getText()))
        

