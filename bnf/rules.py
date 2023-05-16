RULES = {
    "1": {
        "var": "Function",
        "rule": [
            "Type",
            "identifier",
            "(",
            "ArgList",
            ")",
            "CompoundStmt"
        ]
    },
    "2": {
        "var": "ArgList",
        "rule": [
            "Arg"
        ]
    },
    "3": {
        "var": "ArgList",
        "rule": [
            ",",
            "Arg",
            "ArgList'"
        ]
    },
    "4": {
        "var": "ArgList'",
        "rule": [
            ",",
            "Arg",
            "ArgList'"
        ]
    },
    "5": {
        "var": "ArgList'",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "6": {
        "var": "Arg",
        "rule": [
            "Type",
            "identifier"
        ]
    },
    "7": {
        "var": "Declaration",
        "rule": [
            "Type",
            "IdentList",
            ";"
        ]
    },
    "8": {
        "var": "Type",
        "rule": [
            "int"
        ]
    },
    "9": {
        "var": "Type",
        "rule": [
            "float"
        ]
    },
    "10": {
        "var": "IdentList",
        "rule": [
            "identifier",
            ",",
            "IdentList"
        ]
    },
    "11": {
        "var": "IdentList",
        "rule": [
            "identifier"
        ]
    },
    "12": {
        "var": "Stmt",
        "rule": [
            "ForStmt"
        ]
    },
    "13": {
        "var": "Stmt",
        "rule": [
            "WhileStmt"
        ]
    },
    "14": {
        "var": "Stmt",
        "rule": [
            "Expr",
            ";"
        ]
    },
    "15": {
        "var": "Stmt",
        "rule": [
            "IfStmt"
        ]
    },
    "16": {
        "var": "Stmt",
        "rule": [
            "CompoundStmt"
        ]
    },
    "17": {
        "var": "Stmt",
        "rule": [
            "Declaration"
        ]
    },
    "18": {
        "var": "Stmt",
        "rule": [
            ";"
        ]
    },
    "19": {
        "var": "ForStmt",
        "rule": [
            "for",
            "(",
            "Expr",
            ";",
            "OptExpr",
            ";",
            "OptExpr",
            ")",
            "Stmt"
        ]
    },
    "20": {
        "var": "OptExpr",
        "rule": [
            "Expr"
        ]
    },
    "21": {
        "var": "OptExpr",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "22": {
        "var": "WhileStmt",
        "rule": [
            "while",
            "(",
            "Expr",
            ")",
            "Stmt"
        ]
    },
    "23": {
        "var": "IfStmt",
        "rule": [
            "if",
            "(",
            "Expr",
            ")",
            "Stmt",
            "ElsePart"
        ]
    },
    "24": {
        "var": "ElsePart",
        "rule": [
            "else",
            "Stmt"
        ]
    },
    "25": {
        "var": "ElsePart",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "26": {
        "var": "CompoundStmt",
        "rule": [
            "{",
            "StmtList",
            "}"
        ]
    },
    "27": {
        "var": "StmtList",
        "rule": [
            "Stmt",
            "StmtList'"
        ]
    },
    "28": {
        "var": "StmtList",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "29": {
        "var": "StmtList'",
        "rule": [
            "Stmt",
            "StmtList'"
        ]
    },
    "30": {
        "var": "StmtList'",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "31": {
        "var": "Expr",
        "rule": [
            "identifier",
            "=",
            "Expr"
        ]
    },
    "32": {
        "var": "Expr",
        "rule": [
            "Rvalue"
        ]
    },
    "33": {
        "var": "Rvalue",
        "rule": [
            "Compare",
            "Mag",
            "Rvalue'"
        ]
    },
    "34": {
        "var": "Rvalue",
        "rule": [
            "Mag"
        ]
    },
    "35": {
        "var": "Rvalue'",
        "rule": [
            "Compare",
            "Mag",
            "Rvalue'"
        ]
    },
    "36": {
        "var": "Rvalue'",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "37": {
        "var": "Compare",
        "rule": [
            "=="
        ]
    },
    "38": {
        "var": "Compare",
        "rule": [
            "<"
        ]
    },
    "39": {
        "var": "Compare",
        "rule": [
            ">"
        ]
    },
    "40": {
        "var": "Compare",
        "rule": [
            "<="
        ]
    },
    "41": {
        "var": "Compare",
        "rule": [
            ">="
        ]
    },
    "42": {
        "var": "Compare",
        "rule": [
            "!="
        ]
    },
    "43": {
        "var": "Mag",
        "rule": [
            "+",
            "Term",
            "Mag'"
        ]
    },
    "44": {
        "var": "Mag",
        "rule": [
            "-",
            "Term",
            "Mag''"
        ]
    },
    "45": {
        "var": "Mag",
        "rule": [
            "Term"
        ]
    },
    "46": {
        "var": "Mag'",
        "rule": [
            "+",
            "Term",
            "Mag'"
        ]
    },
    "47": {
        "var": "Mag'",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "48": {
        "var": "Mag''",
        "rule": [
            "-",
            "Term",
            "Mag''"
        ]
    },
    "49": {
        "var": "Mag''",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "50": {
        "var": "Term",
        "rule": [
            "*",
            "Factor",
            "Term'"
        ]
    },
    "51": {
        "var": "Term",
        "rule": [
            "/",
            "Factor",
            "Term''"
        ]
    },
    "52": {
        "var": "Term",
        "rule": [
            "Factor"
        ]
    },
    "53": {
        "var": "Term'",
        "rule": [
            "*",
            "Factor",
            "Term'"
        ]
    },
    "54": {
        "var": "Term'",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "55": {
        "var": "Term''",
        "rule": [
            "/",
            "Factor",
            "Term''"
        ]
    },
    "56": {
        "var": "Term''",
        "rule": [
            "\u00ce\u00b5"
        ]
    },
    "57": {
        "var": "Factor",
        "rule": [
            "(",
            "Expr",
            ")"
        ]
    },
    "58": {
        "var": "Factor",
        "rule": [
            "-",
            "Factor"
        ]
    },
    "59": {
        "var": "Factor",
        "rule": [
            "+",
            "Factor"
        ]
    },
    "60": {
        "var": "Factor",
        "rule": [
            "identifier"
        ]
    },
    "61": {
        "var": "Factor",
        "rule": [
            "number"
        ]
    }
}