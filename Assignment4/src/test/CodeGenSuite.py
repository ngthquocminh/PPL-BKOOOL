import unittest
from TestUtils import TestCodeGen
from AST import *


    
class CheckCodeGenSuite(unittest.TestCase):
    def test_simple_program_00(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [StringLiteral("Hi")])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi"
        self.assertTrue(TestCodeGen.test(input, expect, 500))

    def test_simple_program_01(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [],
                        [
                            CallStmt(Id("io"), Id("writeFloat"),
                                    [FloatLiteral(1.2e-1)])
                        ]
                    )
                )
            ])
        ])
        expect = "0.12"
        self.assertTrue(TestCodeGen.test(input, expect, 501))
        
    def test_simple_program_02(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            ConstDecl(Id("i"),IntType(), IntLiteral(5))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeInt"),
                                    [Id("i")])
                        ]
                    )
                )
            ])
        ])
        expect = "5"
        self.assertTrue(TestCodeGen.test(input, expect, 502))
    
    def test_simple_program_03(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            ConstDecl(Id("i"),StringType(), StringLiteral("Hello, World!"))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [Id("i")])
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!"
        self.assertTrue(TestCodeGen.test(input, expect, 503))

    def test_simple_program_04(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("i"),BoolType(), BooleanLiteral(True))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeBool"),
                                    [Id("i")])
                        ]
                    )
                )
            ])
        ])
        expect = "true"
        self.assertTrue(TestCodeGen.test(input, expect, 504))
        
    def test_simple_program_05(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("i"),BoolType(), BooleanLiteral(True)),
                            VarDecl(Id("j"),StringType(), StringLiteral("Minh")),
                        ],
                        [
                            CallStmt(Id("io"), Id("writeBoolLn"),[Id("i")]),
                            CallStmt(Id("io"), Id("writeStr"),[Id("j")])
                        ]
                    )
                )
            ])
        ])
        expect = "true\nMinh"
        self.assertTrue(TestCodeGen.test(input, expect, 505))
        
    def test_simple_program_06(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("i"),BoolType(), BooleanLiteral(True)),
                            ConstDecl(Id("j"),StringType(), StringLiteral("Minh")),
                        ],
                        [
                            CallStmt(Id("io"), Id("writeBoolLn"),[Id("i")]),
                            CallStmt(Id("io"), Id("writeStr"),[Id("j")])
                        ]
                    )
                )
            ])
        ])
        expect = "true\nMinh"
        self.assertTrue(TestCodeGen.test(input, expect, 506))
        
    def test_simple_program_07(self):
        input = Program([
            ClassDecl(Id("A"),[
            ]),
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("a"),ClassType(Id("A")),NewExpr(Id("A"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [StringLiteral("Hi")])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi"
        self.assertTrue(TestCodeGen.test(input, expect, 507))
        
    def test_simple_program_08(self):
        input = Program([
            ClassDecl(Id("A"),[
                AttributeDecl(Instance(),VarDecl(Id('text'),StringType(),StringLiteral("Hi")))
            ]),
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("a"),ClassType(Id("A")),NewExpr(Id("A"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("a"),Id("text"))])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi"
        self.assertTrue(TestCodeGen.test(input, expect, 508))

    def test_simple_program_09(self):
        input = Program([
            ClassDecl(Id("A"),[
                AttributeDecl(Instance(),VarDecl(Id('enabled'),BoolType(),BooleanLiteral(True))),
                AttributeDecl(Static(),VarDecl(Id('val'),FloatType(),FloatLiteral(1.5)))
            ]),
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("a"),ClassType(Id("A")),NewExpr(Id("A"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(Id("a"),Id("enabled"))]),
                            CallStmt(Id("io"), Id("writeFloat"),
                                    [FieldAccess(Id("A"),Id("val"))])
                        ]
                    )
                )
            ])
        ])
        expect = "true\n1.5"
        self.assertTrue(TestCodeGen.test(input, expect, 509))

    def test_simple_program_10(self):
        input = Program([
            ClassDecl(Id("A"),[
                AttributeDecl(Instance(),ConstDecl(Id('enabled'),BoolType(),BooleanLiteral(False))),
                AttributeDecl(Static(),ConstDecl(Id('val'),FloatType(),FloatLiteral(0.123)))
            ]),
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("a"),ClassType(Id("A")),NewExpr(Id("A"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(Id("a"),Id("enabled"))]),
                            CallStmt(Id("io"), Id("writeFloat"),
                                    [FieldAccess(Id("A"),Id("val"))])
                        ]
                    )
                )
            ])
        ])
        expect = "false\n0.123"
        self.assertTrue(TestCodeGen.test(input, expect, 510))  

    def test_simple_program_11(self):
        input = Program([
            ClassDecl(Id("A"),[
                AttributeDecl(Instance(),ConstDecl(Id('enabled'),BoolType(),BooleanLiteral(False))),
                AttributeDecl(Instance(),VarDecl(Id('val'),FloatType(),FloatLiteral(1.5)))
            ]),
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            ConstDecl(Id("a"),ClassType(Id("A")),NewExpr(Id("A"),[])),
                        ],
                        [
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(Id("a"),Id("enabled"))]),
                            CallStmt(Id("io"), Id("writeFloat"),
                                    [FieldAccess(Id("a"),Id("val"))])
                        ]
                    )
                )
            ])
        ])
        expect = "false\n1.5"
        self.assertTrue(TestCodeGen.test(input, expect, 511))   

    def test_simple_program_12(self):
        input = Program([
            ClassDecl(Id("A"),[
                AttributeDecl(Instance(),ConstDecl(Id('enabled'),BoolType(),BooleanLiteral(False))),
                AttributeDecl(Instance(),VarDecl(Id('val'),FloatType(),FloatLiteral(1.5)))
            ]),
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            ConstDecl(Id("a"),ClassType(Id("A")),NewExpr(Id("A"),[])),
                            VarDecl(Id("b"),ClassType(Id("A")),NewExpr(Id("A"),[])),
                        ],
                        [
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(Id("a"),Id("enabled"))]),
                            CallStmt(Id("io"), Id("writeFloatLn"),
                                    [FieldAccess(Id("b"),Id("val"))]),
                            CallStmt(Id("io"), Id("writeFloat"),
                                    [FieldAccess(Id("a"),Id("val"))]),
                        ]
                    )
                )
            ])
        ])
        expect = "false\n1.5\n1.5"
        self.assertTrue(TestCodeGen.test(input, expect, 512))    
        
    def test_simple_program_13(self):
        input = Program([
            ClassDecl(Id("A"),[
                AttributeDecl(Instance(),ConstDecl(Id('enabled'),BoolType(),BooleanLiteral(False))),
                AttributeDecl(Instance(),VarDecl(Id('val'),FloatType(),FloatLiteral(1.5))),
                AttributeDecl(Static(),VarDecl(Id('name'),StringType(),StringLiteral("Hello"))),
                AttributeDecl(Instance(),ConstDecl(Id('num'),IntType(),IntLiteral(111))),
            ]),
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            ConstDecl(Id("a"),ClassType(Id("A")),NewExpr(Id("A"),[])),
                            VarDecl(Id("b"),ClassType(Id("A")),NewExpr(Id("A"),[])),
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStrLn"),
                                    [FieldAccess(Id("A"),Id("name"))]),
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(Id("a"),Id("enabled"))]),
                            CallStmt(Id("io"), Id("writeIntLn"),
                                    [FieldAccess(Id("b"),Id("num"))]),
                            CallStmt(Id("io"), Id("writeFloat"),
                                    [FieldAccess(Id("a"),Id("val"))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello\nfalse\n111\n1.5"
        self.assertTrue(TestCodeGen.test(input, expect, 513))  

    def test_simple_program_514(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Static(),VarDecl(Id("says"),StringType(),StringLiteral("Hi"))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("BKoolClass"),Id("says"))])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi"
        self.assertTrue(TestCodeGen.test(input, expect, 514)) 
        
    def test_simple_program_515(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Static(),VarDecl(Id("says"),StringType(),StringLiteral("Hi"))),
                AttributeDecl(Instance(),VarDecl(Id("name"),StringType(),StringLiteral("Bkool"))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bkool"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[])),
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("BKoolClass"),Id("says"))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [StringLiteral(", ")]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("bkool"),Id("name"))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hi, Bkool"
        self.assertTrue(TestCodeGen.test(input, expect, 515)) 

    def test_simple_program_516(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),ConstDecl(Id("hello"),StringType(), StringLiteral("Hello, World!"))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bk"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("bk"),Id("hello"))])
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!"
        self.assertTrue(TestCodeGen.test(input, expect, 516))    
        
    def test_simple_program_517(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),ConstDecl(Id("hello1"),StringType(), StringLiteral("Hello"))),
                AttributeDecl(Static(),ConstDecl(Id("hello2"),StringType(), StringLiteral(", "))),
                AttributeDecl(Instance(),VarDecl(Id("hello3"),StringType(), StringLiteral("World"))),
                AttributeDecl(Static(),VarDecl(Id("hello4"),StringType(), StringLiteral("!"))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bk"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("bk"),Id("hello1"))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("BKoolClass"),Id("hello2"))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("bk"),Id("hello3"))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [FieldAccess(Id("BKoolClass"),Id("hello4"))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!"
        self.assertTrue(TestCodeGen.test(input, expect, 517))    

    def test_simple_program_519(self):
        input = Program([
            ClassDecl(Id("A"),[]),
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arr"),ClassType(Id("A")))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [StringLiteral("Hi")])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi"
        self.assertTrue(TestCodeGen.test(input, expect, 519)) 

    def test_simple_program_520(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arr"),ArrayType(3,IntType()))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [StringLiteral("Hi")])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi"
        self.assertTrue(TestCodeGen.test(input, expect, 520))   
        
    def test_simple_program_521(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arr"),ArrayType(3,IntType()))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeInt"),
                                    [ArrayCell(Id("arr"),IntLiteral(1))])
                        ]
                    )
                )
            ])
        ])
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 521))  
        
    def test_simple_program_522(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arr"),ArrayType(3,IntType()),ArrayLiteral([IntLiteral(5),IntLiteral(4),IntLiteral(3)]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeInt"),
                                    [ArrayCell(Id("arr"),IntLiteral(1))])
                        ]
                    )
                )
            ])
        ])
        expect = "4"
        self.assertTrue(TestCodeGen.test(input, expect, 522)) 
        
    def test_simple_program_523(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arr"),ArrayType(3,StringType()),ArrayLiteral([StringLiteral("Hello, "),StringLiteral("World"),StringLiteral("!")]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(Id("arr"),IntLiteral(0))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(Id("arr"),IntLiteral(1))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(Id("arr"),IntLiteral(2))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!"
        self.assertTrue(TestCodeGen.test(input, expect, 523)) 
    
    def test_simple_program_524(self):
        input = Program([
            ClassDecl(Id("A"),[
                AttributeDecl(Instance(),ConstDecl(Id('enabled'),BoolType(),BooleanLiteral(False))),
                AttributeDecl(Instance(),VarDecl(Id('val'),FloatType(),FloatLiteral(1.5)))
            ]),
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),ConstDecl(Id('a1'),ClassType(Id("A")),NewExpr(Id("A"),[]))),
                AttributeDecl(Static(),ConstDecl(Id('a2'),ClassType(Id("A")),NewExpr(Id("A"),[]))),
                AttributeDecl(Instance(),VarDecl(Id('a3'),ClassType(Id("A")),NewExpr(Id("A"),[]))),
                AttributeDecl(Static(),VarDecl(Id('a4'),ClassType(Id("A")),NewExpr(Id("A"),[]))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            ConstDecl(Id("a"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[])),
                        ],
                        [
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(FieldAccess(Id("a"),Id("a1")),Id("enabled"))]),
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(FieldAccess(Id("BKoolClass"),Id("a2")),Id("enabled"))]),
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(FieldAccess(Id("a"),Id("a3")),Id("enabled"))]),
                            CallStmt(Id("io"), Id("writeBoolLn"),
                                    [FieldAccess(FieldAccess(Id("BKoolClass"),Id("a2")),Id("enabled"))]),
                        ]
                    )
                )
            ])
        ])
        expect = "false\nfalse\nfalse\nfalse\n"
        self.assertTrue(TestCodeGen.test(input, expect, 524))   
        
    def test_simple_program_530(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),VarDecl(Id("arr"),ArrayType(3,IntType()))), #ArrayLiteral([StringLiteral("Hello, "),StringLiteral("World"),StringLiteral("!")]
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [ ],
                        [ ]
                    )
                )
            ])
        ])
        expect = ""
        self.assertTrue(TestCodeGen.test(input, expect, 530))          

    def test_simple_program_531(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),VarDecl(Id("arr"),ArrayType(3,IntType()))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bkool"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeInt"),
                                    [ArrayCell(FieldAccess(Id("bkool"),Id("arr")),IntLiteral(0))]),
                        ]
                    )
                )
            ])
        ])
        expect = "0"
        self.assertTrue(TestCodeGen.test(input, expect, 531))  
        
    def test_simple_program_532(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),VarDecl(Id("arr"),ArrayType(3,IntType()),ArrayLiteral([IntLiteral(32),IntLiteral(55),IntLiteral(-23)]))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bkool"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeInt"),
                                    [ArrayCell(FieldAccess(Id("bkool"),Id("arr")),IntLiteral(2))]),
                        ]
                    )
                )
            ])
        ])
        expect = "-23"
        self.assertTrue(TestCodeGen.test(input, expect, 532))  
        
    def test_simple_program_533(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),VarDecl(Id("arr"),ArrayType(3,StringType()), ArrayLiteral([StringLiteral("Hello, "),StringLiteral("World"),StringLiteral("!")]))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bkool"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[]))
                        ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(FieldAccess(Id("bkool"),Id("arr")),IntLiteral(0))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(FieldAccess(Id("bkool"),Id("arr")),IntLiteral(1))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(FieldAccess(Id("bkool"),Id("arr")),IntLiteral(2))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!"
        self.assertTrue(TestCodeGen.test(input, expect, 533))  

    def test_simple_program_534(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Static(),VarDecl(Id("arr"),ArrayType(3,StringType()), ArrayLiteral([StringLiteral("Hello, "),StringLiteral("World"),StringLiteral("!")]))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [ ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(FieldAccess(Id("BKoolClass"),Id("arr")),IntLiteral(0))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(FieldAccess(Id("BKoolClass"),Id("arr")),IntLiteral(1))]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(FieldAccess(Id("BKoolClass"),Id("arr")),IntLiteral(2))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!"
        self.assertTrue(TestCodeGen.test(input, expect, 534))          

    def test_simple_program_540(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("i"),IntType(), IntLiteral(1))
                        ],
                        [
                            Assign(Id("i"),IntLiteral("5")),
                            CallStmt(Id("io"), Id("writeInt"),
                                    [Id("i")])
                        ]
                    )
                )
            ])
        ])
        expect = "5"
        self.assertTrue(TestCodeGen.test(input, expect, 540))
    
    def test_simple_program_541(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("i"),IntType(), IntLiteral(1)),
                            VarDecl(Id("s"),StringType(), StringLiteral("Hello")),
                        ],
                        [
                            Assign(Id("i"),IntLiteral("100000")),
                            Assign(Id("s"),StringLiteral("Hello, World!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")),
                            CallStmt(Id("io"), Id("writeIntLn"),
                                    [Id("i")]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [Id("s")]),
                        ]
                    )
                )
            ])
        ])
        expect = "100000\nHello, World!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        self.assertTrue(TestCodeGen.test(input, expect, 541))
        
    def test_simple_program_541(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("i"),IntType()),
                            VarDecl(Id("s"),StringType()),
                        ],
                        [
                            Assign(Id("i"),IntLiteral("100000")),
                            Assign(Id("s"),StringLiteral("Hello, World!")),
                            CallStmt(Id("io"), Id("writeIntLn"),
                                    [Id("i")]),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [Id("s")]),
                        ]
                    )
                )
            ])
        ])
        expect = "100000\nHello, World!"
        self.assertTrue(TestCodeGen.test(input, expect, 542))
        
    def test_simple_program_543(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arrr"),ArrayType(10, StringType())),
                            # VarDecl(Id("s"),StringType()),
                        ],
                        [
                            # Assign(Id("s"),StringLiteral("Hello, World!")),
                            Assign(ArrayCell(Id("arrr"),IntLiteral(1)),StringLiteral("Hello, World!")),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(Id("arrr"),IntLiteral(1))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!"
        self.assertTrue(TestCodeGen.test(input, expect, 543))
        
    def test_simple_program_544(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arrr"),ArrayType(10, StringType())),
                            VarDecl(Id("s"),StringType(),StringLiteral("Hello, World!!")),
                        ],
                        [
                            # Assign(Id("s"),StringLiteral("Hello, World!")),
                            Assign(ArrayCell(Id("arrr"),IntLiteral(1)),Id("s")),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(Id("arrr"),IntLiteral(1))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!!"
        self.assertTrue(TestCodeGen.test(input, expect, 544))
        
    def test_simple_program_545(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arrr"),ArrayType(10, StringType())),
                            ConstDecl(Id("s"),StringType(),StringLiteral("Hello, World!!")),
                        ],
                        [
                            # Assign(Id("s"),StringLiteral("Hello, World!")),
                            Assign(ArrayCell(Id("arrr"),IntLiteral(1)),Id("s")),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(Id("arrr"),IntLiteral(1))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!!"
        self.assertTrue(TestCodeGen.test(input, expect, 545))

    def test_simple_program_546(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("arrr"),ArrayType(10, StringType())),
                            VarDecl(Id("s"),StringType()),
                        ],
                        [
                            Assign(Id("s"),StringLiteral("Hello, World!!")),
                            Assign(ArrayCell(Id("arrr"),IntLiteral(1)),Id("s")),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(Id("arrr"),IntLiteral(1))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!!"
        self.assertTrue(TestCodeGen.test(input, expect, 546))
    
    def test_simple_program_550(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),VarDecl(Id("hi"),StringType(),StringLiteral("Hi!"))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bk"),ClassType(Id("BKoolClass")))
                        ],
                        [
                            Assign(Id("bk"),NewExpr(Id("BKoolClass"),[])),
                            CallStmt(Id("io"),Id("writeStr"),[FieldAccess(Id("bk"),Id("hi"))])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi!"
        self.assertTrue(TestCodeGen.test(input, expect, 550))          

    def test_simple_program_551(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),ConstDecl(Id("hi"),StringType(),StringLiteral("Hi!"))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bk"),ClassType(Id("BKoolClass")))
                        ],
                        [
                            Assign(Id("bk"),NewExpr(Id("BKoolClass"),[])),
                            CallStmt(Id("io"),Id("writeStr"),[FieldAccess(Id("bk"),Id("hi"))])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi!"
        self.assertTrue(TestCodeGen.test(input, expect, 551))
        
    def test_simple_program_552(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),VarDecl(Id("hi"),StringType(),StringLiteral("Hi!"))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bk"),ClassType(Id("BKoolClass")))
                        ],
                        [
                            Assign(Id("bk"),NewExpr(Id("BKoolClass"),[])),
                            Assign(FieldAccess(Id("bk"),Id("hi")),StringLiteral("Hi, Minh!")),
                            CallStmt(Id("io"),Id("writeStr"),[FieldAccess(Id("bk"),Id("hi"))])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi, Minh!"
        self.assertTrue(TestCodeGen.test(input, expect, 552))

     
    def test_simple_program_553(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Static(),VarDecl(Id("hi"),StringType(),StringLiteral("Hi!"))),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("s"),StringType(),StringLiteral("Quoc Minh"))
                        ],
                        [
                            Assign(FieldAccess(Id("BKoolClass"),Id("hi")),StringLiteral("Hi, Minh!")),
                            CallStmt(Id("io"),Id("writeStr"),[FieldAccess(Id("BKoolClass"),Id("hi"))])
                        ]
                    )
                )
            ])
        ])
        expect = "Hi, Minh!"
        self.assertTrue(TestCodeGen.test(input, expect, 553))

    def test_simple_program_560(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),VarDecl(Id("arrr"),ArrayType(10, StringType()))),
                # AttributeDecl(Instance(),VarDecl(Id("s"),StringType())),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bk"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[]))
                        ],
                        [
                            # Assign(Id("s"),StringLiteral("Hello, World!!")),
                            Assign(ArrayCell(FieldAccess(Id("bk"),Id("arrr")),IntLiteral(1)),StringLiteral("Hello, World!!!!")),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(FieldAccess(Id("bk"),Id("arrr")),IntLiteral(1))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!!!!"
        self.assertTrue(TestCodeGen.test(input, expect, 560))

    def test_simple_program_561(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                AttributeDecl(Instance(),VarDecl(Id("arrr"),ArrayType(10, StringType()))),
                # AttributeDecl(Instance(),VarDecl(Id("s"),StringType())),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [
                            VarDecl(Id("bk"),ClassType(Id("BKoolClass")),NewExpr(Id("BKoolClass"),[])),
                            VarDecl(Id("s"),StringType()),
                        ],
                        [
                            Assign(Id("s"),StringLiteral("Hello, World!!!!!")),
                            Assign(ArrayCell(FieldAccess(Id("bk"),Id("arrr")),IntLiteral(1)),Id("s")),
                            CallStmt(Id("io"), Id("writeStr"),
                                    [ArrayCell(FieldAccess(Id("bk"),Id("arrr")),IntLiteral(1))]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello, World!!!!!"
        self.assertTrue(TestCodeGen.test(input, expect, 561))

    def test_simple_program_562(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(Static(), Id("foo"),[],VoidType(),Block([],[
                    CallStmt(Id("io"), Id("writeStr"), [StringLiteral("Hello!")])    
                ])),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [ ],
                        [
                            CallStmt(Id("BKoolClass"), Id("foo"),[]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello!"
        self.assertTrue(TestCodeGen.test(input, expect, 562))

    def test_simple_program_563(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(Static(), Id("says"),[],StringType(),Block([],[
                    Return(StringLiteral("Hello!"))
                ])),
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [ ],
                        [
                            CallStmt(Id("io"), Id("writeStr"),[CallExpr(Id("BKoolClass"),Id("says"),[])]),
                        ]
                    )
                )
            ])
        ])
        expect = "Hello!"
        self.assertTrue(TestCodeGen.test(input, expect, 563))



    def test_simple_program_564(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [ ],
                        [
                            If(BooleanLiteral(True),CallStmt(Id("io"), Id("writeStr"),[StringLiteral("Hello!!")]))
                            
                        ]
                    )
                )
            ])
        ])
        expect = "Hello!!"
        self.assertTrue(TestCodeGen.test(input, expect, 564))

    def test_simple_program_565(self):
        input = Program([
            ClassDecl(Id("BKoolClass"),[
                MethodDecl(
                    Static(), Id("main"), [], VoidType(),
                    Block(
                        [ ],
                        [
                            If(BooleanLiteral(True),CallStmt(Id("io"), Id("writeStr"),[StringLiteral("Hello!!")]))
                            
                        ]
                    )
                )
            ])
        ])
        expect = "Hello!!"
        self.assertTrue(TestCodeGen.test(input, expect, 565))




    # def test_simple_program_12(self):
    #     input = Program([
    #         ClassDecl(Id("B"),[
    #             AttributeDecl(Instance(),VarDecl(Id('a'),ClassType(Id("A")),NewExpr(Id("A"),[])))
    #         ]),            
    #         ClassDecl(Id("A"),[
    #             AttributeDecl(Instance(),ConstDecl(Id('enabled'),BoolType(),BooleanLiteral(False))),
    #             AttributeDecl(Static(),ConstDecl(Id('val'),FloatType(),FloatLiteral(1.5)))
    #         ]),
    #         ClassDecl(Id("BKoolClass"),[
    #             MethodDecl(
    #                 Static(), Id("main"), [], VoidType(),
    #                 Block(
    #                     [
    #                         VarDecl(Id("b"),ClassType(Id("B")),NewExpr(Id("B"),[]))
    #                     ],
    #                     [
    #                         CallStmt(Id("io"), Id("writeBoolLn"),
    #                                 [FieldAccess(FieldAccess(Id("b"),Id("a")),Id("enabled"))]),
    #                         CallStmt(Id("io"), Id("writeFloat"),
    #                                 [FieldAccess(FieldAccess(Id("b"),Id("a")),Id("val"))])
    #                     ]
    #                 )
    #             )
    #         ])
    #     ])
    #     expect = "false\n1.5"
    #     self.assertTrue(TestCodeGen.test(input, expect, 512))        

    # def test_simple_program_08(self):
    #     input = Program([
    #         ClassDecl(Id("A"),[
    #             ConstDecl(Id('hi'),StringType(),StringLiteral("Hi"))
    #         ]),
    #         ClassDecl(Id("BKoolClass"),[
    #             MethodDecl(
    #                 Static(), Id("main"), [], VoidType(),
    #                 Block(
    #                     [
    #                         VarDecl(Id("a"),ClassType(Id("A")),NewExpr(Id("A"),[]))
    #                     ],
    #                     [
    #                         CallStmt(Id("io"), Id("writeStr"),
    #                                 [FieldAccess(Id("a"),Id("hi"))])
    #                     ]
    #                 )
    #             )
    #         ])
    #     ])
    #     expect = "Hi"
    #     self.assertTrue(TestCodeGen.test(input, expect, 508))