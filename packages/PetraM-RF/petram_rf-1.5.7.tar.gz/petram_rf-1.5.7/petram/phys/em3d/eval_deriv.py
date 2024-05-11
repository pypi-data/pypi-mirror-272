'''

  evaulate derivative of Nedelec element using
  DiscreteLinearOperator

'''
from petram.mfem_config import use_parallel
import petram.debug
dprint1, dprint2, dprint3 = petram.debug.init_dprints('eval_deriv')

if use_parallel:
   import mfem.par as mfem
   FiniteElementSpace = mfem.ParFiniteElementSpace
   DiscreteLinearOperator = mfem.ParDiscreteLinearOperator
   GridFunction = mfem.ParGridFunction
else:
   import mfem.ser as mfem
   FiniteElementSpace = mfem.FiniteElementSpace
   DiscreteLinearOperator = mfem.DiscreteLinearOperator
   GridFunction = mfem.GridFunction

def eval_curl(gfr, gfi = None):
    fes = gfr.FESpace()
    ordering = fes.GetOrdering()
    mesh = fes.GetMesh()
    vdim = 1
    sdim = mesh.SpaceDimension()
    p = fes.GetOrder(0)
    rt_coll = mfem.RT_FECollection(p-1, sdim)

    rts = FiniteElementSpace(mesh,  rt_coll, vdim, ordering)

    
    curl = DiscreteLinearOperator(fes, rts)
    itp = mfem.CurlInterpolator()
    curl.AddDomainInterpolator(itp)
    curl.Assemble();
    curl.Finalize();

    br   = GridFunction(rts)    
    curl.Mult(gfr,  br)
    if gfi is not None:
       bi = GridFunction(rts)           
       curl.Mult(gfi,  bi)
    else:
       bi = None
    ### needs to return rts to prevent rts to be collected.
    return br, bi,  rts


