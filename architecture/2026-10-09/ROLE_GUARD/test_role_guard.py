"""Synthetic-only regressions: no research pixels, references, RNG or network."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import unittest
from shapely.geometry import box, Polygon
from role_guard import (Actor, Denied, Evidence, EvaluationGate, ExposureEvent,
                        NativeWindow, PixelScope, Role, Selection,
                        append_exposure, check_access, check_native_window,
                        derive, validate_blinded_packet, verify_exposure_extension)


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.meta = Evidence("meta", Role.METADATA, Role.METADATA)
        self.aux = Evidence("aux", Role.AUXILIARY, Role.AUXILIARY)
        self.dev = Evidence("dev", Role.DEV_REFERENCE, Role.DEV_REFERENCE,
                            independent_measurement=True, acquisition_utc="2018-01-12T02:00:00Z")
        self.final = Evidence("final", Role.FINAL_REFERENCE, Role.FINAL_REFERENCE,
                              Selection.FINAL_PROBABILITY, independent_measurement=True,
                              acquisition_utc="2018-01-12T02:00:00Z")
        self.gate = EvaluationGate("candidate", "sha-candidate", "sha-protocol", "lock",
                                   "reference-release", "sha-candidate", "responses-locked", "join-release")
        self.packet = {"neutral_id":"R01", "geometry":{"type":"Point", "coordinates":[0,0],
                       "crs":"EPSG:32750"}, "support_m":30,
                       "target_acquisition_utc":"2018-01-12T02:00:00Z", "protocol_version":"v1",
                       "optical_observations":[{"image":"images/R01_optical.png",
                         "acquisition_utc":"2018-01-12T03:00:00Z", "sensor":"S2",
                         "native_resolution_m":10, "display_pipeline_id":"display-v1",
                         "registration_context":{"status":"UNKNOWN", "uncertainty_m":None}}]}

    def test_population_metadata_allowed(self):
        self.assertIn("NO_IO", check_access(self.meta, Actor.DEVELOPER))

    def test_sampling_auxiliary_allowed(self):
        self.assertIn("NO_IO", check_access(self.aux, Actor.DEVELOPER))

    def test_detector_discovery_dev_allowed(self):
        e = replace(self.dev, selection=Selection.DETECTOR)
        self.assertIn("NO_IO", check_access(e, Actor.DEVELOPER))
        self.assertIn("DETECTOR_DISCOVERY", e.effective_taints)

    def test_disagreement_discovery_dev_allowed(self):
        e = replace(self.dev, selection=Selection.DISAGREEMENT)
        self.assertIn("NO_IO", check_access(e, Actor.READER, blinded_packet=True))

    def test_detector_discovery_cannot_become_auxiliary(self):
        with self.assertRaises(Denied):
            check_access(replace(self.aux, selection=Selection.DETECTOR), Actor.DEVELOPER)

    def test_detector_discovery_does_not_create_independent_response(self):
        with self.assertRaises(Denied):
            check_access(replace(self.dev, selection=Selection.DISAGREEMENT,
                                 independent_measurement=False), Actor.DEVELOPER)

    def test_dev_promotion_blocked(self):
        with self.assertRaises(Denied):
            derive(self.dev, artifact_id="fake-final", role=Role.FINAL_REFERENCE)

    def test_transitive_dev_taint_survives(self):
        intermediate = derive(self.dev, artifact_id="intermediate", role=Role.ENGINEERING)
        self.assertIn("DEVELOPMENT_LABEL", intermediate.effective_taints)
        with self.assertRaises(Denied):
            derive(intermediate, artifact_id="fake-final", role=Role.FINAL_REFERENCE)

    def test_explicit_inherited_dev_taint_blocks_final(self):
        with self.assertRaises(Denied):
            check_access(replace(self.final, taints=frozenset({"DEVELOPMENT"})), Actor.CUSTODIAN, self.gate)

    def test_legacy_answer_reuse_blocked(self):
        with self.assertRaises(Denied):
            check_access(replace(self.final, reused_development_response=True), Actor.CUSTODIAN, self.gate)

    def test_auxiliary_cannot_masquerade_as_reference(self):
        with self.assertRaises(Denied):
            check_access(replace(self.final, origin_role=Role.AUXILIARY), Actor.CUSTODIAN, self.gate)

    def test_engineering_cannot_masquerade_as_reference(self):
        with self.assertRaises(Denied):
            check_access(replace(self.dev, origin_role=Role.ENGINEERING), Actor.DEVELOPER)

    def test_final_reference_requires_probability_selection(self):
        with self.assertRaises(Denied):
            check_access(replace(self.final, selection=Selection.INDEPENDENT), Actor.CUSTODIAN, self.gate)

    def test_final_reference_sealed_without_lock(self):
        with self.assertRaises(Denied):
            check_access(self.final, Actor.CUSTODIAN)

    def test_final_reference_sealed_without_release(self):
        with self.assertRaises(Denied):
            check_access(self.final, Actor.CUSTODIAN, replace(self.gate, release_record_id=None))

    def test_candidate_digest_mismatch_denied(self):
        with self.assertRaises(Denied):
            check_access(self.final, Actor.CUSTODIAN, replace(self.gate, release_candidate_digest="other"))

    def test_retired_test_cannot_be_released_as_fresh(self):
        with self.assertRaises(Denied):
            check_access(self.final, Actor.CUSTODIAN, replace(self.gate, retired_for_current_candidate=True))

    def test_developer_final_access_denied_even_after_release(self):
        with self.assertRaises(Denied):
            check_access(self.final, Actor.DEVELOPER, self.gate)

    def test_custodian_final_access_after_lock_release(self):
        self.assertIn("NO_IO", check_access(self.final, Actor.CUSTODIAN, self.gate))

    def test_blind_reader_after_release(self):
        self.assertIn("NO_IO", check_access(self.final, Actor.READER, self.gate, blinded_packet=True))

    def test_reader_cannot_browse_auxiliary(self):
        with self.assertRaises(Denied):
            check_access(self.aux, Actor.READER, blinded_packet=True)

    def test_reader_cannot_read_unblinded_reference(self):
        with self.assertRaises(Denied):
            check_access(self.dev, Actor.READER)

    def test_reader_cannot_view_prediction(self):
        pred = Evidence("pred", Role.FINAL_PREDICTION, Role.FINAL_PREDICTION)
        with self.assertRaises(Denied):
            check_access(pred, Actor.READER, self.gate, blinded_packet=True)

    def test_custodian_prediction_before_reference_release(self):
        pred = Evidence("pred", Role.FINAL_PREDICTION, Role.FINAL_PREDICTION)
        gate = EvaluationGate("candidate", "sha-candidate", "sha-protocol", "lock",
                               prediction_authorization_record_id="processing-authorized",
                               prediction_candidate_digest="sha-candidate")
        self.assertIn("NO_IO", check_access(pred, Actor.CUSTODIAN, gate))
        with self.assertRaises(Denied):
            check_access(self.final, Actor.CUSTODIAN, gate)

    def test_prediction_lock_without_processing_authorization_denied(self):
        pred = Evidence("pred", Role.FINAL_PREDICTION, Role.FINAL_PREDICTION)
        with self.assertRaises(Denied):
            check_access(pred, Actor.CUSTODIAN, self.gate)

    def test_prediction_authorization_digest_mismatch_denied(self):
        pred = Evidence("pred", Role.FINAL_PREDICTION, Role.FINAL_PREDICTION)
        gate = replace(self.gate, prediction_authorization_record_id="processing-authorized",
                        prediction_candidate_digest="other-candidate")
        with self.assertRaises(Denied):
            check_access(pred, Actor.CUSTODIAN, gate)

    def test_prediction_analyst_join_still_requires_reference_release(self):
        pred = Evidence("pred", Role.FINAL_PREDICTION, Role.FINAL_PREDICTION)
        gate = EvaluationGate("candidate", "sha-candidate", "sha-protocol", "lock",
                               prediction_authorization_record_id="processing-authorized",
                               prediction_candidate_digest="sha-candidate")
        with self.assertRaises(Denied):
            check_access(pred, Actor.ANALYST, gate)

    def test_prediction_analyst_access_after_all_required_releases(self):
        pred = Evidence("pred", Role.FINAL_PREDICTION, Role.FINAL_PREDICTION)
        gate = replace(self.gate, prediction_authorization_record_id="processing-authorized",
                        prediction_candidate_digest="sha-candidate")
        self.assertIn("NO_IO", check_access(pred, Actor.ANALYST, gate))

    def test_final_join_requires_response_lock(self):
        with self.assertRaises(Denied):
            check_access(self.final, Actor.ANALYST, replace(self.gate, response_lock_record_id=None))

    def test_final_join_requires_analysis_release(self):
        with self.assertRaises(Denied):
            check_access(self.final, Actor.ANALYST, replace(self.gate, analysis_release_record_id=None))

    def test_final_join_allowed_after_both_locks(self):
        self.assertIn("NO_IO", check_access(self.final, Actor.ANALYST, self.gate))

    def test_neutral_geometry_times_and_registration_allowed(self):
        validate_blinded_packet(self.packet)

    def test_packet_rejects_detector_strata_first_reader_fields(self):
        for field in ("detector_values", "candidate_id", "sampling_stratum", "first_reader",
                      "ab_disagreement", "expected_state", "discovery_reason", "hidden_key"):
            with self.subTest(field=field), self.assertRaises(Denied):
                validate_blinded_packet(dict(self.packet, **{field:"leak"}))

    def test_packet_nested_unapproved_field_rejected(self):
        packet = deepcopy(self.packet)
        packet["optical_observations"][0]["detector_values"] = [0]
        with self.assertRaises(Denied):
            validate_blinded_packet(packet)

    def test_packet_image_path_cannot_expose_stratum_folder(self):
        packet = deepcopy(self.packet)
        packet["optical_observations"][0]["image"] = "P1_water/R01_optical.png"
        with self.assertRaises(Denied):
            validate_blinded_packet(packet)

    def test_packet_image_path_cannot_encode_expected_water_state(self):
        packet = deepcopy(self.packet)
        packet["optical_observations"][0]["image"] = "images/R01_water.png"
        with self.assertRaises(Denied):
            validate_blinded_packet(packet)

    def test_packet_ids_neutral(self):
        with self.assertRaises(Denied):
            validate_blinded_packet(dict(self.packet, neutral_id="WATER_01"))

    def test_exposure_append_preserves_unknown(self):
        original = (ExposureEvent("incident", "UNVIEWED_EXTENT_UNKNOWN", "unviewed preview"),)
        extension = append_exposure(original, ExposureEvent("observation", "ADDITIONAL_OBSERVATION",
                                                            "more provenance, no retrospective clearance", "incident"))
        verify_exposure_extension(original, extension)
        self.assertEqual(extension[0], original[0])

    def test_exposure_clear_denied(self):
        with self.assertRaises(Denied):
            append_exposure((), ExposureEvent("incident", "CLEARED", "not supported"))

    def test_exposure_mutation_denied(self):
        original = (ExposureEvent("incident", "UNVIEWED_EXTENT_UNKNOWN", "unviewed preview"),)
        with self.assertRaises(Denied):
            verify_exposure_extension(original, (replace(original[0], status="EXPOSED"),))

    def test_exposure_removal_denied(self):
        original = (ExposureEvent("incident", "EXPOSED", "old incident"),)
        with self.assertRaises(Denied):
            verify_exposure_extension(original, ())


class NativeWindowTests(unittest.TestCase):
    def setUp(self):
        self.artifact = Evidence("pixels", Role.ENGINEERING, Role.ENGINEERING)
        self.scope = PixelScope("synthetic-scope", Role.ENGINEERING, "pixels", "EPSG:32750",
                                box(0,0,1000,1000), operation_authorization_record="SYNTHETIC_ONLY")
        self.transform = (0,10,0,1000,0,-10)

    def call(self, window=NativeWindow(20,20,23,23), **kwargs):
        settings = {"e":self.artifact, "actor":Actor.DEVELOPER, "scope":self.scope,
                    "window":window, "transform":self.transform, "source_crs":"EPSG:32750",
                    "source_width":100, "source_height":100}
        settings.update(kwargs)
        return check_native_window(**settings)

    def test_safe_rounding_halo_padding_combined(self):
        result = self.call(NativeWindow(20.2,20.2,22.8,22.8), halo=2, padding=1)
        self.assertEqual(result["native_window"], [17,17,26,26])

    def test_missing_operation_authorization_denied(self):
        with self.assertRaises(Denied):
            self.call(scope=replace(self.scope, operation_authorization_record=None))

    def test_role_scope_binding_no_global_bypass(self):
        aux_scope = replace(self.scope, role=Role.AUXILIARY)
        with self.assertRaises(Denied):
            self.call(scope=aux_scope)

    def test_artifact_scope_binding(self):
        with self.assertRaises(Denied):
            self.call(scope=replace(self.scope, artifact_id="other"))

    def test_full_population_aux_scope_not_dev_permission(self):
        aux = Evidence("aux", Role.AUXILIARY, Role.AUXILIARY)
        scope = replace(self.scope, role=Role.AUXILIARY, artifact_id="aux")
        self.call(e=aux, scope=scope)
        with self.assertRaises(Denied):
            self.call(scope=scope)

    def test_metadata_role_cannot_request_pixels(self):
        e = Evidence("meta", Role.METADATA, Role.METADATA)
        with self.assertRaises(Denied):
            self.call(e=e, scope=replace(self.scope, role=Role.METADATA, artifact_id="meta"))

    def test_edge_window_regression_rounding_padding_before_read(self):
        # Requested display footprint ends at x=498, but ceil -> 500 and
        # one-pixel padding -> 510. Protected region begins at x=500.
        scope = replace(self.scope, authorized_geometry=box(0,0,500,1000),
                        prohibited_geometry=box(500,0,1000,1000))
        read_calls = []
        def fake_read():
            self.call(NativeWindow(47.1,20.1,49.8,22.9), scope=scope, padding=1)
            read_calls.append("FAKE_NO_PIXELS")
        with self.assertRaises(Denied):
            fake_read()
        self.assertEqual(read_calls, [])

    def test_halo_crossing_blocked(self):
        scope = replace(self.scope, authorized_geometry=box(200,700,300,800))
        with self.assertRaises(Denied):
            self.call(scope=scope, halo=1)

    def test_mask_hole_blocks_bbox_shortcut(self):
        allowed = box(0,0,1000,1000).difference(box(210,760,240,790))
        with self.assertRaises(Denied):
            self.call(scope=replace(self.scope, authorized_geometry=allowed))

    def test_exact_prohibited_boundary_contact_denied(self):
        scope = replace(self.scope, prohibited_geometry=box(230,0,1000,1000))
        with self.assertRaises(Denied):
            self.call(scope=scope)

    def test_source_extent_excess_denied(self):
        with self.assertRaises(Denied):
            self.call(NativeWindow(0,0,3,3), padding=1)

    def test_crs_mismatch_denied(self):
        with self.assertRaises(Denied):
            self.call(source_crs="EPSG:4326")

    def test_rotated_transform_corner_polygon_used(self):
        result = self.call(transform=(0,10,2,1000,1,-10))
        self.assertEqual(result["native_window"], [20,20,23,23])

    def test_singular_transform_denied(self):
        with self.assertRaises(Denied):
            self.call(transform=(0,10,20,0,5,10))

    def test_invalid_geometry_denied(self):
        polygon = Polygon([(0,0),(1000,1000),(0,1000),(1000,0),(0,0)])
        with self.assertRaises(Denied):
            self.call(scope=replace(self.scope, authorized_geometry=polygon))

    def test_negative_halo_denied(self):
        with self.assertRaises(Denied):
            self.call(halo=-1)

    def test_empty_window_denied(self):
        with self.assertRaises(Denied):
            self.call(NativeWindow(5,5,5,9))

    def test_unknown_final_scope_cannot_unseal(self):
        e = Evidence("final", Role.FINAL_REFERENCE, Role.FINAL_REFERENCE,
                     Selection.FINAL_PROBABILITY, independent_measurement=True, acquisition_utc="2018-01-12Z")
        scope = replace(self.scope, role=Role.FINAL_REFERENCE, artifact_id="final")
        with self.assertRaises(Denied):
            self.call(e=e, actor=Actor.CUSTODIAN, scope=scope)


class RecordingResult(unittest.TextTestResult):
    def startTest(self, test):
        super().startTest(test)
        self.case_ids.append(test.id())


if __name__ == "__main__":
    import sys
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    RecordingResult.case_ids = []
    result = unittest.TextTestRunner(verbosity=1, resultclass=RecordingResult).run(suite)
    out = Path(__file__).parent / "SYNTHETIC_ROLE_GUARD_RESULTS.json"
    payload = {"status":"PASS" if result.wasSuccessful() else "FAIL",
               "test_methods":result.testsRun, "failures":len(result.failures), "errors":len(result.errors),
               "test_ids":result.case_ids, "scope":"SYNTHETIC_ONLY_NO_RESEARCH_IO",
               "limitations":["Policy assertions are not authentication or independent verification.",
                              "No production caller integrated; no acquisition authorization issued.",
                              "Packet image pixels and free-text semantics are not automatically inspected."]}
    out.write_text(json.dumps(payload, indent=2)+"\n", encoding="utf-8")
    raise SystemExit(0 if result.wasSuccessful() else 1)
