##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018-2020, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################
"""
Pure component properties as used by the NIST WebBook

https://webbook.nist.gov/chemistry/

Retrieved: September 13th, 2019

All parameter indicies and units based on conventions used by the source
"""
from pyomo.environ import log, Var, units as pyunits

from idaes.generic_models.properties.core.generic.utility import \
    set_param_value


# -----------------------------------------------------------------------------
# Shomate Equation for heat capacities, enthalpy and entropy
class cp_mol_ig_comp():

    @staticmethod
    def build_parameters(cobj):
        cobj.cp_mol_ig_comp_coeff_A = Var(
            doc="Shomate A parameter for ideal gas molar heat capacity",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1)
        set_param_value(cobj,
                        param="cp_mol_ig_comp_coeff",
                        units=pyunits.J*pyunits.mol**-1*pyunits.K**-1,
                        index="A")

        cobj.cp_mol_ig_comp_coeff_B = Var(
            doc="Shomate B parameter for ideal gas molar heat capacity",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1*pyunits.kiloK**-1)
        set_param_value(
            cobj,
            param="cp_mol_ig_comp_coeff",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1*pyunits.kiloK**-1,
            index="B")

        cobj.cp_mol_ig_comp_coeff_C = Var(
            doc="Shomate C parameter for ideal gas molar heat capacity",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1*pyunits.kiloK**-2)
        set_param_value(
            cobj,
            param="cp_mol_ig_comp_coeff",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1*pyunits.kiloK**-2,
            index="C")

        cobj.cp_mol_ig_comp_coeff_D = Var(
            doc="Shomate D parameter for ideal gas molar heat capacity",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1*pyunits.kiloK**-3)
        set_param_value(
            cobj,
            param="cp_mol_ig_comp_coeff",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1*pyunits.kiloK**-3,
            index="D")

        cobj.cp_mol_ig_comp_coeff_E = Var(
            doc="Shomate E parameter for ideal gas molar heat capacity",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1*pyunits.kiloK**2)
        set_param_value(
            cobj,
            param="cp_mol_ig_comp_coeff",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1*pyunits.kiloK**2,
            index="E")

        cobj.cp_mol_ig_comp_coeff_F = Var(
            doc="Shomate F parameter for ideal gas molar heat capacity",
            units=pyunits.kJ*pyunits.mol**-1)
        set_param_value(
            cobj,
            param="cp_mol_ig_comp_coeff",
            units=pyunits.kJ*pyunits.mol**-1,
            index="F")

        cobj.cp_mol_ig_comp_coeff_G = Var(
            doc="Shomate G parameter for ideal gas molar heat capacity",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1)
        set_param_value(
            cobj,
            param="cp_mol_ig_comp_coeff",
            units=pyunits.J*pyunits.mol**-1*pyunits.K**-1,
            index="G")

        cobj.cp_mol_ig_comp_coeff_H = Var(
            doc="Shomate H parameter for ideal gas molar heat capacity",
            units=pyunits.kJ*pyunits.mol**-1)
        set_param_value(
            cobj,
            param="cp_mol_ig_comp_coeff",
            units=pyunits.kJ*pyunits.mol**-1,
            index="H")

    @staticmethod
    def return_expression(b, cobj, T):
        # Specific heat capacity (const. P)  via the Shomate equation
        t = pyunits.convert(T, to_units=pyunits.kiloK)
        cp = (cobj.cp_mol_ig_comp_coeff_A +
              cobj.cp_mol_ig_comp_coeff_B*t +
              cobj.cp_mol_ig_comp_coeff_C*t**2 +
              cobj.cp_mol_ig_comp_coeff_D*t**3 +
              cobj.cp_mol_ig_comp_coeff_E*t**-2)

        units = b.params.get_metadata().derived_units
        return pyunits.convert(cp, units["heat_capacity_mole"])


class enth_mol_ig_comp():

    @staticmethod
    def build_parameters(cobj):
        if not hasattr(cobj, "cp_mol_ig_comp_coeff_A"):
            cp_mol_ig_comp.build_parameters(cobj)

    @staticmethod
    def return_expression(b, cobj, T):
        # Specific enthalpy via the Shomate equation
        t = pyunits.convert(T, to_units=pyunits.kiloK)
        tr = pyunits.convert(b.params.temperature_ref, to_units=pyunits.kiloK)

        h = (cobj.cp_mol_ig_comp_coeff_A*(t-tr) +
             (cobj.cp_mol_ig_comp_coeff_B/2)*(t**2-tr**2) +
             (cobj.cp_mol_ig_comp_coeff_C/3)*(t**3-tr**3) +
             (cobj.cp_mol_ig_comp_coeff_D/4)*(t**4-tr**4) -
             cobj.cp_mol_ig_comp_coeff_E*(1/t-1/tr) +
             cobj.cp_mol_ig_comp_coeff_F -
             cobj.cp_mol_ig_comp_coeff_H)

        units = b.params.get_metadata().derived_units
        return pyunits.convert(h, units["energy_mole"])


class entr_mol_ig_comp():

    @staticmethod
    def build_parameters(cobj):
        if not hasattr(cobj, "cp_mol_ig_comp_coeff_A"):
            cp_mol_ig_comp.build_parameters(cobj)

    @staticmethod
    def return_expression(b, cobj, T):
        # Specific entropy via the Shomate equation
        t = pyunits.convert(T, to_units=pyunits.kiloK)
        s = (cobj.cp_mol_ig_comp_coeff_A*log(t/pyunits.kiloK) +  # need to make unitless
             cobj.cp_mol_ig_comp_coeff_B*t +
             (cobj.cp_mol_ig_comp_coeff_C/2)*t**2 +
             (cobj.cp_mol_ig_comp_coeff_D/3)*t**3 -
             (cobj.cp_mol_ig_comp_coeff_E/2)*t**-2 +
             cobj.cp_mol_ig_comp_coeff_G)

        units = b.params.get_metadata().derived_units
        return pyunits.convert(s, units["entropy_mole"])


# -----------------------------------------------------------------------------
# Antoine equation for saturation pressure
class pressure_sat_comp():

    @staticmethod
    def build_parameters(cobj):
        cobj.pressure_sat_comp_coeff_A = Var(
                doc="Antoine A coefficient for calculating Psat",
                units=None)
        set_param_value(cobj,
                        param="pressure_sat_comp_coeff",
                        units=None,
                        index="A")

        cobj.pressure_sat_comp_coeff_B = Var(
                doc="Antoine B coefficient for calculating Psat",
                units=pyunits.K)
        set_param_value(cobj,
                        param="pressure_sat_comp_coeff",
                        units=pyunits.K,
                        index="B")

        cobj.pressure_sat_comp_coeff_C = Var(
                doc="Antoine C coefficient for calculating Psat",
                units=pyunits.K)
        set_param_value(cobj,
                        param="pressure_sat_comp_coeff",
                        units=pyunits.K,
                        index="C")

    @staticmethod
    def return_expression(b, cobj, T, dT=False):
        if dT:
            return pressure_sat_comp.dT_expression(b, cobj, T)

        psat = 10**(cobj.pressure_sat_comp_coeff_A -
                    cobj.pressure_sat_comp_coeff_B /
                    (pyunits.convert(T, to_units=pyunits.K) +
                     cobj.pressure_sat_comp_coeff_C))*pyunits.bar

        units = b.params.get_metadata().derived_units
        return pyunits.convert(psat, to_units=units["pressure"])

    @staticmethod
    def dT_expression(b, cobj, T):
        p_sat_dT = (pressure_sat_comp.return_expression(b, cobj, T) *
                    cobj.pressure_sat_comp_coeff_B *
                    log(10)/(pyunits.convert(T, to_units=pyunits.K) +
                             cobj.pressure_sat_comp_coeff_C)**2)

        units = b.params.get_metadata().derived_units
        dp_units = units["pressure"]/units["temperature"]
        return pyunits.convert(p_sat_dT, to_units=dp_units)
