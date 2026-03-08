from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from math import ceil
from typing import Dict, List, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="EditPro Ultra API",
    description="Advanced feature discovery and rollout planning for EditPro.",
    version="2.0.0",
)


class Feature(BaseModel):
    id: str
    name: str
    category: str
    tier: str
    impact_score: int = Field(ge=1, le=100)
    description: str


class PlanRequest(BaseModel):
    goals: List[Literal["speed", "quality", "ai", "collaboration", "social"]] = Field(
        ..., description="Desired outcomes such as speed, quality, collaboration, social, or AI"
    )
    timeline_weeks: int = Field(default=8, ge=2, le=52)


class PlanItem(BaseModel):
    week: int
    milestone: str
    features: List[str]


class PlanResponse(BaseModel):
    created_at: datetime
    timeline_weeks: int
    goals: List[str]
    plan: List[PlanItem]


FEATURES: List[Feature] = [
    Feature(id="F001", name="4K Timeline", category="Video", tier="Core", impact_score=88, description="Smooth native 4K timeline editing with adaptive rendering."),
    Feature(id="F002", name="8K Proxy Workflow", category="Video", tier="Ultra", impact_score=86, description="Auto-generated smart proxies for 8K and high bitrate content."),
    Feature(id="F003", name="AI Scene Detection", category="AI", tier="Pro", impact_score=90, description="Automatically split footage into scene-aware clips."),
    Feature(id="F004", name="AI Transcript Editing", category="AI", tier="Ultra", impact_score=91, description="Edit spoken content by editing generated transcripts."),
    Feature(id="F005", name="Noise Reduction v2", category="Audio", tier="Core", impact_score=80, description="One-click adaptive denoise for voice and ambient tracks."),
    Feature(id="F006", name="Stem Separation", category="Audio", tier="Ultra", impact_score=84, description="Split vocals, drums, bass, and instruments into separate stems."),
    Feature(id="F007", name="Multicam Sync", category="Video", tier="Pro", impact_score=82, description="Waveform and timecode multicam synchronization."),
    Feature(id="F008", name="Color Match AI", category="Color", tier="Pro", impact_score=83, description="Match camera profiles and lighting using ML-based balancing."),
    Feature(id="F009", name="LUT Marketplace", category="Color", tier="Core", impact_score=70, description="Browse and apply curated cinematic LUT packs."),
    Feature(id="F010", name="Motion Graphics Presets", category="Design", tier="Core", impact_score=76, description="Drag-and-drop title and animation templates."),
    Feature(id="F011", name="Auto Captions", category="Accessibility", tier="Pro", impact_score=87, description="Generate multilingual captions with style presets."),
    Feature(id="F012", name="Live Collaboration", category="Team", tier="Ultra", impact_score=93, description="Real-time shared timeline editing for distributed teams."),
    Feature(id="F013", name="Version History", category="Team", tier="Core", impact_score=79, description="Branch, compare, and restore timeline versions."),
    Feature(id="F014", name="Cloud Review Links", category="Team", tier="Pro", impact_score=81, description="Share secure web previews with frame-accurate comments."),
    Feature(id="F015", name="Auto Reframe", category="Social", tier="Pro", impact_score=85, description="Resize compositions for vertical, square, and widescreen outputs."),
    Feature(id="F016", name="Social Export Pack", category="Social", tier="Core", impact_score=74, description="One-click exports for YouTube, TikTok, Instagram, and Shorts."),
    Feature(id="F017", name="Smart B-Roll Suggestions", category="AI", tier="Ultra", impact_score=88, description="Recommend context-aware B-roll from your media library."),
    Feature(id="F018", name="Face Blur Tracker", category="Privacy", tier="Pro", impact_score=78, description="Track and blur faces/license plates across clips."),
    Feature(id="F019", name="Object Removal", category="AI", tier="Ultra", impact_score=86, description="Remove unwanted objects with content-aware fill."),
    Feature(id="F020", name="Beat Sync", category="Audio", tier="Core", impact_score=77, description="Snap edits automatically to musical beats."),
    Feature(id="F021", name="Auto Ducking", category="Audio", tier="Core", impact_score=73, description="Lower background music around speech intelligently."),
    Feature(id="F022", name="Podcast Suite", category="Audio", tier="Pro", impact_score=75, description="Episode templates, loudness normalization, and chapter markers."),
    Feature(id="F023", name="Green Screen Keying", category="VFX", tier="Core", impact_score=72, description="Fast and clean keying with spill suppression."),
    Feature(id="F024", name="Depth-Based Blur", category="VFX", tier="Ultra", impact_score=80, description="Cinematic depth simulation using AI depth maps."),
    Feature(id="F025", name="GPU Render Queue", category="Performance", tier="Pro", impact_score=89, description="Parallel GPU rendering for batch exports."),
    Feature(id="F026", name="Background Render", category="Performance", tier="Core", impact_score=82, description="Render while editing to minimize downtime."),
    Feature(id="F027", name="Project Health Analyzer", category="Performance", tier="Pro", impact_score=78, description="Identify bottlenecks, missing assets, and heavy effects."),
    Feature(id="F028", name="Template Marketplace", category="Design", tier="Pro", impact_score=71, description="Install creator-made intro/outro packs and overlays."),
    Feature(id="F029", name="Brand Kit", category="Design", tier="Core", impact_score=69, description="Store fonts, palettes, logos, and brand-safe lower thirds."),
    Feature(id="F030", name="Voice Clone Narration", category="AI", tier="Ultra", impact_score=84, description="Generate narration in a trained voice profile."),
    Feature(id="F031", name="Shot List Generator", category="Pre-Production", tier="Pro", impact_score=67, description="Convert script ideas into practical shot lists."),
    Feature(id="F032", name="AI Thumbnail Creator", category="AI", tier="Core", impact_score=79, description="Produce attention-grabbing thumbnail variants."),
    Feature(id="F033", name="Auto Highlights", category="AI", tier="Ultra", impact_score=87, description="Detect and extract best moments for trailers."),
    Feature(id="F034", name="SRT/ASS Subtitle Import", category="Accessibility", tier="Core", impact_score=64, description="Import and map subtitles with visual styling options."),
    Feature(id="F035", name="Speech Translation", category="Accessibility", tier="Ultra", impact_score=83, description="Translate speech and captions into 30+ languages."),
    Feature(id="F036", name="Camera Metadata Hub", category="Video", tier="Pro", impact_score=68, description="Centralized metadata panel for camera and lens info."),
    Feature(id="F037", name="Asset Deduplication", category="Storage", tier="Core", impact_score=66, description="Detect duplicate files and reclaim project space."),
    Feature(id="F038", name="Cloud Auto Backup", category="Storage", tier="Pro", impact_score=81, description="Automated backups with restore checkpoints."),
    Feature(id="F039", name="Team Permission Matrix", category="Team", tier="Ultra", impact_score=76, description="Fine-grained roles for reviewers, editors, and admins."),
    Feature(id="F040", name="Plugin SDK", category="Developer", tier="Ultra", impact_score=85, description="Build custom effects, exporters, and workflow plugins."),
]

FEATURE_INDEX: Dict[str, Feature] = {feature.id: feature for feature in FEATURES}


def _feature_index() -> Dict[str, Feature]:
    return FEATURE_INDEX


@app.get("/", tags=["system"])
def root() -> dict:
    return {
        "message": "EditPro Ultra API is running",
        "version": app.version,
        "feature_count": len(FEATURES),
    }


@app.get("/health", tags=["system"])
def health() -> dict:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/features", response_model=List[Feature], tags=["features"])
def list_features(category: str | None = None, tier: str | None = None) -> List[Feature]:
    results = FEATURES
    if category:
        results = [f for f in results if f.category.lower() == category.lower()]
    if tier:
        results = [f for f in results if f.tier.lower() == tier.lower()]
    return results


@app.get("/features/summary", tags=["features"])
def feature_summary() -> dict:
    by_category = defaultdict(int)
    by_tier = defaultdict(int)
    for feature in FEATURES:
        by_category[feature.category] += 1
        by_tier[feature.tier] += 1

    return {
        "total": len(FEATURES),
        "by_category": dict(sorted(by_category.items())),
        "by_tier": dict(sorted(by_tier.items())),
    }


@app.get("/features/{feature_id}", response_model=Feature, tags=["features"])
def get_feature(feature_id: str) -> Feature:
    feature = _feature_index().get(feature_id.upper())
    if not feature:
        raise HTTPException(status_code=404, detail=f"Feature {feature_id} not found")
    return feature


@app.post("/plans/generate", response_model=PlanResponse, tags=["planning"])
def generate_plan(request: PlanRequest) -> PlanResponse:
    goal_keywords = {
        "speed": ["Performance", "Video", "Storage"],
        "quality": ["Color", "VFX", "Audio", "Video"],
        "ai": ["AI"],
        "collaboration": ["Team", "Storage"],
        "social": ["Social", "Accessibility", "Design"],
    }

    selected_categories = set()
    for goal in request.goals:
        selected_categories.update(goal_keywords.get(goal.lower(), []))

    filtered = [f for f in FEATURES if not selected_categories or f.category in selected_categories]
    filtered = sorted(filtered, key=lambda f: f.impact_score, reverse=True)

    if not filtered:
        return PlanResponse(
            created_at=datetime.now(timezone.utc),
            timeline_weeks=request.timeline_weeks,
            goals=list(request.goals),
            plan=[],
        )

    phase_count = min(4, len(filtered))
    chunk_size = max(1, ceil(len(filtered) / phase_count))
    weeks_per_phase = max(1, ceil(request.timeline_weeks / phase_count))

    items: List[PlanItem] = []
    for index in range(phase_count):
        start = index * chunk_size
        end = min(len(filtered), start + chunk_size)
        batch = filtered[start:end]
        if not batch:
            continue
        items.append(
            PlanItem(
                week=min(request.timeline_weeks, (index * weeks_per_phase) + 1),
                milestone=f"Phase {index + 1}: {batch[0].category} acceleration",
                features=[f"{feature.id} - {feature.name}" for feature in batch[:5]],
            )
        )

    return PlanResponse(
        created_at=datetime.now(timezone.utc),
        timeline_weeks=request.timeline_weeks,
        goals=list(request.goals),
        plan=items,
    )
