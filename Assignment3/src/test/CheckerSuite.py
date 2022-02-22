import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    def test_redeclaration_01(self):
        input = Program([ClassDecl(Id("io"), [])])
        expect = "Redeclared Class: io"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_redeclaration_02(self):
        input = Program([ClassDecl(Id("A"), []),ClassDecl(Id("B"), []),ClassDecl(Id("A"), [])])
        expect = "Redeclared Class: A"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_redeclaration_03(self):
        input = Program([ClassDecl(
            Id("A"), 
            [
                MethodDecl(Instance(),Id("foo"),[],VoidType(),Block([],[])),
                AttributeDecl(Instance(),VarDecl(Id("foo"),IntType()))
            ]
        )])
        expect = "Redeclared Attribute: foo"
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_redeclaration_04(self):
        input = Program([ClassDecl(
            Id("A"), 
            [
                MethodDecl(Instance(),Id("A"),[],VoidType(),Block([],[])),
                AttributeDecl(Instance(),VarDecl(Id("A"),IntType()))
            ]
        )])
        expect = "Redeclared Attribute: A"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_redeclaration_05(self):
        input = Program([ClassDecl(
            Id("A"), 
            [
                AttributeDecl(Instance(),VarDecl(Id("A"),IntType())),
                MethodDecl(Instance(),Id("A"),[],VoidType(),Block([],[])),
            ]
        )])
        expect = "Redeclared Method: A"
        self.assertTrue(TestChecker.test(input,expect,405))

    def test_redeclaration_06(self):
        input = Program([ClassDecl(
            Id("A"), 
            [
                AttributeDecl(Instance(),VarDecl(Id("a"),IntType())),
                MethodDecl(Instance(),Id("foo"),[],VoidType(),Block([],[])),
                AttributeDecl(Static(),VarDecl(Id("a"),IntType(), IntLiteral(1))),
            ]
        )])
        expect = "Redeclared Attribute: a"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_redeclaration_07(self):
        input = Program([ClassDecl(
            Id("A"), 
            [
                AttributeDecl(Instance(),VarDecl(Id("a"),IntType())),
                MethodDecl(Instance(),Id("foo"),[],VoidType(),Block([],[])),
                AttributeDecl(Static(),VarDecl(Id("a"),IntType(), IntLiteral(1))),
            ]
        )])
        expect = "Redeclared Attribute: a"
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_redeclaration_08(self):
        input = Program([
            ClassDecl(
                Id("A"), 
                [
                    AttributeDecl(Instance(),VarDecl(Id("a"),IntType())),
                    MethodDecl(Instance(),Id("foo"),[],VoidType(),Block([],[])),
                ]),

            ClassDecl(
                Id("B"), 
                [
                    AttributeDecl(Instance(),VarDecl(Id("a"),IntType())),
                    MethodDecl(Instance(),Id("foo"),[],VoidType(),Block([],[])),
                    AttributeDecl(Static(),ConstDecl(Id("a"),IntType(), IntLiteral(1))),
                ],
                Id("A")),
                
        ])
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_redeclaration_08(self):
        input = Program([ClassDecl(Id("Ex"),[
            AttributeDecl(Instance(),ConstDecl(Id("x"),IntType(),FloatLiteral(10.0)))
        ])])
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(x),IntType,FloatLit(10.0))"
        self.assertTrue(TestChecker.test(input,expect,409))
        

    # def test_undeclared_function(self):
    #     input = Program([ClassDecl(Id("Child"), [
    #         MethodDecl(Static(),Id("main"),[],VoidType(),Block([],[CallStmt(SelfLiteral(),Id("foo"),[])]))
    #     ])],True)
    #     expect = "Undeclared Method: foo"
    #     self.assertTrue(TestChecker.test(input,expect,402))