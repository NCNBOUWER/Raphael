"""Deterministic CGX PrintSpace replay tests; not process qualification."""
import copy
import json
import math
import unittest
from pathlib import Path
from functional_time_preview import (
    SEEDS, SCHEMA, _sorted_stages, compile_preview,
    load_and_compile, validate_seed, assess_functional_device_requirements,
    assess_process_window, review_directional_material_transition,
)

class FunctionalTimeReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.seeds=json.loads(Path(SEEDS).read_text(encoding="utf-8"))
        cls.output=load_and_compile()
        cls.products={p["id"]:p for p in cls.output["products"]}

    def test_source_and_global_holds(self):
        self.assertTrue(validate_seed(self.seeds))
        self.assertEqual(self.output["schema"], SCHEMA)
        self.assertEqual(len(self.output["products"]),3)
        self.assertEqual(len(self.output["source_sha256"]),64)
        self.assertFalse(self.output["public_release_authorized"])
        self.assertFalse(self.output["machine_control_enabled"])
        self.assertFalse(self.output["physical_or_calibrated_simulation"])
        self.assertEqual(self.output, load_and_compile())

    def test_butter_bot_has_assembled_part_replay_and_motion_candidate(self):
        b=self.products["BB-SOURCE-DEMO"]
        self.assertEqual(len(b["parts"]),10)
        self.assertEqual(len(b["frames"]),9)
        self.assertIn("left_arm",b["frames"][-1]["visible_part_ids"])
        self.assertIn("right_arm",b["frames"][-1]["visible_part_ids"])
        self.assertNotIn("left_arm",b["frames"][0]["visible_part_ids"])
        self.assertEqual(b["motion_candidate"]["track_count_candidate"],2)
        self.assertIsNone(b["motion_candidate"]["torque_nm"])
        self.assertFalse(b["motion_candidate"]["torque_verified"])
        self.assertFalse(b["production_approved"])

    def test_watch_variants_non_gendered_and_dimensioned(self):
        square=self.products["WATCH-SQUARE"]
        round_watch=self.products["WATCH-ROUND"]
        self.assertEqual(square["aesthetic"]["gendered"],False)
        self.assertEqual(round_watch["aesthetic"]["gendered"],False)
        self.assertEqual(square["display_area_mm2_candidate"],961)
        self.assertAlmostEqual(round_watch["display_area_mm2_candidate"],
                               math.pi * 32**2 / 4,places=4)
        for p in (square,round_watch):
            self.assertIsNone(p["compute_capacity_n"])
            self.assertIsNone(p["battery_capacity_wh"])
            self.assertEqual(len(p["frames"]),7)
            self.assertEqual(p["frames"][-1]["progress_fraction"],1)
            self.assertFalse(p["qualified_fabrication"])
            self.assertTrue(all(f["claimed_elapsed_seconds"] is None for f in p["frames"]))

    def test_every_part_assigned_exactly_once_and_stages_qualified_false(self):
        for product in self.output["products"]:
            all_parts={p["id"] for p in product["parts"]}
            disclosed=[part for frame in product["frames"] for part in frame["added_part_ids"]]
            self.assertEqual(set(disclosed),all_parts)
            self.assertEqual(len(disclosed),len(set(disclosed)))
            self.assertEqual(set(product["frames"][-1]["visible_part_ids"]),all_parts)
            self.assertEqual([x["progress_fraction"] for x in product["frames"]],
                             sorted(x["progress_fraction"] for x in product["frames"]))
            self.assertTrue(all(not x["qualified_process"] for x in product["frames"]))

    def test_masked_litho_and_laser_held_for_specific_process_evidence(self):
        masks=[f for f in self.products["WATCH-ROUND"]["frames"] if f["process"]=="MASKED_PHOTOLITHOGRAPHY_CANDIDATE"]
        laser=[f for f in self.products["WATCH-SQUARE"]["frames"] if f["process"]=="LASER_DIRECT_WRITE_CANDIDATE"]
        self.assertEqual(len(masks),1)
        self.assertEqual(len(laser),1)
        self.assertIn("photoresist", masks[0]["process_required_evidence"])
        self.assertIn("etch_or_deposit_compatibility",masks[0]["process_required_evidence"])
        self.assertIn("enclosure_interlocks",laser[0]["process_required_evidence"])
        self.assertIn("fluence_threshold",laser[0]["process_required_evidence"])
        self.assertIsNone(laser[0]["measured_energy_j"])

    def test_arm_angle_payload_and_motion_are_bounded_not_certified(self):
        result=assess_functional_device_requirements(
            self.products["BB-SOURCE-DEMO"], arm_angle_deg=30,
            arm_length_mm=100, payload_mass_kg=0.5)
        self.assertAlmostEqual(result["arm_tip_horizontal_offset_mm"], 50, places=4)
        self.assertAlmostEqual(result["arm_tip_vertical_rise_mm"], 86.60254,places=4)
        self.assertAlmostEqual(result["static_gravity_torque_nm_candidate"],0.24516625,places=7)
        self.assertFalse(result["hardware_control"])
        self.assertFalse(result["measured_or_qualified"])
        self.assertTrue(any("motor" in hold for hold in result["unresolved"]))
        negative=assess_functional_device_requirements(
            self.products["BB-SOURCE-DEMO"],arm_angle_deg=-30,arm_length_mm=100)
        self.assertAlmostEqual(negative["arm_tip_horizontal_offset_mm"],-50,places=4)
        self.assertIsNone(negative["static_gravity_torque_nm_candidate"])

    def test_screen_battery_compute_unitless_inputs_never_claim_functional_device(self):
        square=self.products["WATCH-SQUARE"]
        result=assess_functional_device_requirements(
            square,required_screen_area_mm2=960, battery_capacity_wh=4.5,
            average_power_w=0.5,compute_target_n=120000,
            compute_metric="reference_operations_per_second")
        self.assertEqual(result["display_fit_comparison"],"AREA_ONLY_FITS")
        self.assertEqual(result["ideal_arithmetic_runtime_h"],9)
        self.assertEqual(result["compute_n_user_candidate"],120000)
        self.assertFalse(result["hardware_control"])
        self.assertTrue(any("optical" in hold for hold in result["unresolved"]))
        oversized=assess_functional_device_requirements(
            square,required_screen_area_mm2=1200)
        self.assertEqual(oversized["display_fit_comparison"],
                         "AREA_EXCEEDS_SCHEMATIC_APERTURE")
        self.assertFalse(oversized["measured_or_qualified"])

    def test_functional_parameter_inputs_fail_closed(self):
        bot=self.products["BB-SOURCE-DEMO"]
        watch=self.products["WATCH-ROUND"]
        bad=[
            (bot,{"arm_angle_deg":181},"-180..180"),
            (bot,{"arm_angle_deg":float("nan")},"finite"),
            (bot,{"arm_angle_deg":40,"arm_length_mm":-1},"nonnegative"),
            (watch,{"arm_angle_deg":5},"not applicable"),
            (watch,{"battery_capacity_wh":float("inf")},"finite"),
            (watch,{"average_power_w":0},"positive"),
            (watch,{"compute_target_n":10},"declared metric"),
        ]
        for product,values,msg in bad:
            with self.subTest(values=values):
                with self.assertRaisesRegex(ValueError,msg):
                    assess_functional_device_requirements(product,**values)

    def test_temporal_window_wet_lithography_is_conditional_not_qualified(self):
        wet=assess_process_window(
            "MASKED_PHOTOLITHOGRAPHY_CANDIDATE",
            substrate_state="WET_FLOWABLE",environment="LOCAL_SHROUD",
            source_lot_ref="UNVERIFIED_LOT_LABEL",
            substrate_temperature_c=55.0,
            exposure_dose_j_cm2=1.25,focus_or_alignment_um=10.0,
        )
        self.assertEqual(
            wet["disposition"],
            "CAN_IF_WET_CHEMISTRY_FOCUS_AND_MASK_COUPONS_VALIDATED")
        self.assertTrue(any("mask adhesion" in x for x in
                            wet["requires_independent_evidence"]))
        self.assertTrue(any("earlier deposited material" in x for x in
                            wet["requires_independent_evidence"]))
        self.assertFalse(wet["physical_process_verified"])
        self.assertFalse(wet["safety_interlocks_verified"])
        self.assertFalse(wet["production_approved"])
        self.assertIsNone(wet["hardware_command"])
        self.assertIsNone(wet["claim_time_seconds"])

    def test_optical_state_unknown_and_laser_open_enclosure_gates(self):
        unknown=assess_process_window("LASER_DIRECT_WRITE_CANDIDATE")
        self.assertEqual(unknown["disposition"],"HOLD_SUBSTRATE_STATE_UNRESOLVED")
        self.assertIn("actual substrate cure/rheology and temperature state",
                      unknown["requires_independent_evidence"])
        open_air=assess_process_window(
            "LASER_DIRECT_WRITE_CANDIDATE",
            substrate_state="STABILIZED",environment="OPEN",
            source_lot_ref="USER_LOT",substrate_temperature_c=24,
            exposure_dose_j_cm2=0.1,focus_or_alignment_um=15)
        self.assertEqual(open_air["disposition"],
                         "HOLD_LASER_ENCLOSURE_NOT_QUALIFIED")
        self.assertFalse(open_air["production_approved"])
        self.assertTrue(any("open laser" in s for s in
                            open_air["requires_independent_evidence"]))
        conditioned=assess_process_window(
            "LASER_DIRECT_WRITE_CANDIDATE",
            substrate_state="STABILIZED",environment="MACRO_CHAMBER",
            source_lot_ref="UNVERIFIED_SOURCE",substrate_temperature_c=24,
            exposure_dose_j_cm2=1.0,focus_or_alignment_um=3.5)
        self.assertEqual(conditioned["disposition"],
                         "CAN_IF_SOURCE_REQUIREMENTS_INDEPENDENTLY_QUALIFIED")
        self.assertFalse(conditioned["material_compatibility_verified"])
        self.assertFalse(conditioned["safety_interlocks_verified"])

    def test_green_staged_uv_process_requires_transient_material_history(self):
        green=assess_process_window(
            "UV_CURE_CANDIDATE",substrate_state="GREEN_PARTIALLY_CURED",
            environment="SEALED_MICROCHAMBER")
        self.assertEqual(green["disposition"],
                         "CAN_IF_TRANSIENT_STATE_EXPOSURE_AND_DAMAGE_VALIDATED")
        self.assertTrue(any("viscosity" in s for s in green["requires_independent_evidence"]))
        self.assertFalse(green["production_approved"])

    def test_directional_material_pair_provenance_not_reversible_authority(self):
        forward=review_directional_material_transition("TP","CI")
        reverse=review_directional_material_transition("CI","TP")
        self.assertEqual(forward["pair_id"],"PS-PAIR-TP-CI")
        self.assertEqual(reverse["pair_id"],"PS-PAIR-CI-TP")
        self.assertEqual(forward["reverse_pair_id"],reverse["pair_id"])
        self.assertEqual(forward["source_catalog_sha256"],reverse["source_catalog_sha256"])
        self.assertEqual(len(forward["source_catalog_sha256"]),64)
        self.assertTrue(forward["reverse_is_separate_contract"])
        self.assertFalse(forward["production_approved"])
        self.assertFalse(forward["actual_tool_route_available"])
        self.assertIn("Pause, cure, clean and resume",forward["fallback_routes"])

    def test_process_input_and_material_family_are_fail_closed(self):
        attempts=[
            {"process":"LASER_DIRECT_WRITE_CANDIDATE",
             "substrate_state":"STABILIZED","environment":"OPEN",
             "exposure_dose_j_cm2":float("nan")},
            {"process":"LASER_DIRECT_WRITE_CANDIDATE",
             "substrate_state":"STABILIZED","environment":"OPEN",
             "exposure_dose_j_cm2":-2},
            {"process":"LASER_DIRECT_WRITE_CANDIDATE",
             "substrate_state":"STABILIZED","environment":"OPEN",
             "focus_or_alignment_um":True},
            {"process":"LASER_DIRECT_WRITE_CANDIDATE",
             "substrate_state":"HOT_AND_PERFECT"},
            {"process":"LASER_DIRECT_WRITE_CANDIDATE",
             "environment":"MAGIC_VACUUM"},
            {"process":"LASER_DIRECT_WRITE_CANDIDATE",
             "source_lot_ref":"CREDENTIAL\nBAD"},
        ]
        for item in attempts:
            with self.subTest(item=item):
                process=item.pop("process")
                with self.assertRaises(ValueError):
                    assess_process_window(process,**item)
        with self.assertRaisesRegex(ValueError,"unregistered PrintSpace"):
            assess_process_window("ARBITRARY_LASER_GCODE")
        with self.assertRaisesRegex(ValueError,"unregistered material family"):
            review_directional_material_transition("UNKNOWN","CI")
        with self.assertRaisesRegex(ValueError,"unqualified process"):
            assess_process_window("LASER_DIRECT_WRITE_CANDIDATE",process_contracts={
                "LASER_DIRECT_WRITE_CANDIDATE":{"can_run_physically":True,"needs":["danger"]}
            })

    def test_cycle_and_duplicate_stage_rejected(self):
        altered=copy.deepcopy(self.seeds)
        x=altered["product_variants"][0]["stages"]
        x[0]["depends_on"]=[x[-1]["id"]]
        with self.assertRaisesRegex(ValueError,"cycle"):
            compile_preview(altered)
        altered=copy.deepcopy(self.seeds)
        altered["product_variants"][0]["stages"][1]["id"]=altered["product_variants"][0]["stages"][0]["id"]
        with self.assertRaisesRegex(ValueError,"unique"):
            compile_preview(altered)

    def test_bad_geometry_and_unqualified_data_are_rejected(self):
        for field,value,expected in [
            ("size_mm",[10,-1,20],"positive"),
            ("center_mm",[0,float("nan"),20],"finite"),
            ("size_mm",[10,20],"vectors"),
        ]:
            altered=copy.deepcopy(self.seeds)
            altered["product_variants"][0]["parts"][0][field]=value
            with self.assertRaisesRegex(ValueError,expected):
                compile_preview(altered)
        altered=copy.deepcopy(self.seeds)
        altered["product_variants"][1]["parameters"]["compute_capacity_n"]=4
        with self.assertRaisesRegex(ValueError,"source measurement"):
            compile_preview(altered)
        altered=copy.deepcopy(self.seeds)
        altered["process_contracts"]["LASER_DIRECT_WRITE_CANDIDATE"]["can_run_physically"]=True
        with self.assertRaisesRegex(ValueError,"unqualified"):
            compile_preview(altered)
        altered=copy.deepcopy(self.seeds)
        altered["product_variants"][2]["aesthetic"]["gendered"]=True
        with self.assertRaisesRegex(ValueError,"design choice"):
            compile_preview(altered)

    def test_corrupted_input_stages_and_parts_fail_closed(self):
        altered=copy.deepcopy(self.seeds)
        altered["product_variants"][0]["parts"][0]["stage"]="MADE_UP"
        with self.assertRaisesRegex(ValueError,"unregistered primitive or part stage"):
            compile_preview(altered)
        altered=copy.deepcopy(self.seeds)
        altered["product_variants"][0]["stages"][1]["part_ids"]=["not_present"]
        with self.assertRaisesRegex(ValueError,"unknown or re-used"):
            compile_preview(altered)
        altered=copy.deepcopy(self.seeds)
        altered["product_variants"][0]["parts"][0]["center_mm"][0]=9999
        with self.assertRaisesRegex(ValueError,"outside"):
            compile_preview(altered)

if __name__=="__main__":
    unittest.main()
