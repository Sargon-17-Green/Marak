import os,sys
C=os.environ['E_V082_C_ROOT'];E=os.environ['E_V082_E08_ROOT'];sys.path[:0]=[C,E+'/tools']
from test_v082_final import deep
from compiler.api import compile_source
from compiler.runtime.reference import execute_reference
from compiler.runtime.ir_reference import execute_reference_ir
from compiler.backend.portable import execute_ir
c=compile_source(deep(1000));assert c.valid;sys.setrecursionlimit(80)
print(type(execute_reference(c.hast)).__name__,type(execute_reference_ir(c.ir)).__name__,type(execute_ir(c.ir)).__name__)
