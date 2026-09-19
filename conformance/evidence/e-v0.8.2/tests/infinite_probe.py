import os,sys
C=os.environ['E_V082_C_ROOT'];sys.path.insert(0,C)
from compiler.api import compile_source
s=open(sys.argv[2],encoding='utf8').read();c=compile_source(s);assert c.valid
layer=sys.argv[1]
if layer=='hast':
 from compiler.runtime.reference import execute_reference;o=execute_reference(c.hast)
elif layer=='ir':
 from compiler.runtime.ir_reference import execute_reference_ir;o=execute_reference_ir(c.ir)
else:
 from compiler.backend.portable import execute_ir;o=execute_ir(c.ir)
print(type(o).__name__,getattr(o,'category',None))
