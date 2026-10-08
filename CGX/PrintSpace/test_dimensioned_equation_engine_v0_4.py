"""Regression tests for dimensionally consistent CGX analytic screening v0.4.
All values are synthetic equation-check fixtures, not measured material data.
"""
import json
import math
import unittest
from pathlib import Path
from dimensioned_equation_engine import evaluate, load_catalogue, validate_catalogue

HERE=Path(__file__).resolve().parent

def read(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))

class DimensionalEquationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=load_catalogue()
        cls.cross=read("PHYSICS_FUNCTION_CROSSWALK_v0_4.json")
        cls.materials=read("MATERIAL_CANDIDATE_PASSPORTS_v0_3.json")

    def test_all_equation_dimensions(self):
        self.assertTrue(validate_catalogue(self.registry))
        self.assertEqual(len(self.registry["models"]),59)

    def test_canonical_constants_explicit(self):
        cs=self.registry["constants"]
        self.assertAlmostEqual(cs["c_light"]["value"],299792458.0,places=0)
        self.assertEqual(cs["eps0"]["status"],"CODATA_2022_APPROXIMATE")
        self.assertEqual(cs["mu0"]["status"],"CODATA_2022_APPROXIMATE")

    def test_dc_resistance_and_power(self):
        r=evaluate("PS-EQ-001",dict(resistivity=1.7e-8,length=1.,area=1e-6))
        self.assertAlmostEqual(r["value"],0.017)
        p=evaluate("PS-EQ-002",dict(current=2.,resistance=r["value"]))
        self.assertAlmostEqual(p["value"],0.068)
        self.assertFalse(r["production_approved"])

    def test_capacitance_and_energy(self):
        c=evaluate("PS-EQ-004",dict(eps_r=2,area=0.01,gap=0.001))["value"]
        self.assertAlmostEqual(c,2*8.8541878188e-12*0.01/0.001)
        j=evaluate("PS-EQ-005",dict(capacitance=c,voltage=5))["value"]
        self.assertAlmostEqual(j,0.5*c*25)

    def test_resonant_frequency(self):
        f=evaluate("PS-EQ-006",dict(inductance=0.001,capacitance=1e-6))["value"]
        self.assertAlmostEqual(f,1/(2*math.pi*math.sqrt(1e-9)),places=8)

    def test_laminar_circular_channel_screen(self):
        q=evaluate("PS-EQ-014",dict(radius=.001,delta_pressure=10.,dynamic_viscosity=.001,length=.1))["value"]
        self.assertAlmostEqual(q,math.pi*.001**4*10/(8*.001*.1))

    def test_bond_number_and_capillarity_gravity(self):
        params=dict(density_difference=1000,gravity=9.81,length=.001,surface_tension=.072)
        earth=evaluate("PS-EQ-021",params)["value"]
        self.assertAlmostEqual(earth,0.13625)
        orbit=evaluate("PS-EQ-021",{**params,"gravity":0})["value"]
        self.assertEqual(orbit,0)
        with self.assertRaises(ValueError):
            evaluate("PS-EQ-046",dict(surface_tension=.072,density_difference=1000,gravity=0))

    def test_post_mix_ideal_mass_balance(self):
        frac=evaluate("PS-EQ-035",dict(mass_a=2.,fraction_a=.1,mass_b=1.,fraction_b=.4))["value"]
        self.assertAlmostEqual(frac,.2)

    def test_unrestrained_thermal_mismatch(self):
        mismatch=evaluate("PS-EQ-041",dict(alpha_a=1e-5,alpha_b=3e-5,delta_temperature=100.,length=.1))["value"]
        self.assertAlmostEqual(mismatch,0.0002)

    def test_ideal_gas_and_permeation(self):
        p=evaluate("PS-EQ-019",dict(moles=1.,temperature=300.,volume=0.01))["value"]
        self.assertAlmostEqual(p,8.31446261815324*300/0.01)
        leak=evaluate("PS-EQ-024",dict(permeability=1e-15,area=1e-4,delta_pressure=1e5,thickness=1e-3))["value"]
        self.assertAlmostEqual(leak,1e-11)
        self.assertFalse(evaluate("PS-EQ-024",dict(permeability=1e-15,area=1e-4,delta_pressure=1e5,thickness=1e-3))["production_approved"])

    def test_no_silent_defaults_or_invalid_inputs(self):
        with self.assertRaises(ValueError):
            evaluate("PS-EQ-001",{"length":1.,"area":1e-6})
        with self.assertRaises(ValueError):
            evaluate("PS-EQ-001",{"resistivity":1e-8,"length":1.,"area":0})
        with self.assertRaises(ValueError):
            evaluate("PS-EQ-030",dict(irradiance=500,area=1,conversion_efficiency=1.2))
        with self.assertRaises(ValueError):
            evaluate("PS-EQ-019",dict(moles=1,temperature=-5,volume=1))
        with self.assertRaises(ValueError):
            evaluate("PS-EQ-001",dict(resistivity=float("nan"),length=1,area=1))

    def test_dimension_falsification_detected(self):
        modified=json.loads(json.dumps(self.registry))
        modified["models"][0]["result_unit"]="s"
        with self.assertRaises(ValueError):
            validate_catalogue(modified)

    def test_physics_crosswalk_coverage_and_referential_integrity(self):
        m=self.cross
        self.assertEqual(len(m["technology_bindings"]),70)
        self.assertEqual(len(m["geometry_bindings"]),30)
        self.assertEqual(len(m["environment_bindings"]),26)
        self.assertEqual(len(m["material_route_bindings"]),72)
        valid={x["id"] for x in self.registry["models"]}
        for kind,field in (("technology_bindings","analytic_equation_ids"),
                           ("geometry_bindings","analytic_equation_ids"),
                           ("environment_bindings","analytic_screening_equation_ids"),
                           ("material_route_bindings","screening_equation_ids")):
            for entry in m[kind]:
                self.assertTrue(set(entry[field])<=valid)
                self.assertFalse(entry["production_approved"])
        self.assertEqual({x["technology_id"] for x in m["technology_bindings"]},
                         {f"PT-{n:03d}" for n in range(1,71)})

    def test_similarity_scaling_for_terrestrial_and_orbital_cells(self):
        pe=evaluate("PS-EQ-048",dict(velocity=0.1,length=0.001,diffusivity=1e-9))["value"]
        self.assertAlmostEqual(pe,100000)
        ca=evaluate("PS-EQ-049",dict(dynamic_viscosity=0.001,velocity=0.1,surface_tension=0.07))["value"]
        self.assertAlmostEqual(ca,0.001/0.07*0.1)
        we=evaluate("PS-EQ-050",dict(density=1000,velocity=0.1,length=0.001,surface_tension=0.07))["value"]
        self.assertAlmostEqual(we,1000*.1**2*.001/.07)
        kn=evaluate("PS-EQ-053",dict(mean_free_path=1e-7,length=1e-6))["value"]
        self.assertAlmostEqual(kn,0.1)
        da=evaluate("PS-EQ-054",dict(flow_timescale=2.,reaction_timescale=1.))["value"]
        self.assertAlmostEqual(da,2.)

    def test_thermal_diffusivity_and_similarity(self):
        alpha=evaluate("PS-EQ-058",dict(thermal_conductivity=0.2,density=1000,specific_heat=4000))["value"]
        self.assertAlmostEqual(alpha,5e-8)
        fo=evaluate("PS-EQ-051",dict(thermal_diffusivity=alpha,duration=10,length=0.001))["value"]
        self.assertAlmostEqual(fo,0.5)
        bi=evaluate("PS-EQ-052",dict(convective_coefficient=10,length=.01,thermal_conductivity=.2))["value"]
        self.assertAlmostEqual(bi,0.5)

    def test_skin_depth_and_magnetofluid_similarity(self):
        sd=evaluate("PS-EQ-059",dict(resistivity=1.7e-8,mu_r=1.,angular_speed=2*math.pi*1e6))["value"]
        self.assertGreater(sd,0)
        self.assertLess(sd,0.001)
        rm=evaluate("PS-EQ-055",dict(mu_r=1.,electrical_conductivity=5.8e7,velocity=0.1,length=0.01))["value"]
        self.assertGreater(rm,0)
        ha=evaluate("PS-EQ-056",dict(magnetic_field=.1,length=.01,electrical_conductivity=1e6,dynamic_viscosity=.001))["value"]
        self.assertAlmostEqual(ha,0.1*.01*math.sqrt(1e9))
        debye=evaluate("PS-EQ-057",dict(debye_length=1e-8,length=1e-6))["value"]
        self.assertAlmostEqual(debye,0.01)

    def test_scale_binding_vectors_are_typed_and_non_approved(self):
        valid={x["id"] for x in self.registry["models"]}
        scale=set(f"PS-EQ-{i:03d}" for i in range(48,60))
        for group in ("technology_bindings","geometry_bindings",
                      "environment_bindings","material_route_bindings"):
            for rec in self.cross[group]:
                entries=rec.get("scale_regime_equation_ids")
                self.assertIsNotNone(entries)
                self.assertTrue(set(entries)<=valid)
                self.assertTrue(set(entries)<=scale)
                self.assertFalse(rec["production_approved"])

    def test_complete_kernel_reference_naming(self):
        known={"K-CLOSURE","K-FLUID-MASS","K-FLUID-MOM","K-ENERGY","K-SPECIES",
               "K-MAXWELL","K-NP","K-BV","K-CH","K-AC","K-MECH","K-SEMI",
               "K-PLASMA","K-RADIATION","K-FREEENERGY","K-RAPHAEL-OBW",
               "K-EML-CANDIDATE"}
        for eq in self.registry["models"]:
            self.assertTrue(set(eq["utp_kernel_ids"])<=known)
            self.assertFalse(eq["production_approved"])

    def test_qualified_properties_still_unset(self):
        self.assertEqual(sum(len(x["measured_material_properties"]) for x in self.materials["materials"]),0)
        self.assertTrue(all(x["process_window"] is None for x in self.materials["materials"]))


if __name__=="__main__":
    unittest.main()
