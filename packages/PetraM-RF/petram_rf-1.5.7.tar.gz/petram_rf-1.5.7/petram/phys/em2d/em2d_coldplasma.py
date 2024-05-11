'''
   Anistropic media:
      However, can have arbitrary scalar epsilon_r, mu_r, sigma

    Expansion of matrix is as follows

               [e_xy  e_12 ][Exy ]
[Wxy, Wz]   =  [           ][    ] = Wrz e_xy Erz + Wxy e_12 Ez
               [e_21  e_zz][Ez  ]

                                   + Wz e_21 Exy + Wz*e_zz*Exy


  Exy = Ex e_x + Ey e_y
  Ez =  Ez e_z

'''
from petram.phys.common.rf_dispersion_coldplasma import (stix_options,
                                                         default_stix_option,
                                                         vtable_data0,)

from petram.phys.em2d.em2d_base import EM2D_Bdry, EM2D_Domain, EM2D_Domain_helper
from petram.phys.phys_const import mu0, epsilon0
from petram.phys.vtable import VtableElement, Vtable
from petram.mfem_config import use_parallel
import numpy as np

import petram.debug as debug
dprint1, dprint2, dprint3 = debug.init_dprints('EM2D_ColdPlasma')

if use_parallel:
    import mfem.par as mfem
else:
    import mfem.ser as mfem

vtable_data = vtable_data0.copy()
vtable_data.extend([('kz', VtableElement('kz', type='float',
                                         guilabel='kz',
                                         default=0.0,
                                         no_func=True,
                                         tip="out-of-plane wave number")), ])


def domain_constraints():
    return [EM2D_ColdPlasma]


class EM2D_ColdPlasma(EM2D_Domain, EM2D_Domain_helper):
    vt = Vtable(vtable_data)
    # nlterms = ['epsilonr']

    def get_possible_child(self):
        from .em2d_pml import EM2D_LinearPML
        return [EM2D_LinearPML]

    def has_bf_contribution(self, kfes):
        if kfes == 0:
            return True
        elif kfes == 1:
            return True
        else:
            return False

    def has_mixed_contribution(self):
        return True

    def get_mixedbf_loc(self):
        '''
        r, c, and flag1, flag2 of MixedBilinearForm
           flag1 : take transpose
           flag2 : take conj
        '''
        return [(0, 1, 1, 1), (1, 0, 1, 1), ]  # (0, 1, -1, 1)]

    def attribute_set(self, v):
        EM2D_Domain.attribute_set(self, v)
        v["stix_terms"] = default_stix_option
        return v

    def config_terms(self, evt):
        from petram.phys.common.rf_stix_terms_panel import ask_rf_stix_terms

        self.vt.preprocess_params(self)
        _B, _dens_e, _t_e, _dens_i, _masses, charges, _kz = self.vt.make_value_or_expression(
            self)

        num_ions = len(charges)
        win = evt.GetEventObject()
        value = ask_rf_stix_terms(win, num_ions, self.stix_terms)
        self.stix_terms = value

    def stix_terms_txt(self):
        return self.stix_terms

    def panel1_param(self):
        panels = super(EM2D_ColdPlasma, self).panel1_param()
        panels.extend([["Stix terms", "", 2, None],
                       [None, None, 341, {"label": "Customize terms",
                                          "func": "config_terms",
                                          "sendevent": True,
                                          "noexpand": True}], ])
        return panels

    def get_panel1_value(self):
        values = super(EM2D_ColdPlasma, self).get_panel1_value()
        values.extend([self.stix_terms_txt(), self])
        return values

    def import_panel1_value(self, v):
        check = super(EM2D_ColdPlasma, self).import_panel1_value(v[:-2])
        return check

    @ property
    def jited_coeff(self):
        return self._jited_coeff

    def compile_coeffs(self):
        self._jited_coeff = self.get_coeffs()

    def get_coeffs(self):
        freq, omega = self.get_root_phys().get_freq_omega()
        B, dens_e, t_e, dens_i, masses, charges, kz = self.vt.make_value_or_expression(
            self)
        ind_vars = self.get_root_phys().ind_vars

        from petram.phys.common.rf_dispersion_coldplasma import build_coefficients
        coeff1, coeff2, coeff3, coeff4, coeff_nuei = build_coefficients(ind_vars, omega, B, dens_e, t_e,
                                                                        dens_i, masses, charges,
                                                                        self._global_ns, self._local_ns,
                                                                        sdim=2, terms=self.stix_terms)

        return coeff1, coeff2, coeff3, coeff4, coeff_nuei, kz

    def get_coeffs_2(self):
        # e, m, s
        coeff1, coeff2, coeff3, coeff_stix, _coeff_nuei, kz = self.jited_coeff
        '''
        coeff4 = ComplexMatrixSum(
            coeff1, coeff3)      # -> coeff4 = coeff1 + coeff3
        '''
        coeff4 = coeff1 + coeff3

        if self.has_pml():
            coeff4 = self.make_PML_coeff(coeff4)
            coeff2 = self.make_PML_coeff(coeff2)

        eps11 = coeff4[[0, 1], [0, 1]]
        eps21 = coeff4[[0, 1], 2]
        eps12 = coeff4[2, [0, 1]]
        eps22 = coeff4[2, 2]

        eps = [eps11, eps12, eps21, eps22]

        tmp = coeff2.inv()

        mu11 = tmp[[0, 1], [0, 1]]
        mu11 = mu11.adj()
        mu22 = tmp[2, 2]
        k2_over_mu11 = mu11*(kz*kz)
        ik_over_mu11 = mu11*(1j*kz)

        mu = [mu11, mu22, k2_over_mu11, ik_over_mu11]

        return eps, mu, kz

    def add_bf_contribution(self, engine, a, real=True, kfes=0):
        # freq, omega = self.get_root_phys().get_freq_omega()
        eps, mu, kz = self.get_coeffs_2()

        self.set_integrator_realimag_mode(real)

        if real:
            if kfes == 0:
                dprint1("Add ND contribution(real)" + str(self._sel_index))
            elif kfes == 1:
                dprint1("Add H1 contribution(real)" + str(self._sel_index))
        else:
            if kfes == 0:
                dprint1("Add ND contribution(imag)" + str(self._sel_index))
            elif kfes == 1:
                dprint1("Add H1 contribution(imag)" + str(self._sel_index))

        self.call_bf_add_integrator(eps,  mu, kz,  engine, a, kfes)

    def add_mix_contribution(self, engine, mbf, r, c, is_trans, real=True):
        if real:
            dprint1("Add mixed contribution(real)" + "(" + str(r) + "," + str(c) + ')'
                    + str(self._sel_index))
        else:
            dprint1("Add mixed contribution(imag)" + "(" + str(r) + "," + str(c) + ')'
                    + str(self._sel_index))

        # freq, omega = self.get_root_phys().get_freq_omega()
        eps, mu, kz = self.get_coeffs_2()

        self.set_integrator_realimag_mode(real)

        self.call_mix_add_integrator(eps, mu, engine, mbf, r, c, is_trans)

    def add_domain_variables(self, v, n, suffix, ind_vars):
        from petram.helper.variables import add_expression, add_constant

        if len(self._sel_index) == 0:
            return

        freq, omega = self.get_root_phys().get_freq_omega()
        B, dens_e, t_e, dens_i, masses, charges, kz = self.vt.make_value_or_expression(
            self)
        ind_vars = self.get_root_phys().ind_vars

        add_constant(v, 'kz', suffix, np.float64(kz),
                     domains=self._sel_index,
                     gdomain=self._global_ns)

        from petram.phys.common.rf_dispersion_coldplasma import build_variables

        ss = self.parent.parent.name()+'_'+self.name()  # phys module name + name
        var1, var2, var3, var4, var5 = build_variables(v, ss, ind_vars,
                                                       omega, B, dens_e, t_e,
                                                       dens_i, masses, charges,
                                                       self._global_ns, self._local_ns,
                                                       sdim=1, terms=self.stix_terms)

        v["_e_"+ss] = var1
        v["_m_"+ss] = var2
        v["_s_"+ss] = var3
        v["_spd_"+ss] = var4
        v["_nuei_"+ss] = var5

        self.do_add_matrix_expr(v, suffix, ind_vars, 'epsilonr', ["_e_"+ss + "/(-omega*omega*e0)"])
        self.do_add_matrix_expr(v, suffix, ind_vars, 'mur', ["_m_"+ss + "/mu0"])
        self.do_add_matrix_expr(v, suffix, ind_vars, 'sigma', ["_s_"+ss + "/(-1j*omega)"])
        self.do_add_matrix_expr(v, suffix, ind_vars, 'nuei', ["_nuei_"+ss])
        self.do_add_matrix_expr(v, suffix, ind_vars,
                                'Sstix', ["_spd_"+ss+"[0,0]"])
        self.do_add_matrix_expr(v, suffix, ind_vars, 'Dstix', [
                                "1j*_spd_"+ss+"[0,1]"])
        self.do_add_matrix_expr(v, suffix, ind_vars,
                                'Pstix', ["_spd_"+ss+"[2,2]"])

        var = ['x', 'y', 'z']
        self.do_add_matrix_component_expr(v, suffix, ind_vars, var, 'epsilonr')
        self.do_add_matrix_component_expr(v, suffix, ind_vars, var, 'mur')
        self.do_add_matrix_component_expr(v, suffix, ind_vars, var, 'sigma')

        return

