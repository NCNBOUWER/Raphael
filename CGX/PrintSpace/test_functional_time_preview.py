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
    compile_i3_track_closure_plan, I3_TRACK_PLAN,
    simulate_adaptive_seed_alternatives, ADAPTIVE_SEED_POLICY, ADAPTIVE_SCENARIO_FIXTURE,
    assess_confirmed_cpu_substitution,
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

    def test_compiled_stage_preview_includes_explicit_process_window_profiles(self):
        result=load_and_compile()
        self.assertEqual(len(result["process_window_profiles"]),7)
        self.assertEqual(len(result["directional_material_catalog_sha256"]),64)
        self.assertEqual(
            result["process_window_profiles"]["LASER_DIRECT_WRITE_CANDIDATE"]["UNKNOWN"]["disposition"],
            "HOLD_SUBSTRATE_STATE_UNRESOLVED")
        wet=result["process_window_profiles"]["MASKED_PHOTOLITHOGRAPHY_CANDIDATE"]["WET_FLOWABLE"]
        self.assertEqual(wet["disposition"],
            "CAN_IF_WET_CHEMISTRY_FOCUS_AND_MASK_COUPONS_VALIDATED")
        self.assertFalse(wet["production_approved"])
        for product in result["products"]:
            for stage in product["frames"]:
                self.assertIsNone(stage["observed_substrate_state"])
                self.assertFalse(stage["stage_process_window_verified"])
                self.assertFalse(stage["qualified_process"])

    def test_butter_bot_replay_retains_unrepresented_source_dependencies(self):
        b=self.products["BB-SOURCE-DEMO"]
        coverage=b["inverse_source_coverage"]
        self.assertEqual(coverage["owner_goal_id"],"BB-FINAL")
        self.assertEqual(len(coverage["graph_sha256"]),64)
        self.assertEqual(len(coverage["required_node_ids"]),8)
        self.assertEqual(coverage["not_geometrically_represented"],
                         ["BB-ACT","BB-VOICE"])
        self.assertEqual(coverage["reference_count"],9)
        self.assertEqual(len(coverage["referenced_node_ids"]),6)
        self.assertFalse(coverage["physical_functional_coverage_verified"])
        self.assertFalse(coverage["qualified_fabrication"])
        self.assertIsNone(self.products["WATCH-ROUND"]["inverse_source_coverage"])
        self.assertIsNone(self.products["WATCH-SQUARE"]["inverse_source_coverage"])

    def test_unregistered_or_wrong_owner_source_dependency_fails_closed(self):
        bad=copy.deepcopy(self.seeds)
        bad["product_variants"][0]["parts"][0]["source_dependency_node_ref"]="PC-C0"
        with self.assertRaisesRegex(ValueError,"foreign or unregistered"):
            compile_preview(bad)
        bad=copy.deepcopy(self.seeds)
        bad["product_variants"][0]["source_goal_node"]="BB-GOAL-MISSING"
        with self.assertRaisesRegex(ValueError,"missing or duplicate inverse"):
            compile_preview(bad)
        bad=copy.deepcopy(self.seeds)
        del bad["product_variants"][0]["source_goal_node"]
        with self.assertRaisesRegex(ValueError,"require registered inverse goal"):
            compile_preview(bad)


    def test_intel_i3_is_real_sourced_core_with_separate_safety_controller(self):
        route=compile_i3_track_closure_plan()
        self.assertEqual(route["schema"],
                         "cgx.printspace.butterbot_i3_track_closure_compiled.v0.1")
        self.assertEqual(route["cpu"]["core_family"],"Intel Core i3")
        self.assertIsNone(route["cpu"]["exact_sku"])
        self.assertEqual(route["cpu"]["safety_control"],
                         "SEPARATE_DETERMINISTIC_MCU")
        self.assertEqual(route["stage_count"],28)
        self.assertEqual(len(route["source_sha256"]),64)
        self.assertIsNone(route["cpu"]["processor_tdp_w"])
        self.assertIsNone(route["cpu"]["battery_wh"])
        self.assertFalse(route["factory_production_authorized"])
        self.assertFalse(route["physical_machine_motion_simulated"])
        kinds={x["id"]:x for x in route["source_components"]}
        for ident in ("i3_module","safety_MCU","battery_pack","motor_left",
                      "motor_right","servo_pack","speaker_and_LEDs"):
            self.assertEqual(kinds[ident]["kind"],"SOURCED")
            self.assertFalse(kinds[ident]["can_print"])

    def test_open_tracks_have_only_stock_allowance_and_close_last(self):
        route=compile_i3_track_closure_plan()
        tracks=route["track"]
        self.assertAlmostEqual(tracks["allowance"]["value"],0.10)
        self.assertIn("BELT_OPERATING_STRAIN",tracks["allowance"]["applies_not_to"])
        self.assertIsNone(tracks["force_target_n"])
        self.assertEqual([x["id"] for x in tracks["closure_modes"] if x["default"]],
                         ["MECHANICAL_PIN_AND_IDLER"])
        ids=route["ordered_stages"]
        idx=lambda item:ids.index(item)
        self.assertLess(idx("S02_LOWER_TRACK_LEFT_10PCT"),
                        idx("S04_PRINT_CHASSIS_AND_CRADLE"))
        self.assertLess(idx("S03_LOWER_TRACK_RIGHT_10PCT"),
                        idx("S04_PRINT_CHASSIS_AND_CRADLE"))
        for step in ("S06_INSTALL_BEARINGS_AXLES","S07_INSTALL_TRACK_DRIVE_MOTORS",
                     "S13_INSTALL_I3_MODULE","S14_BATTERY_AND_REGULATORS",
                     "S17_VOICE_LED","S18_DRY_ASSEMBLY_INSPECTION",
                     "S19_MEASURE_FINAL_TRACK_ROUTE"):
            self.assertLess(idx(step),idx("S21_CLOSE_LEFT_TRACK"))
        self.assertLess(idx("S21_CLOSE_LEFT_TRACK"),idx("S22_LEFT_COOL_RELAX_INSPECT"))
        self.assertLess(idx("S22_LEFT_COOL_RELAX_INSPECT"),idx("S24_CLOSE_RIGHT_TRACK"))
        self.assertLess(idx("S24_CLOSE_RIGHT_TRACK"),idx("S25_RIGHT_COOL_RELAX_INSPECT"))
        self.assertLess(idx("S25_RIGHT_COOL_RELAX_INSPECT"),idx("S26_FINAL_C0_TEST"))
        self.assertLess(idx("S16_HEAD_SHELL"),idx("S13_INSTALL_I3_MODULE"))
        self.assertLess(idx("S16_HEAD_SHELL"),idx("S14_BATTERY_AND_REGULATORS"))

    def test_two_arms_alternate_tension_and_join_only_as_planned(self):
        frames=compile_i3_track_closure_plan()["frames"]
        left=next(x for x in frames if x["stage_id"]=="S21_CLOSE_LEFT_TRACK")
        right=next(x for x in frames if x["stage_id"]=="S24_CLOSE_RIGHT_TRACK")
        self.assertEqual((left["tension_arm"],left["joining_arm"]),("ARM_A","ARM_B"))
        self.assertEqual((right["tension_arm"],right["joining_arm"]),("ARM_B","ARM_A"))
        self.assertEqual(left["closure_side"],"LEFT")
        self.assertEqual(right["closure_side"],"RIGHT")
        self.assertFalse(left["track_right_closed_candidate"])
        self.assertTrue(right["track_left_closed_candidate"])
        self.assertTrue(right["track_right_closed_candidate"])
        self.assertFalse(left["joint_strength_verified"])
        self.assertIsNone(left["force_measured_n"])
        self.assertIsNone(right["time_s"])
        self.assertFalse(right["physical_execution_approved"])

    def test_each_station_travel_is_symbolic_and_unapproved(self):
        route=compile_i3_track_closure_plan()
        self.assertEqual(len(route["station_metadata"]),14)
        self.assertTrue(all(s["physical_position_mm"] is None
                            for s in route["station_metadata"].values()))
        for idx,frame in enumerate(route["frames"]):
            self.assertEqual(frame["step"],idx+1)
            self.assertIn(frame["from_station"],route["station_metadata"])
            self.assertIn(frame["to_station"],route["station_metadata"])
            self.assertIsNone(frame["travel_mm"])
            self.assertIsNone(frame["cartesian_path"])
            self.assertIsNone(frame["force_target_n"])
            self.assertFalse(frame["tool_reachability_verified"])
            self.assertFalse(frame["physical_execution_approved"])
        self.assertEqual(len(set(route["ordered_stages"])),len(route["ordered_stages"]))
        self.assertEqual(route,compile_i3_track_closure_plan())
        bb=self.products["BB-SOURCE-DEMO"]
        self.assertEqual(bb["i3_track_build_route"]["source_sha256"],route["source_sha256"])
        self.assertIsNone(self.products["WATCH-SQUARE"]["i3_track_build_route"])

    def test_unsafe_hot_tracks_after_cpu_and_unqualified_force_are_rejected(self):
        source=json.loads(Path(I3_TRACK_PLAN).read_text(encoding="utf-8"))
        variants=[
          ("S21_CLOSE_LEFT_TRACK",{"tension_arm":"ARM_B"},"handoff"),
          ("S24_CLOSE_RIGHT_TRACK",{"toolhead_conflict_guard":False},"collision guard"),
          ("S21_CLOSE_LEFT_TRACK",{"temperature_guard":""},"hot welding"),
          ("S16_HEAD_SHELL",{"depends_on":["S14_BATTERY_AND_REGULATORS"]},"cycle"),
        ]
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            candidate=Path(tmp)/"draft.json"
            for stage_id,mutation,msg in variants:
                with self.subTest(stage_id=stage_id,msg=msg):
                    changed=copy.deepcopy(source)
                    target=next(s for s in changed["steps"] if s["id"]==stage_id)
                    target.update(mutation)
                    candidate.write_text(json.dumps(changed),encoding="utf-8")
                    with self.assertRaisesRegex(ValueError,msg):
                        compile_i3_track_closure_plan(candidate)
            changed=copy.deepcopy(source)
            changed["track_plan"]["allowance"]["applies_to"]="FINAL_BELT_OPERATING_STRAIN"
            candidate.write_text(json.dumps(changed),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"track allowance"):
                compile_i3_track_closure_plan(candidate)
            changed=copy.deepcopy(source)
            changed["host_i3_seed"]["exact_sku"]="i3-13100"
            candidate.write_text(json.dumps(changed),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"SKU"):
                compile_i3_track_closure_plan(candidate)
            changed=copy.deepcopy(source)
            changed["source_components"][0]["can_print"]=True
            candidate.write_text(json.dumps(changed),encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"unprintable"):
                compile_i3_track_closure_plan(candidate)


    def test_three_adaptive_tiers_pick_threshold_driven_substitutions(self):
        result=simulate_adaptive_seed_alternatives()
        self.assertEqual(result["tier_count"],3)
        self.assertTrue(result["scenario_only"])
        self.assertFalse(result["physical_process_qualified"])
        self.assertFalse(result["closed_chamber_fabrication_accepted"])
        self.assertEqual(len(result["policy_sha256"]),64)
        self.assertEqual(len(result["scenario_sha256"]),64)
        selected=[x["selection"] for x in result["results"]]
        self.assertEqual([x["tier_id"] for x in result["results"]],
                         ["BOOTSTRAP_EVERYDAY","PRO_BALANCED","INDUSTRIAL_CIRCULAR"])
        self.assertEqual([x["id"] for x in selected],[
            "HYPOTHETICAL_LOW_POWER_I3",
            "HYPOTHETICAL_COMPACT_I5",
            "HYPOTHETICAL_PERFORMANCE_I5"
        ])
        self.assertEqual([r["stage_count"] for r in result["results"]],[28,30,32])
        self.assertEqual([x["family"] for x in selected],["i3","i5","i5"])
        self.assertTrue(all(x["actual_CPU_SKU"] is None for x in result["results"]))
        self.assertEqual(result,simulate_adaptive_seed_alternatives())

    def test_bootstrap_keeps_budget_and_runtime_thresholds_over_cpu_badge(self):
        result=simulate_adaptive_seed_alternatives()
        bootstrap=result["results"][0]
        low_power=bootstrap["selection"]
        self.assertEqual(low_power["family"],"i3")
        self.assertAlmostEqual(low_power["ideal_arithmetic_runtime_h"],3)
        self.assertEqual(low_power["scenario_cost_aud"],90)
        rejects={x["id"]:x["rejected_thresholds"] for x in bootstrap["alternatives"]}
        self.assertIn("IDEAL_RUNTIME_BELOW_TIER_MINIMUM",
                      rejects["HYPOTHETICAL_RECYCLED_I3"])
        self.assertIn("ACQUISITION_COST_EXCEEDS_ASSUMED_AVAILABLE_BUDGET",
                      rejects["HYPOTHETICAL_COMPACT_I5"])
        self.assertFalse(bootstrap["actual_device_selection_approved"])
        self.assertFalse(bootstrap["actual_sealed_session_verified"])

    def test_three_tiers_overlay_original_28_stages_without_changing_safety(self):
        original=compile_i3_track_closure_plan()
        result=simulate_adaptive_seed_alternatives()
        for tier in result["results"]:
            frames=tier["frames"]
            real_ids=[f["stage_id"] for f in frames
                      if f["mode"]=="BASE_28_STAGE_ROUTE"]
            self.assertEqual(real_ids,original["ordered_stages"])
            self.assertEqual(len({f["stage_id"] for f in frames}),len(frames))
            self.assertEqual(frames[-1]["progress_fraction"],1)
            self.assertTrue(all(f["travel_mm"] is None for f in frames))
            self.assertTrue(all(f["physical_execution_approved"] is False for f in frames))
            overlays=[f for f in frames
                      if f["mode"]=="OPTIONAL_REVIEW_HOLD_NOT_HARDWARE_OPERATION"]
            self.assertEqual(len(overlays),tier["stage_count"]-28)
            self.assertFalse(tier["fully_printable"])
            self.assertFalse(tier["actual_device_selection_approved"])
            self.assertEqual(tier["source_component_class_count"],19)
            self.assertTrue(0<tier["candidate_print_class_fraction"]<1)
            self.assertTrue(tier["unknown_physical_print_fraction"])
        self.assertEqual(original,compile_i3_track_closure_plan())

    def test_threshold_inputs_refuse_fake_source_approval_or_offline_session(self):
        from tempfile import TemporaryDirectory
        policy=json.loads(Path(ADAPTIVE_SEED_POLICY).read_text(encoding="utf-8"))
        fixture=json.loads(Path(ADAPTIVE_SCENARIO_FIXTURE).read_text(encoding="utf-8"))
        with TemporaryDirectory() as tmp:
            p=Path(tmp)/"policy.json"
            s=Path(tmp)/"scenario.json"
            variants=[
                ({"type":"policy","change":lambda x:x["tiers"][0]["weights"].__setitem__("cost",0.90)}, "sum to one"),
                ({"type":"policy","change":lambda x:x["tiers"][1].__setitem__("sealed_session_mandatory",False)}, "sealed session"),
                ({"type":"fixture","change":lambda x:x["candidates"][0].__setitem__("exact_cpu_sku","i3-13100")}, "remain unverified"),
                ({"type":"fixture","change":lambda x:x["candidates"][0].__setitem__("cooling_capacity_w",float("nan"))}, "finite"),
                ({"type":"fixture","change":lambda x:x["tier_snapshots"][0].__setitem__("internally_preloaded_sourced_trays",False)}, "sealed session"),
                ({"type":"policy","change":lambda x:x["tiers"][2]["stage_insertions"][0].__setitem__("qualified",True)}, "unqualified"),
            ]
            for item,errmsg in variants:
                with self.subTest(item=errmsg):
                    data1=copy.deepcopy(policy)
                    data2=copy.deepcopy(fixture)
                    if item["type"]=="policy":
                        item["change"](data1)
                    else:
                        item["change"](data2)
                    p.write_text(json.dumps(data1),encoding="utf-8")
                    s.write_text(json.dumps(data2),encoding="utf-8")
                    with self.assertRaisesRegex(ValueError,errmsg):
                        simulate_adaptive_seed_alternatives(p,s)

    def test_printing_coverage_target_is_not_claimed_when_modules_sourced(self):
        result=simulate_adaptive_seed_alternatives()
        a=result["results"][-1]
        self.assertLess(a["candidate_print_class_fraction"],a["target_print_fraction"])
        self.assertEqual(a["all_component_printable_target_gate"],
                         "HOLD_UNTIL_SOURCED_CHIPS_BATTERY_MOTORS_PRECISION_CLAIM_QUALIFIED")
        self.assertFalse(a["actual_sealed_session_verified"])
        self.assertFalse(a["real_battery_runtime_verified"])
        self.assertFalse(a["toolpaths_and_simulated_physics_verified"])
        self.assertEqual(a["release_status"],
                         "DIGITAL_SCENARIO_ONLY_NO_PURCHASING_OR_HARDWARE_AUTHORITY")

    def test_confirmed_processor_intake_stays_held_when_unmeasured(self):
        result=assess_confirmed_cpu_substitution(
            "PRO_BALANCED",{"cpu_family":"i5","cpu_sku":"user-reported-i5-model"})
        self.assertEqual(result["disposition"],"HOLD_INPUTS_PENDING")
        self.assertIn("processor_peak_power_w",result["incomplete_required_inputs"])
        self.assertIn("module_xyz_mm",result["incomplete_required_inputs"])
        self.assertIn("source_reference",result["incomplete_required_inputs"])
        self.assertFalse(result["approved_to_build"])
        self.assertFalse(result["approved_to_purchase"])
        self.assertFalse(result["actual_source_identity_cryptographically_verified"])

    def test_submitted_i5_can_clear_math_without_manufacture_approval(self):
        supplied={
            "cpu_family":"i5","cpu_sku":"SOURCE_REPORTED_SKU",
            "source_reference":"owner:attachment:part_passport_candidate",
            "module_xyz_mm":[120,105,42],
            "machine_internal_envelope_mm":[190,165,135],
            "margin_mm":[10,10,7],
            "processor_peak_power_w":74,
            "cooling_capacity_w":90,
            "average_system_power_w":28,
            "battery_capacity_wh":96,
            "workload_score_n":210,
            "baseline_i3_workload_n":100,
            "incremental_cost_aud":175,
            "available_budget_aud":260,
            "registered_machine_cells":["FDM","PICK","INSPECT","SEALED_TRAYS",
                                        "TOOLCHANGE","VISION","SENSOR_FEEDBACK"],
            "internal_sourced_tray_preloaded":True,
        }
        result=assess_confirmed_cpu_substitution("PRO_BALANCED", supplied)
        self.assertEqual(result["disposition"],
                         "ARITHMETIC_AND_DECLARED_DIMENSION_THRESHOLDS_ONLY")
        self.assertEqual(result["derived_metric_candidates"]["required_body_cavity_mm"],
                         [140,125,56])
        self.assertAlmostEqual(result["derived_metric_candidates"]["ideal_runtime_h"],
                               96/28,places=4)
        self.assertEqual(result["derived_metric_candidates"]["thermal_peak_headroom_w"],16)
        self.assertAlmostEqual(result["derived_metric_candidates"]["i5_gain_ratio_to_supplied_i3"],2.1)
        self.assertEqual(result["rejected_thresholds"],[])
        self.assertFalse(result["actual_source_identity_cryptographically_verified"])
        self.assertFalse(result["approved_to_build"])
        self.assertFalse(result["approved_to_purchase"])
        self.assertFalse(result["approved_to_actuate"])

    def test_upgraded_cpu_cannot_bypass_thermal_cash_or_sealed_chamber(self):
        intake={
            "cpu_family":"i5","cpu_sku":"CANDIDATE",
            "source_reference":"user:part-record",
            "module_xyz_mm":[160,120,80],
            "machine_internal_envelope_mm":[155,125,75],
            "margin_mm":[12,12,8],
            "processor_peak_power_w":150,
            "cooling_capacity_w":70,
            "average_system_power_w":70,
            "battery_capacity_wh":70,
            "workload_score_n":180,
            "baseline_i3_workload_n":160,
            "incremental_cost_aud":700,
            "available_budget_aud":80,
            "registered_machine_cells":["FDM","PICK"],
            "internal_sourced_tray_preloaded":False,
        }
        result=assess_confirmed_cpu_substitution("PRO_BALANCED",intake)
        self.assertEqual(result["disposition"],"REJECT_OR_REDESIGN_CONSTRAINTS")
        reasons=result["rejected_thresholds"]
        for reason in ("THERMAL_PEAK_OVERRUN","ACTUAL_MODULE_ENVELOPE_REQUIRES_BODY_REDIMENSION",
                       "I5_GAIN_NOT_WORTH_UPGRADE_BY_POLICY",
                       "PRICE_EXCEEDS_TIER_CAP_OR_AVAILABLE_CASH",
                       "NECESSARY_MACHINE_CELLS_NOT_PRESENT",
                       "SEALED_SESSION_CANNOT_USE_EXTERNAL_INSERTION"):
            self.assertIn(reason,reasons)
        self.assertFalse(result["approved_to_build"])

    def test_source_substitution_intake_rejects_fabricated_fields_and_nonfinite(self):
        with self.assertRaisesRegex(ValueError,"unregistered hardware intake"):
            assess_confirmed_cpu_substitution("BOOTSTRAP_EVERYDAY",
                {"cpu_family":"i5","owner_override_safety":True})
        with self.assertRaisesRegex(ValueError,"unknown Butter Bot threshold tier"):
            assess_confirmed_cpu_substitution("UNREGISTERED",{})
        result=assess_confirmed_cpu_substitution("INDUSTRIAL_CIRCULAR",
            {"cpu_family":"i7","cpu_sku":"fantasy", "battery_capacity_wh":float("nan")})
        self.assertIn("UNREGISTERED_CPU_FAMILY",result["rejected_thresholds"])
        self.assertIn("INVALID_NUMERIC_BATTERY_CAPACITY_WH",result["rejected_thresholds"])
        self.assertFalse(result["approved_to_publish"])

    def test_report_cli_and_nullable_donor_template_are_source_safe(self):
        import subprocess
        import sys
        from functional_time_preview import HERE
        submitted=json.loads((HERE/"BUTTERBOT_CPU_SUBSTITUTION_INTAKE_v0_1.json").read_text(encoding="utf-8"))
        assessment=assess_confirmed_cpu_substitution("PRO_BALANCED",submitted)
        self.assertEqual(assessment["disposition"],"HOLD_INPUTS_PENDING")
        self.assertFalse(assessment["approved_to_build"])
        p=subprocess.run([sys.executable,str(HERE/"functional_time_preview.py"),
                          "--adaptive-summary"],capture_output=True,text=True,
                         timeout=12,check=True)
        data=json.loads(p.stdout)
        self.assertEqual(data["tier_count"],3)
        self.assertTrue(data["scenario_only"])
        self.assertEqual([x["selection"]["family"] for x in data["results"]],
                         ["i3","i5","i5"])
        self.assertTrue(all("frames" not in x for x in data["results"]))
        self.assertTrue(all(x["actual_device_selection_approved"] is False
                            for x in data["results"]))
        self.assertFalse(data["physical_process_qualified"])

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
