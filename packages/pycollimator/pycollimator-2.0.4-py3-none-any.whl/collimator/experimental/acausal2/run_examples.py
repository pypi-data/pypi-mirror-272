# Copyright (C) 2024 Collimator, Inc.
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, version 3. This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General
# Public License for more details.  You should have received a copy of the GNU
# Affero General Public License along with this program. If not, see
# <https://www.gnu.org/licenses/>.

from component_library.base import EqnEnv
from diagram_processing import AcausalDiagram
from acausal_compiler import AcausalCompiler
from component_library import elec
from component_library import translational as trans
from component_library import rotational as rot
from component_library import thermal as ht
from component_library import cross_domain as cd
from component_library import fluid_i as fld


def const_voltage_RC_circuit():
    # expected output of diagram_processing
    # Cv - Vparam = Vref
    # Vref = I*R
    # -I = C*dCv
    # dCv = Der(Cv) # der_relation
    print("======================const_voltage_RC_circuit")
    # EqnEnv an object that 'holds' the symbol for 'time' that is used in all equations.
    ev = EqnEnv()
    diagram = AcausalDiagram()
    v1 = elec.VoltageSource(ev, name="v1", enable_voltage_port=False)
    r1 = elec.Resistor(ev, name="r1")
    c1 = elec.Capacitor(ev, name="c1")
    ref1 = elec.Ground(ev, name="ref1")
    diagram.connect(v1, "p", r1, "n")
    diagram.connect(r1, "p", c1, "p")
    diagram.connect(c1, "n", v1, "n")
    diagram.connect(v1, "n", ref1, "p")
    compiler = AcausalCompiler(ev, diagram)
    # compiler.diagram_processing()
    # compiler.index_reduction()
    # compiler.generate_phleaf()
    compiler()  # this now replaces the 3 lines above


def const_voltage_RLC_circuit():
    # expected output of diagram_processing
    # Vparam = Rv + Cv + Lv
    # Rv = I*R
    # I = C*dCv
    # Lv = L*dI
    # dCv = Der(Cv) # der_relation
    # dI = Der(I) # der_relation

    print("======================const_voltage_RLC_circuit")
    ev = EqnEnv()
    diagram = AcausalDiagram()
    v1 = elec.VoltageSource(ev, name="v1", enable_voltage_port=True)
    r1 = elec.Resistor(ev, name="r1")
    c1 = elec.Capacitor(ev, name="c1")
    l1 = elec.Inductor(ev, name="l1")
    ref1 = elec.Ground(ev, name="ref1")
    diagram.connect(v1, "p", r1, "p")
    diagram.connect(r1, "n", l1, "p")
    diagram.connect(l1, "n", c1, "p")
    diagram.connect(c1, "n", v1, "n")
    diagram.connect(v1, "n", ref1, "p")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def translational_oscillator():
    # expected output of diagram_processing
    # f = x1*k
    # -f = m*a1
    # v1 = Der(x1) # der_relation
    # a1 = Der(v1) # der_relation

    print("======================translational_oscillator")
    ev = EqnEnv()
    diagram = AcausalDiagram()
    m1 = trans.Mass(ev, name="m1", M=1.0, initial_position=1.0)
    sp1 = trans.Spring(ev, name="sp1", initial_position_A=1.0)
    r1 = trans.FixedPosition(ev, name="r1")
    diagram.connect(sp1, "flange_a", m1, "flange")
    diagram.connect(sp1, "flange_b", r1, "flange")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def translational_oscillator_damped():
    # expected output of diagram_processing
    # f = m*m_a
    # -d_f2 = b*m_v
    # sp_f1 = m_x*k
    # 0 = d_f2 + ref_f - sp_f1
    # 0 = -d_f2 + m_f + sp_f1
    # m_a = Der(m_v) # der_relation
    # m_v = Der(m_x) # der_relation

    print("======================translational_oscillator_damped")
    ev = EqnEnv()
    diagram = AcausalDiagram()
    x_ic = 1.0
    m1 = trans.Mass(ev, name="m1", M=1.0, initial_position=x_ic)
    sp1 = trans.Spring(ev, name="sp1", initial_position_A=x_ic)
    d1 = trans.Damper(ev, name="d1", initial_position_A=x_ic)
    r1 = trans.FixedPosition(ev, name="r1")
    diagram.connect(sp1, "flange_a", m1, "flange")
    diagram.connect(sp1, "flange_b", r1, "flange")
    diagram.connect(sp1, "flange_a", d1, "flange_a")
    diagram.connect(sp1, "flange_b", d1, "flange_b")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def rotational_oscillator_damped():
    print("======================rotational_oscillator_damped")
    ev = EqnEnv()
    diagram = AcausalDiagram()
    ang_ic = 1.0
    I1 = rot.Inertia(ev, name="I1", I=1.0, initial_angle=ang_ic)
    sp1 = rot.Spring(ev, name="sp1", initial_angle_A=ang_ic)
    d1 = rot.Damper(ev, name="d1", initial_angle_A=ang_ic)
    r1 = rot.FixedAngle(ev, name="r1")
    diagram.connect(sp1, "flange_a", I1, "flange")
    diagram.connect(sp1, "flange_b", r1, "flange")
    diagram.connect(sp1, "flange_a", d1, "flange_a")
    diagram.connect(sp1, "flange_b", d1, "flange_b")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def translational_damped_thruster():
    print("======================translational_damped_thruster")
    ev = EqnEnv()
    diagram = AcausalDiagram()
    f1 = trans.ForceSource(ev, name="f1", F=1.0)
    m1 = trans.Mass(ev, name="m1", M=1.0)
    d1 = trans.Damper(ev, name="d1")
    r1 = trans.FixedPosition(ev, name="r1")
    diagram.connect(f1, "flange", m1, "flange")
    diagram.connect(f1, "flange", d1, "flange_a")
    diagram.connect(d1, "flange_b", r1, "flange")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def thermal_temp_source():
    # expected output of diagram_processing
    # r1_dT = -r1_R*r1_Q2
    # -r1_Q2 = c1_C*c1_derT
    # r1_dT = Tparam + r1_T2
    # c1_derT = Derivative(r1_T2)

    print("======================thermal_temp_source")
    ev = EqnEnv()
    diagram = AcausalDiagram()
    tref = ht.TemperatureSource(ev, name="tref")
    r1 = ht.ThermalResistor(ev, name="r1")
    c1 = ht.HeatCapacitor(ev, name="c1")
    hs1 = ht.HeatFlowSource(ev, name="hs1", Q=-10.0)
    diagram.connect(tref, "port", r1, "port_a")
    diagram.connect(r1, "port_b", c1, "port")
    diagram.connect(c1, "port", hs1, "port")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def cross_domain():
    # expected output of diagram_processing
    # ??

    print("======================cross_domain")
    # has elec, rot, trans, and thermal domains.
    ev = EqnEnv()
    diagram = AcausalDiagram()

    # declare components
    mot = cd.IdealMotor(ev, enable_heat_port=True)
    J = rot.Inertia(ev, name="J", I=1.0)
    v = elec.VoltageSource(ev, name="v1", enable_voltage_port=True)
    ref1 = elec.Ground(ev, name="ref1")
    r = elec.Resistor(ev, name="r", R=0.1, enable_heat_port=True)
    whl = cd.IdealWheel(ev, name="whl", r=0.1)
    mass = trans.Mass(ev, name="mass", M=1.0)
    thermal_mass = ht.HeatCapacitor(ev, name="tm")

    # declare connection
    diagram.connect(v, "p", mot, "pos")
    diagram.connect(v, "n", r, "p")
    diagram.connect(r, "n", mot, "neg")
    diagram.connect(v, "n", ref1, "p")
    diagram.connect(mot, "shaft", J, "flange")
    diagram.connect(mot, "shaft", whl, "shaft")
    diagram.connect(whl, "p", mass, "flange")
    diagram.connect(mot, "heat", thermal_mass, "port")
    diagram.connect(r, "heat", thermal_mass, "port")

    # model compilation
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def fluid_pressure_to_accumulator():
    # expected output of diagram_processing
    # ?

    print("======================fluid_pressure_to_accumulator")
    fluid = fld.Fluid(fluid=fld.FluidName.water)
    ev = EqnEnv(fluid=fluid)
    diagram = AcausalDiagram()
    ps = fld.PressureSource(ev)
    pipe = fld.Pipe(ev)
    acc = fld.Accumulator(ev)
    diagram.connect(ps, "port", pipe, "port_a")
    diagram.connect(pipe, "port_b", acc, "port")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def fluid_inline_pump():
    # expected output of diagram_processing
    # ?

    print("======================fluid_inline_pump")
    fluid = fld.Fluid(fluid=fld.FluidName.hydraulic_fluid)
    ev = EqnEnv(fluid=fluid)
    diagram = AcausalDiagram()
    ps1 = fld.PressureSource(ev, name="ps1", pressure=0.01)
    pipe1 = fld.Pipe(ev, name="pipe1")
    pmp = fld.Pump(ev)
    pipe2 = fld.Pipe(ev, name="pipe2")
    ps2 = fld.PressureSource(ev, name="ps2")
    diagram.connect(ps1, "port", pipe1, "port_a")
    diagram.connect(pipe1, "port_b", pmp, "port_a")
    diagram.connect(pmp, "port_b", pipe2, "port_a")
    diagram.connect(pipe2, "port_b", ps2, "port")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def hyd_act_and_spring():
    # expected output of diagram_processing
    # see WC-341

    print("======================hyd_act_and_spring")
    fluid = fld.Fluid(fluid=fld.FluidName.hydraulic_fluid)
    ev = EqnEnv(fluid=fluid)
    diagram = AcausalDiagram()
    ps1 = fld.PressureSource(ev, name="ps1")
    ps2 = fld.PressureSource(ev, name="ps2", pressure=0.1)
    act = cd.HydraulicActuatorLinear(ev, name="act")
    ref1 = trans.FixedPosition(ev, name="ref1")
    mass = trans.Mass(ev, name="mass")
    sprg = trans.Spring(ev, name="sprg")
    ref2 = trans.FixedPosition(ev, name="ref2")
    diagram.connect(ps1, "port", act, "f1")
    diagram.connect(ps2, "port", act, "f2")
    diagram.connect(act, "flange_a", ref1, "flange")
    diagram.connect(act, "flange_b", sprg, "flange_a")
    diagram.connect(act, "flange_b", mass, "flange")
    diagram.connect(sprg, "flange_b", ref2, "flange")
    compiler = AcausalCompiler(ev, diagram)
    compiler.diagram_processing()
    compiler.index_reduction()


def varistor_lookup_table():
    # expected output of diagram_processing
    # ?
    print("======================varistor_lookup_table")
    ev = EqnEnv()
    diagram = AcausalDiagram()
    v1 = elec.VoltageSource(ev, name="v1")
    r1 = cd.Varistor(ev, name="r1")
    c1 = elec.Capacitor(ev, name="c1")
    ref1 = elec.Ground(ev, name="ref1")
    diagram.connect(v1, "p", r1, "n")
    diagram.connect(r1, "p", c1, "p")
    diagram.connect(c1, "n", v1, "n")
    diagram.connect(v1, "n", ref1, "p")
    compiler = AcausalCompiler(ev, diagram)
    compiler()


if __name__ == "__main__":
    const_voltage_RC_circuit()
    const_voltage_RLC_circuit()
    translational_oscillator()
    translational_oscillator_damped()
    rotational_oscillator_damped()
    translational_damped_thruster()
    thermal_temp_source()
    cross_domain()
    fluid_pressure_to_accumulator()
    fluid_inline_pump()
    hyd_act_and_spring()
    varistor_lookup_table()
