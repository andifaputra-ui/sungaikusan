"""Offline C2 workflow policy checks. These functions perform no file/network pixel IO.

Assertions about provenance, actors, locks and authorization must be supplied by a
trusted workflow. This module is not an authentication or cryptographic boundary.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from math import ceil, floor, isfinite
import re
from typing import Any, FrozenSet


class Denied(ValueError):
    pass


class Role(str, Enum):
    METADATA = "POPULATION_METADATA"
    AUXILIARY = "SAMPLING_DISCOVERY_AUXILIARY"
    ENGINEERING = "DEVELOPMENT_ENGINEERING"
    DEV_REFERENCE = "DEVELOPMENT_REFERENCE"
    FINAL_REFERENCE = "SEALED_FINAL_REFERENCE"
    FINAL_PREDICTION = "LOCKED_FINAL_PREDICTION"


class Actor(str, Enum):
    DEVELOPER = "DEVELOPER"
    CUSTODIAN = "CUSTODIAN"
    READER = "BLINDED_READER"
    ANALYST = "FINAL_ANALYST"


class Selection(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    DETECTOR = "DETECTOR_INFORMED"
    DISAGREEMENT = "AB_DISAGREEMENT"
    FINAL_PROBABILITY = "LOCKED_MAP_PROBABILITY"


DEV_TAINTS = frozenset({"DEVELOPMENT", "DETECTOR_DISCOVERY", "DEVELOPMENT_LABEL"})


@dataclass(frozen=True)
class Evidence:
    artifact_id: str
    role: Role
    origin_role: Role
    selection: Selection = Selection.INDEPENDENT
    taints: FrozenSet[str] = frozenset()
    independent_measurement: bool = False
    acquisition_utc: str | None = None
    reused_development_response: bool = False
    # This is an artifact lineage assertion, not the geographical exposure ledger.
    parents: tuple[str, ...] = ()

    @property
    def effective_taints(self) -> FrozenSet[str]:
        inherited = set(self.taints)
        if self.role in {Role.ENGINEERING, Role.DEV_REFERENCE}:
            inherited.add("DEVELOPMENT")
        if self.selection in {Selection.DETECTOR, Selection.DISAGREEMENT}:
            inherited.update({"DEVELOPMENT", "DETECTOR_DISCOVERY"})
        if self.role == Role.DEV_REFERENCE:
            inherited.add("DEVELOPMENT_LABEL")
        return frozenset(inherited)


@dataclass(frozen=True)
class EvaluationGate:
    candidate_id: str
    candidate_digest: str
    response_protocol_digest: str
    lock_record_id: str
    release_record_id: str | None = None
    release_candidate_digest: str | None = None
    response_lock_record_id: str | None = None
    analysis_release_record_id: str | None = None
    retired_for_current_candidate: bool = False
    prediction_authorization_record_id: str | None = None
    prediction_candidate_digest: str | None = None

    def validate_lock(self) -> None:
        if self.retired_for_current_candidate:
            raise Denied("Opened/retired test cannot become a fresh test of a revised candidate.")
        values = (self.candidate_id, self.candidate_digest,
                  self.response_protocol_digest, self.lock_record_id)
        if not all(isinstance(x, str) and x.strip() for x in values):
            raise Denied("A recorded candidate/protocol evaluation lock is required.")

    def validate_prediction_authorization(self) -> None:
        self.validate_lock()
        if not self.prediction_authorization_record_id:
            raise Denied("Locked-map processing/stratification needs its separate authorization.")
        if self.prediction_candidate_digest != self.candidate_digest:
            raise Denied("Prediction-processing authorization does not match the candidate lock.")

    def validate_release(self, *, analysis: bool = False) -> None:
        self.validate_lock()
        if not self.release_record_id:
            raise Denied("Final reference requires an explicit reference release.")
        if self.release_candidate_digest != self.candidate_digest:
            raise Denied("Release does not match the locked candidate.")
        if analysis and not (self.response_lock_record_id and self.analysis_release_record_id):
            raise Denied("Reference/prediction joining requires response lock and analysis release.")


def validate_evidence(e: Evidence) -> None:
    if not e.artifact_id or not isinstance(e.role, Role) or not isinstance(e.origin_role, Role):
        raise Denied("An explicit, recognized artifact identity and role are required.")
    if not isinstance(e.selection, Selection):
        raise Denied("Unknown discovery mechanism.")
    if e.role in {Role.DEV_REFERENCE, Role.FINAL_REFERENCE}:
        if e.origin_role in {Role.AUXILIARY, Role.METADATA, Role.ENGINEERING,
                             Role.FINAL_PREDICTION}:
            raise Denied("Auxiliary/engineering/prediction evidence cannot masquerade as reference truth.")
        if not e.independent_measurement or not e.acquisition_utc:
            raise Denied("Reference needs independent measurement and actual acquisition metadata.")
    if e.role == Role.FINAL_REFERENCE:
        if e.effective_taints & DEV_TAINTS or e.reused_development_response:
            raise Denied("Development evidence/responses cannot be promoted to final reference.")
        if e.origin_role == Role.DEV_REFERENCE:
            raise Denied("Original development references remain development-only.")
        if e.selection != Selection.FINAL_PROBABILITY:
            raise Denied("Final reference must belong to the separately authorized probability audit.")
    if e.selection in {Selection.DETECTOR, Selection.DISAGREEMENT}:
        if e.role not in {Role.ENGINEERING, Role.DEV_REFERENCE}:
            raise Denied("Detector-informed discovery is development-only.")


def derive(parent: Evidence, *, artifact_id: str, role: Role) -> Evidence:
    """Preserve evidence lineage/taint when deriving a downstream artifact."""
    validate_evidence(parent)
    child = replace(parent, artifact_id=artifact_id, role=role,
                    taints=parent.effective_taints,
                    parents=parent.parents + (parent.artifact_id,))
    validate_evidence(child)
    return child


def check_access(e: Evidence, actor: Actor, gate: EvaluationGate | None = None,
                 *, blinded_packet: bool = False) -> str:
    """Return policy eligibility ONLY. Never authorizes acquisition, cost or pixel IO."""
    validate_evidence(e)
    if not isinstance(actor, Actor):
        raise Denied("Unknown workflow actor.")
    if actor == Actor.READER:
        if not blinded_packet or e.role not in {Role.DEV_REFERENCE, Role.FINAL_REFERENCE}:
            raise Denied("Reader access is limited to validated blinded reference packets.")
    if e.role == Role.FINAL_REFERENCE:
        if actor == Actor.DEVELOPER:
            raise Denied("Developer cannot access final reference while retaining an untouched test.")
        if gate is None:
            raise Denied("Final reference remains sealed.")
        gate.validate_release(analysis=actor == Actor.ANALYST)
    if e.role == Role.FINAL_PREDICTION:
        if actor == Actor.READER or gate is None:
            raise Denied("Locked predictions are not reader material and require a candidate lock.")
        if actor == Actor.DEVELOPER:
            raise Denied("Sampled-location final predictions are custodian/analysis material.")
        gate.validate_prediction_authorization()
        if actor == Actor.ANALYST:
            gate.validate_release(analysis=True)
    if actor == Actor.ANALYST and e.role in {Role.ENGINEERING, Role.DEV_REFERENCE}:
        raise Denied("Development material is not a final-reference result.")
    return "POLICY_ELIGIBLE_ONLY; NO_IO_OR_ACQUISITION_AUTHORIZATION"


_NEUTRAL_ID = re.compile(r"R[0-9]{2,6}\Z")
_IMAGE_PATH = re.compile(r"images/R[0-9]{2,6}_(?:optical|rgb|nir|qa|support10|support30|support50|view[0-9]+)\.png\Z")


def _keys(value: Any, expected: set[str], optional: set[str] = frozenset()) -> None:
    if not isinstance(value, dict) or not expected <= set(value) or set(value) - expected - optional:
        raise Denied("Packet contains an absent or unapproved field; fail closed.")


def validate_blinded_packet(packet: dict[str, Any]) -> None:
    """Strict structured-field allowlist, not content-recognition or OCR security.

    Image pixels, filenames and prose still need independently recorded package QA.
    No first-reader response, discovery route, stratum or detector field is allowed.
    """
    _keys(packet, {"neutral_id", "geometry", "support_m", "target_acquisition_utc",
                   "optical_observations", "protocol_version"})
    if not _NEUTRAL_ID.fullmatch(str(packet["neutral_id"])):
        raise Denied("Packet requires a neutral record alias.")
    if packet["support_m"] not in {10, 30, 50}:
        raise Denied("Unregistered response support.")
    geometry = packet["geometry"]
    _keys(geometry, {"type", "coordinates", "crs"})
    if geometry["type"] not in {"Point", "Polygon", "MultiPolygon"}:
        raise Denied("Unknown response geometry.")
    if not isinstance(packet["optical_observations"], list) or not packet["optical_observations"]:
        raise Denied("A packet needs optical observations.")
    for observation in packet["optical_observations"]:
        _keys(observation, {"image", "acquisition_utc", "sensor", "native_resolution_m",
                            "display_pipeline_id", "registration_context"})
        if not _IMAGE_PATH.fullmatch(str(observation["image"])):
            raise Denied("Use a neutral relative image path; do not expose acquisition folders or hidden keys.")
        _keys(observation["registration_context"], {"status", "uncertainty_m"})
        if observation["registration_context"]["status"] not in {"MEASURED", "SCENARIO", "UNKNOWN"}:
            raise Denied("Unrecognized positional-support context.")


@dataclass(frozen=True)
class ExposureEvent:
    event_id: str
    status: str
    description: str
    related_event_id: str | None = None


def append_exposure(history: tuple[ExposureEvent, ...], event: ExposureEvent) -> tuple[ExposureEvent, ...]:
    if event.status not in {"EXPOSED", "UNVIEWED_EXTENT_UNKNOWN", "ADDITIONAL_OBSERVATION"}:
        raise Denied("Exposure history cannot be cleared or silently reclassified.")
    if event.event_id in {x.event_id for x in history}:
        raise Denied("Event identities are immutable.")
    if event.related_event_id and event.related_event_id not in {x.event_id for x in history}:
        raise Denied("Related historical event is absent.")
    return history + (event,)


def verify_exposure_extension(original: tuple[ExposureEvent, ...], proposed: tuple[ExposureEvent, ...]) -> None:
    if proposed[:len(original)] != original or len(proposed) < len(original):
        raise Denied("Historical exposure events were changed or removed.")
    checked = original
    for item in proposed[len(original):]:
        checked = append_exposure(checked, item)


@dataclass(frozen=True)
class NativeWindow:
    col_min: float
    row_min: float
    col_max: float
    row_max: float


@dataclass(frozen=True)
class PixelScope:
    scope_id: str
    role: Role
    artifact_id: str
    crs: str
    authorized_geometry: Any
    prohibited_geometry: Any | None = None
    operation_authorization_record: str | None = None


def check_native_window(e: Evidence, actor: Actor, scope: PixelScope,
                        window: NativeWindow, transform: tuple[float, ...],
                        *, source_crs: str, source_width: int, source_height: int,
                        halo: int = 0, padding: int = 0,
                        gate: EvaluationGate | None = None,
                        blinded_packet: bool = False) -> dict[str, Any]:
    """Validate the ENTIRE planned native read before opening/reading pixels.

    transform uses GDAL order (x0,a,b,y0,d,e). Fractional window edges round
    outward; halo and padding expand all four edges. No clipping to safe geometry
    or source extent is performed here. Caller must pass exactly this window to
    its IO implementation after independent operation authorization. Scope must
    come from the approved manifest, never from the requested window itself.
    """
    from shapely.geometry import Polygon
    check_access(e, actor, gate, blinded_packet=blinded_packet)
    if e.role == Role.METADATA:
        raise Denied("Metadata role does not authorize pixel reads.")
    if scope.role != e.role or scope.artifact_id != e.artifact_id:
        raise Denied("Pixel scope is bound to a different artifact or role.")
    if not scope.scope_id or not scope.operation_authorization_record:
        raise Denied("Separate recorded operation authorization is required.")
    if not source_crs or source_crs != scope.crs:
        raise Denied("CRS mismatch or missing CRS; no implicit reprojection.")
    coordinates = (window.col_min, window.row_min, window.col_max, window.row_max)
    if len(transform) != 6 or not all(isfinite(x) for x in (*coordinates, *transform)):
        raise Denied("Non-finite window/transform.")
    if window.col_max <= window.col_min or window.row_max <= window.row_min:
        raise Denied("Empty/inverted source window.")
    if any(type(v) is not int or v < 0 for v in (halo, padding)):
        raise Denied("Halo and padding must be nonnegative integers.")
    if any(type(v) is not int or v <= 0 for v in (source_width, source_height)):
        raise Denied("Invalid source dimensions.")
    x0, a, b, y0, d, f = transform
    if a * f - b * d == 0:
        raise Denied("Singular source transform.")
    expansion = halo + padding
    c0, r0 = floor(window.col_min) - expansion, floor(window.row_min) - expansion
    c1, r1 = ceil(window.col_max) + expansion, ceil(window.row_max) + expansion
    if c0 < 0 or r0 < 0 or c1 > source_width or r1 > source_height:
        raise Denied("Expanded read exceeds source extent; do not silently crop the approved plan.")
    footprint = Polygon([(x0 + a*c + b*r, y0 + d*c + f*r)
                         for c, r in ((c0,r0), (c1,r0), (c1,r1), (c0,r1))])
    allowed = scope.authorized_geometry
    if allowed is None or allowed.is_empty or not allowed.is_valid:
        raise Denied("Invalid/absent role-specific authorized geometry.")
    if not allowed.covers(footprint):
        raise Denied("Rounded/halo/padded source read leaves its authorized role scope.")
    prohibited = scope.prohibited_geometry
    if prohibited is not None:
        if not prohibited.is_valid or footprint.intersects(prohibited):
            raise Denied("Source read intersects a prohibited region, including its boundary.")
    return {"status": "WINDOW_POLICY_CHECK_PASSED_NOT_AN_IO_OPERATION",
            "scope_id": scope.scope_id, "artifact_id": e.artifact_id,
            "native_window": [c0, r0, c1, r1],
            "source_crs": source_crs, "role": e.role.value,
            "footprint_wkt": footprint.wkt}
