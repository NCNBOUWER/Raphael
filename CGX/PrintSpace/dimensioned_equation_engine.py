"""CGX PrintSpace v0.4: dimensioned deterministic equation baselines.

Read-only, no hardware access. Input values MUST already be in declared SI
units. Not a full multiphysics solver, not a material qualification, and not
a replacement for the UTP kernel owners or physical test evidence.
"""
from __future__ import annotations

import ast
from fractions import Fraction
import json
import math
from pathlib import Path

ZERO = (Fraction(0),) * 7
def dim(*components):
    return tuple(Fraction(x) for x in components)
def add(a,b):
    return tuple(x+y for x,y in zip(a,b))
def neg(a):
    return tuple(-x for x in a)
def scale(a,n):
    return tuple(x*n for x in a)
SI = {
    "kg":dim(1,0,0,0,0,0,0),"m":dim(0,1,0,0,0,0,0),
    "s":dim(0,0,1,0,0,0,0),"A":dim(0,0,0,1,0,0,0),
    "K":dim(0,0,0,0,1,0,0),"mol":dim(0,0,0,0,0,1,0),
    "cd":dim(0,0,0,0,0,0,1),"rad":ZERO,
    "N":dim(1,1,-2,0,0,0,0),"Pa":dim(1,-1,-2,0,0,0,0),
    "J":dim(1,2,-2,0,0,0,0),"W":dim(1,2,-3,0,0,0,0),
    "C":dim(0,0,1,1,0,0,0),"V":dim(1,2,-3,-1,0,0,0),
    "Ohm":dim(1,2,-3,-2,0,0,0),"F":dim(-1,-2,4,2,0,0,0),
    "H":dim(1,2,-2,-2,0,0,0),"T":dim(1,0,-2,-1,0,0,0),
    "Wb":dim(1,2,-2,-1,0,0,0),"Hz":dim(0,0,-1,0,0,0,0),
    "S":dim(-1,-2,3,2,0,0,0),
}
FUNCTIONS = {
    "sqrt":math.sqrt,"exp":math.exp,"cos":math.cos,
    "abs":abs,
}

def dimensional_ast(node, symbols):
    """Evaluate dimensions; reject all unsupported AST syntax."""
    if isinstance(node, ast.Expression):
        return dimensional_ast(node.body, symbols)
    if isinstance(node, ast.Constant) and type(node.value) in (int,float):
        if not math.isfinite(node.value):
            raise ValueError("Nonfinite number in expression")
        return ZERO
    if isinstance(node, ast.Name):
        if node.id not in symbols:
            raise ValueError("Unrecognised symbol: " + node.id)
        return symbols[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op,(ast.USub,ast.UAdd)):
        return dimensional_ast(node.operand,symbols)
    if isinstance(node, ast.BinOp):
        a=dimensional_ast(node.left,symbols)
        b=dimensional_ast(node.right,symbols)
        if isinstance(node.op,(ast.Add,ast.Sub)):
            if a!=b:
                raise ValueError("Dimensional mismatch in addition/subtraction")
            return a
        if isinstance(node.op,ast.Mult):
            return add(a,b)
        if isinstance(node.op,ast.Div):
            return add(a,neg(b))
        if isinstance(node.op,ast.Pow):
            if b!=ZERO:
                raise ValueError("Dimensional exponent prohibited")
            n=constant_number(node.right)
            return scale(a,Fraction(str(n)).limit_denominator(1000))
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
        if len(node.args)!=1 or node.keywords:
            raise ValueError("Only single-argument permitted functions")
        a=dimensional_ast(node.args[0],symbols)
        if node.func.id=="sqrt":
            return scale(a,Fraction(1,2))
        if node.func.id in ("exp","cos"):
            if a!=ZERO:
                raise ValueError("Exponential/trigonometric argument must be dimensionless")
            return ZERO
        if node.func.id=="abs":
            return a
    raise ValueError("Unsupported or unsafe expression syntax")

def constant_number(node):
    if isinstance(node,ast.Constant) and type(node.value) in (float,int):
        return node.value
    if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):
        return -constant_number(node.operand)
    raise ValueError("Exponent must be literal numeric constant")

def unit_dimensions(unit):
    if unit=="1":
        return ZERO
    return dimensional_ast(ast.parse(unit,mode="eval"),SI)

def numerical_ast(node, values):
    if isinstance(node,ast.Expression):
        return numerical_ast(node.body,values)
    if isinstance(node,ast.Constant) and type(node.value) in (int,float):
        return float(node.value)
    if isinstance(node,ast.Name):
        return values[node.id]
    if isinstance(node,ast.UnaryOp):
        x=numerical_ast(node.operand,values)
        if isinstance(node.op,ast.USub):
            return -x
        if isinstance(node.op,ast.UAdd):
            return x
    if isinstance(node,ast.BinOp):
        a=numerical_ast(node.left,values);b=numerical_ast(node.right,values)
        if isinstance(node.op,ast.Add):
            return a+b
        if isinstance(node.op,ast.Sub):
            return a-b
        if isinstance(node.op,ast.Mult):
            return a*b
        if isinstance(node.op,ast.Div):
            return a/b
        if isinstance(node.op,ast.Pow):
            return a**b
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
        if node.func.id in FUNCTIONS and len(node.args)==1 and not node.keywords:
            return FUNCTIONS[node.func.id](numerical_ast(node.args[0],values))
    raise ValueError("Unsupported numerical operation")

def load_catalogue(path=None):
    path=Path(path) if path else Path(__file__).with_name("PHYSICAL_EQUATION_CATALOGUE_v0_4.json")
    return json.loads(path.read_text(encoding="utf-8"))

def validate_catalogue(catalog):
    eqs=catalog["models"]
    if len(eqs)!=47 or len({x["id"] for x in eqs})!=len(eqs):
        raise ValueError("Expected 47 distinct equation models")
    constants=catalog["constants"]
    for k,data in constants.items():
        if k not in ("pi","c_light","R_gas","F_const","eps0","mu0"):
            raise ValueError("Unexpected constant in registry: "+k)
        if not math.isfinite(data["value"]):
            raise ValueError("Nonfinite physical constant")
        unit_dimensions(data["unit"])
    const_dims={k:unit_dimensions(v["unit"]) for k,v in constants.items()}
    for e in eqs:
        d={k:unit_dimensions(u) for k,u in e["inputs"].items()}
        if set(d)&set(const_dims):
            raise ValueError("Input aliases reserved constants")
        astnode=ast.parse(e["formula"],mode="eval")
        output=dimensional_ast(astnode,{**const_dims,**d})
        expected=unit_dimensions(e["result_unit"])
        if output!=expected:
            raise ValueError(f'{e["id"]} unit mismatch: {output} != {expected}')
        if not e.get("validity") or not e.get("utp_kernel_ids"):
            raise ValueError("Missing physical validity or kernel owner")
        if e.get("production_approved") is not False:
            raise ValueError("Unqualified equations must never assert production approval")
    return True

def evaluate(equation_id,inputs,catalogue=None):
    catalogue=catalogue or load_catalogue()
    validate_catalogue(catalogue)
    equations={e["id"]:e for e in catalogue["models"]}
    if equation_id not in equations:
        raise ValueError("Unknown equation id")
    e=equations[equation_id]
    required=set(e["inputs"])
    if set(inputs)!=required:
        raise ValueError(f"Expected exactly {sorted(required)}, got {sorted(inputs)}")
    for k,v in inputs.items():
        if type(v) not in (float,int) or not math.isfinite(v):
            raise ValueError("Inputs must be finite SI floats/integers")
        if k in ("area","radius","length","thickness","gap","width","diameter","volume","range",
                 "dynamic_viscosity","diffusivity","thermal_conductivity","young_modulus",
                 "internal_resistance","resistance","density_a","density_b","charge_number",
                 "surface_tension","density_difference","permeability"):
            if v<=0:
                raise ValueError("Positive input required: "+k)
        if k in ("efficiency","conversion_efficiency","fraction_a","fraction_b") and not 0<=v<=1:
            raise ValueError("Fraction/efficiency must be in [0,1]")
        if k=="temperature" and v<=0:
            raise ValueError("Absolute temperature must be positive Kelvin")
        if k=="gravity" and v<0:
            raise ValueError("Gravity magnitude cannot be negative")
    if equation_id=="PS-EQ-046" and inputs["gravity"]==0:
        raise ValueError("Capillary length diverges at g=0; use force balance instead")
    constants={k:v["value"] for k,v in catalogue["constants"].items()}
    result=numerical_ast(ast.parse(e["formula"],mode="eval"),{**constants,**inputs})
    if isinstance(result,complex) or not math.isfinite(result):
        raise ValueError("Equation yielded invalid or nonfinite result")
    return {
        "equation_id":equation_id,"value":result,"unit":e["result_unit"],
        "validity_required":e["validity"],
        "evidence_state":"ANALYTIC_IDENTITY_NO_PHYSICAL_VALIDATION",
        "production_approved":False,
    }

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--equation",required=True)
    parser.add_argument("--inputs-json",required=True,help="JSON object of SI input values")
    a=parser.parse_args()
    print(json.dumps(evaluate(a.equation,json.loads(a.inputs_json)),indent=2))
