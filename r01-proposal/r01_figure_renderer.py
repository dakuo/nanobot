#!/usr/bin/env python3
"""
r01_figure_renderer.py
Renders NIH R01 proposal figures from YAML spec files using matplotlib.

Supports:
  F1 – System Architecture (community choir → AI pipeline → feedback)
  F2 – CONSORT Study Design Flowchart
  F3 – Data Pipeline (stub)
  F4 – Timeline / Gantt (stub)

Usage:
  python r01_figure_renderer.py --spec-dir /path/to/specs --output-dir /path/to/exports
"""

from __future__ import annotations

import argparse
import os
import pathlib
import sys
from typing import Any, Dict

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np
import yaml


# ── Palette constants ────────────────────────────────────────────────────────
AMBER = "#E8A838"
BLUE = "#3A6EA5"
TEAL = "#2E8B6A"
CHARCOAL = "#1A1A2E"
MID_GRAY = "#6B6B6B"
RED_FILL = "#FDECEA"
RED_BORDER = "#C0392B"
LIGHT_BLUE_BG = "#EBF3FB"
WHITE = "#FFFFFF"

AMBER_30 = "#E8A83840"  # 30 % opacity amber  (hex alpha ≈ 4D, using ~25%)
BLUE_30 = "#3A6EA540"
TEAL_30 = "#2E8B6A40"

FONT_FAMILY = "sans-serif"


# ── Utility helpers ──────────────────────────────────────────────────────────


def _save(fig: plt.Figure, output_dir: str, figure_id: str) -> None:
    """Export to SVG and PNG (300 DPI)."""
    os.makedirs(output_dir, exist_ok=True)
    base = os.path.join(output_dir, figure_id)
    fig.savefig(f"{base}.svg", format="svg", bbox_inches="tight", pad_inches=0.15)
    fig.savefig(f"{base}.png", format="png", dpi=300, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f"  ✓ {figure_id}.svg + {figure_id}.png → {output_dir}")


def _rounded_box(
    ax: plt.Axes,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    *,
    facecolor: str = WHITE,
    edgecolor: str = BLUE,
    fontsize: float = 8,
    fontweight: str = "normal",
    text_color: str = CHARCOAL,
    linewidth: float = 1.5,
    boxstyle: str = "round,pad=0.12",
    zorder: int = 3,
    va: str = "center",
    wrap_width: int | None = None,
) -> FancyBboxPatch:
    """Draw a rounded-rectangle box with centered label and return the patch."""
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=boxstyle,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        zorder=zorder,
    )
    ax.add_patch(patch)
    txt = label
    if wrap_width and len(label) > wrap_width:
        words = label.split()
        lines, cur = [], ""
        for w_ in words:
            if cur and len(cur) + len(w_) + 1 > wrap_width:
                lines.append(cur)
                cur = w_
            else:
                cur = f"{cur} {w_}" if cur else w_
        if cur:
            lines.append(cur)
        txt = "\n".join(lines)
    ax.text(
        x + w / 2,
        y + h / 2,
        txt,
        ha="center",
        va=va,
        fontsize=fontsize,
        color=text_color,
        fontfamily=FONT_FAMILY,
        fontweight=fontweight,
        zorder=zorder + 1,
        linespacing=1.3,
    )
    return patch


def _arrow(
    ax,
    x0,
    y0,
    x1,
    y1,
    *,
    color=MID_GRAY,
    lw=1.5,
    style="->",
    connectionstyle="arc3,rad=0",
    zorder=2,
    mutation_scale=12,
):
    """Draw a FancyArrowPatch between two points."""
    arrow = FancyArrowPatch(
        (x0, y0),
        (x1, y1),
        arrowstyle=style,
        connectionstyle=connectionstyle,
        color=color,
        linewidth=lw,
        mutation_scale=mutation_scale,
        zorder=zorder,
    )
    ax.add_patch(arrow)
    return arrow


def _diamond(
    ax,
    cx,
    cy,
    w,
    h,
    label,
    *,
    facecolor=TEAL,
    text_color=WHITE,
    edgecolor=TEAL,
    fontsize=6.5,
    linewidth=1.2,
    zorder=4,
):
    """Draw a diamond (rotated square) at (cx, cy) with given half-widths."""
    verts = np.array(
        [
            [cx, cy + h],  # top
            [cx + w, cy],  # right
            [cx, cy - h],  # bottom
            [cx - w, cy],  # left
            [cx, cy + h],  # close
        ]
    )
    poly = plt.Polygon(
        verts,
        closed=True,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=linewidth,
        zorder=zorder,
    )
    ax.add_patch(poly)
    ax.text(
        cx,
        cy,
        label,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=text_color,
        fontweight="bold",
        fontfamily=FONT_FAMILY,
        zorder=zorder + 1,
    )


# ══════════════════════════════════════════════════════════════════════════════
# F1 — System Architecture
# ══════════════════════════════════════════════════════════════════════════════


def render_f1_system_architecture(spec: Dict[str, Any], output_dir: str) -> None:
    """Render the Community Choir System Architecture (F1)."""
    fig, ax = plt.subplots(figsize=(7, 5.3))
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)

    # ── Column positions ──────────────────────────────────────────────────
    col_w = 1.85
    col_gap = 0.25
    col_x = [0.15, 0.15 + col_w + col_gap, 0.15 + 2 * (col_w + col_gap)]
    col_colors = [AMBER, BLUE, TEAL]
    col_titles = ["Community Layer", "AI Layer", "Feedback Layer"]
    main_y_top = 5.05
    main_y_bot = 1.35
    col_h = main_y_top - main_y_bot

    # ── Column background strips ──────────────────────────────────────────
    for i, (cx, cc, ct) in enumerate(zip(col_x, col_colors, col_titles)):
        rect = FancyBboxPatch(
            (cx, main_y_bot),
            col_w,
            col_h,
            boxstyle="round,pad=0.08",
            facecolor=cc + "18",  # ~10 % opacity
            edgecolor=cc,
            linewidth=1.8,
            zorder=1,
        )
        ax.add_patch(rect)
        ax.text(
            cx + col_w / 2,
            main_y_top + 0.12,
            ct,
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color=cc,
            fontfamily=FONT_FAMILY,
            zorder=5,
        )

    # ── COMMUNITY LAYER (col 0) ──────────────────────────────────────────
    cx0 = col_x[0]
    cw = col_w

    # Choir circle icon – ring of small circles
    choir_cx = cx0 + cw / 2
    choir_cy = 3.85
    n_seats = 10
    for k in range(n_seats):
        angle = 2 * np.pi * k / n_seats - np.pi / 2
        sx = choir_cx + 0.35 * np.cos(angle)
        sy = choir_cy + 0.28 * np.sin(angle)
        circ = plt.Circle(
            (sx, sy), 0.08, facecolor=AMBER, edgecolor=CHARCOAL, linewidth=0.6, zorder=3
        )
        ax.add_patch(circ)
    ax.text(choir_cx, choir_cy, "●", ha="center", va="center", fontsize=6, color=AMBER, zorder=3)
    ax.text(
        choir_cx,
        choir_cy - 0.50,
        "Community\nStorytelling Circle",
        ha="center",
        va="center",
        fontsize=7.5,
        fontweight="bold",
        color=CHARCOAL,
        fontfamily=FONT_FAMILY,
        zorder=5,
        linespacing=1.2,
    )

    # Site badges
    badge_y = 2.65
    sites = ["Site A", "Site B", "Site C"]
    badge_w, badge_h = 0.48, 0.22
    total_badges_w = 3 * badge_w + 2 * 0.06
    bx_start = cx0 + (cw - total_badges_w) / 2
    for j, sname in enumerate(sites):
        bx = bx_start + j * (badge_w + 0.06)
        _rounded_box(
            ax,
            bx,
            badge_y,
            badge_w,
            badge_h,
            sname,
            facecolor=AMBER,
            edgecolor=AMBER,
            fontsize=6,
            fontweight="bold",
            text_color=WHITE,
            linewidth=0.8,
            boxstyle="round,pad=0.05",
        )

    # Microphone box
    mic_y = 2.05
    mic_w, mic_h = 1.45, 0.38
    mic_x = cx0 + (cw - mic_w) / 2
    _rounded_box(
        ax,
        mic_x,
        mic_y,
        mic_w,
        mic_h,
        "8-ch Array Microphone",
        facecolor=WHITE,
        edgecolor=AMBER,
        fontsize=7,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=1.2,
    )

    # Edge device box
    edge_y = 1.50
    _rounded_box(
        ax,
        mic_x,
        edge_y,
        mic_w,
        mic_h,
        "Edge Device (RPi 5)",
        facecolor=WHITE,
        edgecolor=AMBER,
        fontsize=7,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=1.2,
    )

    # Arrow mic → edge
    _arrow(
        ax, cx0 + cw / 2, mic_y, cx0 + cw / 2, edge_y + mic_h, color=MID_GRAY, lw=1.2, style="->"
    )

    # ── AI LAYER (col 1) ─────────────────────────────────────────────────
    cx1 = col_x[1]
    ai_boxes = [
        "Diarization Engine\n(ECAPA-TDNN + LLM)",
        "Feature Extraction\n(lexical, semantic,\nacoustic prosody)",
        "Temporal Fusion\nTransformer (TFT)",
    ]
    ai_box_w = 1.55
    ai_box_h = 0.60
    ai_x = cx1 + (cw - ai_box_w) / 2
    ai_gap = 0.28
    ai_start_y = 3.90

    for k, lbl in enumerate(ai_boxes):
        by = ai_start_y - k * (ai_box_h + ai_gap)
        _rounded_box(
            ax,
            ai_x,
            by,
            ai_box_w,
            ai_box_h,
            lbl,
            facecolor=WHITE,
            edgecolor=BLUE,
            fontsize=7,
            fontweight="bold",
            text_color=CHARCOAL,
            linewidth=1.4,
        )
        if k < len(ai_boxes) - 1:
            _arrow(ax, cx1 + cw / 2, by, cx1 + cw / 2, by - ai_gap, color=BLUE, lw=1.5, style="-|>")

    # MCI Prediction output label
    pred_y = ai_start_y - 2 * (ai_box_h + ai_gap) - 0.08
    ax.text(
        cx1 + cw / 2,
        pred_y,
        "↓ MCI Trajectory Prediction",
        ha="center",
        va="top",
        fontsize=6.5,
        color=BLUE,
        fontfamily=FONT_FAMILY,
        fontweight="bold",
        fontstyle="italic",
        zorder=6,
        bbox=dict(facecolor=WHITE, edgecolor="none", pad=1.0, alpha=0.9),
    )

    # Arrow from edge device → AI layer (horizontal)
    _arrow(
        ax,
        cx0 + cw,
        edge_y + mic_h / 2,
        cx1,
        ai_start_y - (ai_box_h + ai_gap) + ai_box_h / 2,
        color=MID_GRAY,
        lw=1.5,
        style="-|>",
        connectionstyle="arc3,rad=-0.15",
    )

    # ── FEEDBACK LAYER (col 2) ───────────────────────────────────────────
    cx2 = col_x[2]
    fb_box_w = 1.55
    fb_box_h = 0.65
    fb_x = cx2 + (cw - fb_box_w) / 2

    fb1_y = 3.60
    _rounded_box(
        ax,
        fb_x,
        fb1_y,
        fb_box_w,
        fb_box_h,
        "Individualized\nFeedback Interface",
        facecolor=WHITE,
        edgecolor=TEAL,
        fontsize=7.5,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=1.4,
    )
    # tiny sparkline decoration
    spark_x = np.linspace(fb_x + 0.15, fb_x + fb_box_w - 0.15, 12)
    spark_y = fb1_y + 0.12 + 0.08 * np.sin(np.linspace(0, 4 * np.pi, 12))
    ax.plot(spark_x, spark_y, color=TEAL, linewidth=1.0, zorder=5, alpha=0.6)

    fb2_y = 2.60
    _rounded_box(
        ax,
        fb_x,
        fb2_y,
        fb_box_w,
        fb_box_h,
        "Community\nDashboard",
        facecolor=WHITE,
        edgecolor=TEAL,
        fontsize=7.5,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=1.4,
    )
    # tiny heatmap decoration (3×3 grid)
    hm_x0, hm_y0 = fb_x + fb_box_w / 2 - 0.18, fb2_y + 0.10
    hm_colors = [
        TEAL + "90",
        TEAL + "50",
        TEAL + "30",
        TEAL + "40",
        TEAL + "80",
        TEAL + "60",
        TEAL + "20",
        TEAL + "70",
        TEAL + "50",
    ]
    idx = 0
    for r in range(3):
        for c in range(3):
            rect = plt.Rectangle(
                (hm_x0 + c * 0.12, hm_y0 + r * 0.10),
                0.11,
                0.09,
                facecolor=hm_colors[idx],
                edgecolor="none",
                zorder=5,
            )
            ax.add_patch(rect)
            idx += 1

    # Arrow AI → Feedback (horizontal)
    _arrow(
        ax,
        cx1 + cw,
        ai_start_y - (ai_box_h + ai_gap) + ai_box_h / 2,
        cx2,
        fb1_y + fb_box_h / 2,
        color=MID_GRAY,
        lw=1.5,
        style="-|>",
        connectionstyle="arc3,rad=-0.10",
    )

    # Arrow between two feedback boxes
    _arrow(
        ax, cx2 + cw / 2, fb1_y, cx2 + cw / 2, fb2_y + fb_box_h, color=MID_GRAY, lw=1.0, style="->"
    )

    # ── Bidirectional arrow: Feedback ↔ Community ────────────────────────
    _arrow(
        ax,
        cx2,
        fb2_y + fb_box_h / 2,
        cx0 + cw,
        choir_cy,
        color=TEAL,
        lw=1.8,
        style="<|-|>",
        connectionstyle="arc3,rad=0.35",
        mutation_scale=14,
    )
    # label for co-design loop (with white background to avoid arrow line overlap)
    ax.text(
        3.50,
        4.88,
        "Co-Design Loop (Aim 1)",
        ha="center",
        va="center",
        fontsize=6.5,
        fontstyle="italic",
        color=TEAL,
        fontfamily=FONT_FAMILY,
        zorder=6,
        bbox=dict(facecolor=WHITE, edgecolor="none", pad=1.5, alpha=0.9),
    )

    # ── AIM-MAPPING BAND ─────────────────────────────────────────────────
    band_y = 0.15
    band_h = 0.95
    aim_specs = [
        ("Aim 1\nHCI Co-Design", col_x[0], col_w, AMBER_30, AMBER),
        ("Aim 2\nAI Analytics Pipeline", col_x[1], col_w, BLUE_30, BLUE),
        ("Aim 3\nClinical Validation\n(n=60, 3 sites, 24 wk)", col_x[2], col_w, TEAL_30, TEAL),
    ]
    for lbl, ax_, aw, fc, ec in aim_specs:
        rect = FancyBboxPatch(
            (ax_, band_y),
            aw,
            band_h,
            boxstyle="round,pad=0.06",
            facecolor=fc,
            edgecolor=ec,
            linewidth=1.2,
            zorder=2,
        )
        ax.add_patch(rect)
        ax.text(
            ax_ + aw / 2,
            band_y + band_h / 2,
            lbl,
            ha="center",
            va="center",
            fontsize=7,
            fontweight="bold",
            color=ec,
            fontfamily=FONT_FAMILY,
            zorder=5,
            linespacing=1.2,
        )

    # bracket line on top of aim band
    ax.plot(
        [col_x[0], col_x[2] + col_w],
        [band_y + band_h + 0.05, band_y + band_h + 0.05],
        color=MID_GRAY,
        linewidth=0.8,
        zorder=2,
    )

    # Title
    ax.text(
        3.5,
        5.35,
        spec.get("title", "System Architecture"),
        ha="center",
        va="bottom",
        fontsize=9.5,
        fontweight="bold",
        color=CHARCOAL,
        fontfamily=FONT_FAMILY,
        zorder=6,
    )

    _save(fig, output_dir, spec.get("figure_id", "F1"))


# ══════════════════════════════════════════════════════════════════════════════
# F2 — CONSORT Flowchart
# ══════════════════════════════════════════════════════════════════════════════


def render_f2_consort_flowchart(spec: Dict[str, Any], output_dir: str) -> None:
    """Render CONSORT-style study design flowchart (F2)."""
    fig, ax = plt.subplots(figsize=(7, 9.8))
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 10.2)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)

    center_x = 3.5
    box_w = 2.8
    box_h = 0.55

    # ── Title ─────────────────────────────────────────────────────────────
    ax.text(
        center_x,
        10.00,
        spec.get("title", "CONSORT Study Design Flowchart"),
        ha="center",
        va="top",
        fontsize=9.5,
        fontweight="bold",
        color=CHARCOAL,
        fontfamily=FONT_FAMILY,
        zorder=6,
    )

    # ── Screening box ────────────────────────────────────────────────────
    scr_y = 9.15
    _rounded_box(
        ax,
        center_x - box_w / 2,
        scr_y,
        box_w,
        box_h,
        "Assessed for Eligibility\n(~90 screened)",
        facecolor=WHITE,
        edgecolor=BLUE,
        fontsize=8.5,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=2.0,
    )

    # ── Exclusion box (right branch) ─────────────────────────────────────
    excl_x = 5.2
    excl_w = 1.65
    excl_h = 1.45
    excl_y = 8.25
    _rounded_box(
        ax,
        excl_x,
        excl_y,
        excl_w,
        excl_h,
        "",  # we'll add text manually for multi-line
        facecolor=RED_FILL,
        edgecolor=RED_BORDER,
        fontsize=7,
        text_color=CHARCOAL,
        linewidth=1.5,
        boxstyle="round,pad=0.10",
    )
    excl_lines = [
        ("Excluded (n≈30)", True, 7.5),
        ("• Dementia (CDR ≥ 1)", False, 6.8),
        ("• Non-English primary", False, 6.8),
        ("• Hearing loss >40 dB", False, 6.8),
        ("• Active psychiatric crisis", False, 6.8),
        ("• Declines participation", False, 6.8),
    ]
    ey = excl_y + excl_h - 0.14
    for txt, bold, fs in excl_lines:
        ax.text(
            excl_x + excl_w / 2,
            ey,
            txt,
            ha="center",
            va="top",
            fontsize=fs,
            fontweight="bold" if bold else "normal",
            color=RED_BORDER if bold else CHARCOAL,
            fontfamily=FONT_FAMILY,
            zorder=5,
        )
        ey -= 0.22

    # Arrow screening → exclusion (right)
    _arrow(
        ax,
        center_x + box_w / 2,
        scr_y + box_h / 2,
        excl_x,
        excl_y + excl_h / 2 + 0.3,
        color=CHARCOAL,
        lw=1.5,
        style="-|>",
        connectionstyle="arc3,rad=-0.1",
    )

    # ── Enrollment box ───────────────────────────────────────────────────
    enr_y = 8.05
    _rounded_box(
        ax,
        center_x - box_w / 2,
        enr_y,
        box_w,
        box_h + 0.1,
        "Enrolled (n=60)\nMCI confirmed: MoCA 18–25, informant-confirmed",
        facecolor=WHITE,
        edgecolor=BLUE,
        fontsize=8,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=2.0,
    )

    # Arrow screening → enrollment
    _arrow(ax, center_x, scr_y, center_x, enr_y + box_h + 0.1, color=CHARCOAL, lw=1.5, style="-|>")

    # ── Site allocation columns ──────────────────────────────────────────
    alloc_y = 6.55
    alloc_h = 0.80
    site_w = 1.80
    site_gap = 0.25
    total_w = 3 * site_w + 2 * site_gap
    site_x0 = center_x - total_w / 2

    sites_info = [
        ("Site A — Senior Center\n(n=20)", LIGHT_BLUE_BG),
        ("Site B — Faith Community\n(n=20)", WHITE),
        ("Site C — Public Library\n(n=20)", LIGHT_BLUE_BG),
    ]

    # Arrow enrollment → allocation (split into 3)
    split_y = enr_y - 0.15
    for i in range(3):
        sx = site_x0 + i * (site_w + site_gap) + site_w / 2
        # vertical drop from center
        _arrow(ax, center_x, enr_y, center_x, split_y + 0.15, color=CHARCOAL, lw=1.2, style="-")

    # horizontal spread line
    ax.plot(
        [site_x0 + site_w / 2, site_x0 + 2 * (site_w + site_gap) + site_w / 2],
        [split_y + 0.15, split_y + 0.15],
        color=CHARCOAL,
        linewidth=1.2,
        zorder=2,
    )

    for i, (lbl, fc) in enumerate(sites_info):
        sx = site_x0 + i * (site_w + site_gap)
        scx = sx + site_w / 2
        # vertical arrow down to box
        _arrow(ax, scx, split_y + 0.15, scx, alloc_y + alloc_h, color=CHARCOAL, lw=1.2, style="-|>")
        _rounded_box(
            ax,
            sx,
            alloc_y,
            site_w,
            alloc_h,
            lbl,
            facecolor=fc,
            edgecolor=BLUE,
            fontsize=7.5,
            fontweight="bold",
            text_color=CHARCOAL,
            linewidth=1.5,
        )

    # ── Allocation label ─────────────────────────────────────────────────
    ax.text(
        center_x,
        alloc_y + alloc_h + 0.22,
        "Site Allocation",
        ha="center",
        va="center",
        fontsize=8,
        fontweight="bold",
        color=BLUE,
        fontfamily=FONT_FAMILY,
        fontstyle="italic",
        zorder=5,
    )

    # ── 24-week Timeline Bar ─────────────────────────────────────────────
    tl_y = 5.50
    tl_h = 0.35
    tl_x0 = 0.6
    tl_x1 = 6.4
    tl_w = tl_x1 - tl_x0

    # Bar background
    bar = FancyBboxPatch(
        (tl_x0, tl_y),
        tl_w,
        tl_h,
        boxstyle="round,pad=0.04",
        facecolor=BLUE + "20",
        edgecolor=BLUE,
        linewidth=1.2,
        zorder=2,
    )
    ax.add_patch(bar)
    ax.text(
        center_x,
        tl_y + tl_h + 0.12,
        "24-Week Intervention Period",
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
        color=BLUE,
        fontfamily=FONT_FAMILY,
        zorder=5,
    )

    # Week markers
    weeks = [("Wk 0", 0), ("Wk 12", 12), ("Wk 24", 24)]
    for wlbl, wk in weeks:
        frac = wk / 24
        wx = tl_x0 + frac * tl_w
        ax.plot([wx, wx], [tl_y, tl_y + tl_h], color=BLUE, linewidth=1.0, zorder=3)
        ax.text(
            wx,
            tl_y - 0.06,
            wlbl,
            ha="center",
            va="top",
            fontsize=6.5,
            color=CHARCOAL,
            fontfamily=FONT_FAMILY,
            zorder=5,
        )

    # Arrows from site boxes → timeline bar
    for i in range(3):
        scx = site_x0 + i * (site_w + site_gap) + site_w / 2
        _arrow(ax, scx, alloc_y, scx, tl_y + tl_h, color=CHARCOAL, lw=1.0, style="-|>")

    # ── Assessment diamonds ──────────────────────────────────────────────
    diamond_y = 4.20
    assess_info = [
        ("Wk 0\nBaseline", 0),
        ("Wk 12\nMid", 12),
        ("Wk 24\nFinal", 24),
    ]
    dw, dh = 0.35, 0.30
    for albl, wk in assess_info:
        frac = wk / 24
        dx = tl_x0 + frac * tl_w
        _diamond(ax, dx, diamond_y, dw, dh, albl, facecolor=TEAL, text_color=WHITE, fontsize=5.5)
        # arrow from timeline to diamond
        _arrow(ax, dx, tl_y, dx, diamond_y + dh, color=CHARCOAL, lw=1.0, style="-|>")

    # Instruments label
    instruments = (
        "Instruments at each assessment:\n"
        "MoCA · ADAS-Cog 13 · Speech sample · ZBI · PROMIS-Cognitive"
    )
    ax.text(
        center_x,
        diamond_y - dh - 0.12,
        instruments,
        ha="center",
        va="top",
        fontsize=6.5,
        color=CHARCOAL,
        fontfamily=FONT_FAMILY,
        fontstyle="italic",
        zorder=5,
        linespacing=1.4,
    )

    # ── Follow-up box ────────────────────────────────────────────────────
    fu_y = 2.40
    _rounded_box(
        ax,
        center_x - box_w / 2,
        fu_y,
        box_w,
        box_h,
        "Completed Follow-Up\n(expected attrition ≤15%)",
        facecolor=WHITE,
        edgecolor=BLUE,
        fontsize=8,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=2.0,
    )
    _arrow(
        ax, center_x, diamond_y - dh, center_x, fu_y + box_h, color=CHARCOAL, lw=1.5, style="-|>"
    )

    # ── Analysis box ─────────────────────────────────────────────────────
    an_y = 1.30
    an_h = 0.95
    _rounded_box(
        ax,
        center_x - box_w / 2,
        an_y,
        box_w,
        an_h,
        "",  # manual text
        facecolor=WHITE,
        edgecolor=BLUE,
        fontsize=8,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=2.0,
    )
    ax.text(
        center_x,
        an_y + an_h - 0.12,
        "Intent-to-Treat Analysis",
        ha="center",
        va="top",
        fontsize=8.5,
        fontweight="bold",
        color=CHARCOAL,
        fontfamily=FONT_FAMILY,
        zorder=5,
    )
    ax.text(
        center_x,
        an_y + 0.12,
        (
            "Primary: MoCA trajectory slope\n"
            "Secondary: ADAS-Cog 13, speech features,\n"
            "ZBI, PROMIS-Cognitive\n"
            "Model: mixed-effects regression"
        ),
        ha="center",
        va="bottom",
        fontsize=6.5,
        color=CHARCOAL,
        fontfamily=FONT_FAMILY,
        zorder=5,
        linespacing=1.3,
    )

    _arrow(ax, center_x, fu_y, center_x, an_y + an_h, color=CHARCOAL, lw=1.5, style="-|>")

    # ── Phase separator (dashed line) ────────────────────────────────────
    ax.axhline(
        y=alloc_y + alloc_h + 0.12,
        xmin=0.02,
        xmax=0.98,
        color=MID_GRAY,
        linewidth=0.8,
        linestyle="--",
        zorder=1,
    )
    ax.text(
        0.25,
        alloc_y + alloc_h + 0.14,
        "Screening / Enrollment",
        fontsize=6,
        color=MID_GRAY,
        va="bottom",
        fontfamily=FONT_FAMILY,
    )
    ax.text(
        6.75,
        alloc_y + alloc_h + 0.14,
        "Intervention ▸",
        fontsize=6,
        color=MID_GRAY,
        va="bottom",
        ha="right",
        fontfamily=FONT_FAMILY,
    )

    _save(fig, output_dir, spec.get("figure_id", "F2"))


# ══════════════════════════════════════════════════════════════════════════════
# F3 — Data Pipeline (LLM-Based Speech Analytics)
# ══════════════════════════════════════════════════════════════════════════════

# F3 colour constants
_F3_SLATE_BLUE = "#3A6EA5"
_F3_PURPLE = "#6A5ACD"
_F3_DEEP_TEAL = "#1A6B5A"
_F3_AMBER_OUT = "#E8A838"
_F3_QA_FILL = "#FFFDE7"
_F3_QA_BORDER = "#F57C00"
_F3_DARK_GRAY = "#424242"
_F3_DIVIDER_GRAY = "#9E9E9E"


def render_f3_data_pipeline(spec: Dict[str, Any], output_dir: str) -> None:
    """Render F3: horizontal data-pipeline diagram — raw audio → MCI prediction."""
    fig, ax = plt.subplots(figsize=(7, 5.5))
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 5.5)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)

    # ── Title ─────────────────────────────────────────────────────────────
    ax.text(
        3.5,
        5.35,
        spec.get("title", "LLM-Based Speech Analytics Pipeline"),
        ha="center",
        va="top",
        fontsize=10,
        fontweight="bold",
        color=CHARCOAL,
        fontfamily=FONT_FAMILY,
    )

    # ── INPUT NODE (waveform) ─────────────────────────────────────────────
    inp_x, inp_y, inp_w, inp_h = 0.10, 4.30, 1.15, 0.72
    _rounded_box(
        ax,
        inp_x,
        inp_y,
        inp_w,
        inp_h,
        "",
        facecolor=WHITE,
        edgecolor=_F3_DARK_GRAY,
        linewidth=2,
    )
    # mini waveform
    wv_x = np.linspace(inp_x + 0.08, inp_x + inp_w - 0.08, 60)
    wv_y = inp_y + inp_h * 0.65 + 0.07 * np.sin(wv_x * 26)
    ax.plot(wv_x, wv_y, color=_F3_SLATE_BLUE, linewidth=1.0, zorder=6)
    ax.text(
        inp_x + inp_w / 2,
        inp_y + 0.14,
        "Raw Multi-Speaker Audio\n(8-ch, 16 kHz, WAV)",
        ha="center",
        va="center",
        fontsize=6.5,
        color=CHARCOAL,
        fontweight="bold",
        fontfamily=FONT_FAMILY,
        zorder=6,
    )

    # ── DIARIZATION BLOCK (grouped by dashed border) ─────────────────────
    diar_x, diar_y, diar_w, diar_h = 0.03, 2.88, 6.94, 2.18
    diar_rect = FancyBboxPatch(
        (diar_x, diar_y),
        diar_w,
        diar_h,
        boxstyle="round,pad=0.06",
        facecolor="none",
        edgecolor=MID_GRAY,
        linewidth=0.8,
        linestyle="--",
        zorder=1,
    )
    ax.add_patch(diar_rect)
    ax.text(
        diar_x + 0.10,
        diar_y + diar_h - 0.06,
        "Diarization Block",
        fontsize=7,
        color=MID_GRAY,
        fontstyle="italic",
        va="top",
        fontfamily=FONT_FAMILY,
    )

    # ── Arrow from input to stage 1 ──────────────────────────────────────
    _arrow(
        ax,
        inp_x + inp_w,
        inp_y + inp_h / 2,
        1.48,
        inp_y + inp_h / 2,
        color=_F3_DARK_GRAY,
        lw=2,
        style="-|>",
    )

    # ── 4 Processing Stages ──────────────────────────────────────────────
    stg_w, stg_h = 1.18, 0.97
    stg_gap = 0.20
    stg_x0 = 1.50
    stg_y = 3.65

    stages = [
        {
            "title": "Stage 1:\nAcoustic\nPreprocessing",
            "bullets": "RNNoise · beamforming\nSilero VAD · 30-s windows",
            "fc": _F3_SLATE_BLUE,
            "ec": _F3_SLATE_BLUE,
            "tc": WHITE,
        },
        {
            "title": "Stage 2:\nSpeaker\nEmbedding",
            "bullets": "ECAPA-TDNN · 192-dim\ncosine clustering\nenrollment ref audio",
            "fc": _F3_SLATE_BLUE,
            "ec": _F3_SLATE_BLUE,
            "tc": WHITE,
        },
        {
            "title": "Stage 3:\nLLM Speaker\nAttribution",
            "bullets": "GPT-4o structured JSON\nprior-turn context\nconsistency prompt",
            "fc": _F3_SLATE_BLUE,
            "ec": _F3_SLATE_BLUE,
            "tc": WHITE,
        },
        {
            "title": "Stage 4:\nQA Verification",
            "bullets": "WER (Whisper v3)\nconsistency score\nhuman flag if WER>15%",
            "fc": _F3_QA_FILL,
            "ec": _F3_QA_BORDER,
            "tc": CHARCOAL,
        },
    ]

    for i, stg in enumerate(stages):
        sx = stg_x0 + i * (stg_w + stg_gap)
        lw_box = 2.5 if i == 3 else 1.5
        _rounded_box(
            ax,
            sx,
            stg_y,
            stg_w,
            stg_h,
            "",
            facecolor=stg["fc"],
            edgecolor=stg["ec"],
            linewidth=lw_box,
            boxstyle="round,pad=0.08",
        )
        # title text
        ax.text(
            sx + stg_w / 2,
            stg_y + stg_h - 0.08,
            stg["title"],
            ha="center",
            va="top",
            fontsize=7,
            fontweight="bold",
            color=stg["tc"],
            fontfamily=FONT_FAMILY,
            zorder=6,
            linespacing=1.15,
        )
        # bullet text
        bullet_color = stg["tc"] if stg["fc"] != _F3_QA_FILL else MID_GRAY
        ax.text(
            sx + stg_w / 2,
            stg_y + 0.06,
            stg["bullets"],
            ha="center",
            va="bottom",
            fontsize=5.5,
            color=bullet_color,
            fontfamily=FONT_FAMILY,
            zorder=6,
            linespacing=1.12,
        )
        # inter-stage arrows
        if i > 0:
            prev_right = stg_x0 + (i - 1) * (stg_w + stg_gap) + stg_w
            _arrow(
                ax,
                prev_right + 0.02,
                stg_y + stg_h / 2,
                sx - 0.02,
                stg_y + stg_h / 2,
                color=_F3_DARK_GRAY,
                lw=2,
                style="-|>",
            )

    # ── DIVIDER LINE ─────────────────────────────────────────────────────
    div_y = 2.72
    ax.plot(
        [0.15, 6.85], [div_y, div_y], color=_F3_DIVIDER_GRAY, linewidth=1, linestyle="--", zorder=2
    )
    ax.text(
        3.5,
        div_y + 0.06,
        "Diarization Complete  /  Feature Extraction Begins",
        ha="center",
        va="bottom",
        fontsize=7,
        color=_F3_DIVIDER_GRAY,
        fontstyle="italic",
        fontfamily=FONT_FAMILY,
    )

    # ── FEATURE EXTRACTION (4 parallel boxes) ────────────────────────────
    ft_w, ft_h = 1.48, 0.62
    ft_gap = 0.12
    total_ft = 4 * ft_w + 3 * ft_gap
    ft_x0 = (7 - total_ft) / 2
    ft_y = 1.85

    features = [
        ("Lexical Diversity", "TTR, MATTR-50,\nBrunet W"),
        ("Semantic Density", "Sentence-BERT cosine,\ntopic drift rate"),
        ("Cross-Speaker\nCoherence", "Turn-taking latency,\ntopic maintenance"),
        ("Acoustic-\nProsodic", "F0 range, speech rate,\npause ratio, jitter"),
    ]

    ft_centers = []
    for i, (ftitle, fbullets) in enumerate(features):
        fx = ft_x0 + i * (ft_w + ft_gap)
        _rounded_box(
            ax,
            fx,
            ft_y,
            ft_w,
            ft_h,
            "",
            facecolor=_F3_PURPLE,
            edgecolor=_F3_PURPLE,
            linewidth=1.5,
            boxstyle="round,pad=0.06",
        )
        ax.text(
            fx + ft_w / 2,
            ft_y + ft_h - 0.06,
            ftitle,
            ha="center",
            va="top",
            fontsize=6.5,
            color=WHITE,
            fontweight="bold",
            fontfamily=FONT_FAMILY,
            zorder=6,
        )
        ax.text(
            fx + ft_w / 2,
            ft_y + 0.05,
            fbullets,
            ha="center",
            va="bottom",
            fontsize=5.5,
            color=WHITE,
            alpha=0.88,
            fontfamily=FONT_FAMILY,
            zorder=6,
            linespacing=1.1,
        )
        ft_centers.append(fx + ft_w / 2)

    # Arrows divider → feature boxes
    for fc_x in ft_centers:
        _arrow(
            ax,
            fc_x,
            div_y - 0.02,
            fc_x,
            ft_y + ft_h + 0.02,
            color=_F3_DARK_GRAY,
            lw=1.5,
            style="-|>",
        )

    # ── AGGREGATION NODE ─────────────────────────────────────────────────
    agg_w = 3.8
    agg_x = (7 - agg_w) / 2
    agg_y = 1.32
    agg_h = 0.38
    _rounded_box(
        ax,
        agg_x,
        agg_y,
        agg_w,
        agg_h,
        "Session-Level Feature Vector (per participant, per session)",
        facecolor=WHITE,
        edgecolor=_F3_DARK_GRAY,
        fontsize=7.5,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=1.5,
        boxstyle="round,pad=0.08",
    )
    for fc_x in ft_centers:
        _arrow(ax, fc_x, ft_y, fc_x, agg_y + agg_h + 0.02, color=_F3_DARK_GRAY, lw=1.2, style="-|>")

    # ── TFT MODEL BOX ───────────────────────────────────────────────────
    tft_w, tft_h = 3.0, 0.52
    tft_x = (7 - tft_w) / 2
    tft_y = 0.60
    _rounded_box(
        ax,
        tft_x,
        tft_y,
        tft_w,
        tft_h,
        "",
        facecolor=_F3_DEEP_TEAL,
        edgecolor=_F3_DEEP_TEAL,
        linewidth=1.5,
        boxstyle="round,pad=0.08",
    )
    ax.text(
        3.5,
        tft_y + tft_h - 0.08,
        "Temporal Fusion Transformer (TFT)",
        ha="center",
        va="top",
        fontsize=8.5,
        color=WHITE,
        fontweight="bold",
        fontfamily=FONT_FAMILY,
        zorder=6,
    )
    ax.text(
        3.5,
        tft_y + 0.06,
        "24-wk longitudinal · multi-horizon · attention interpretability",
        ha="center",
        va="bottom",
        fontsize=6,
        color=WHITE,
        alpha=0.85,
        fontfamily=FONT_FAMILY,
        zorder=6,
    )
    _arrow(ax, 3.5, agg_y, 3.5, tft_y + tft_h + 0.02, color=_F3_DARK_GRAY, lw=2, style="-|>")

    # ── OUTPUT NODES (MCI Trajectory Prediction) ─────────────────────────
    out_y = 0.05
    out_h = 0.40

    # Output header label
    ax.text(
        3.5,
        out_y + out_h + 0.13,
        "MCI Trajectory Prediction",
        ha="center",
        va="center",
        fontsize=7.5,
        color=CHARCOAL,
        fontstyle="italic",
        fontfamily=FONT_FAMILY,
    )

    # Risk flag (left)
    rf_w = 1.6
    rf_x = 1.2
    _rounded_box(
        ax,
        rf_x,
        out_y,
        rf_w,
        out_h,
        "Risk Flag (binary)",
        facecolor=_F3_AMBER_OUT,
        edgecolor=_F3_AMBER_OUT,
        fontsize=7.5,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=1.5,
        boxstyle="round,pad=0.06",
    )
    # Trajectory score (right)
    ts_w = 2.5
    ts_x = 3.5
    _rounded_box(
        ax,
        ts_x,
        out_y,
        ts_w,
        out_h,
        "Continuous Trajectory\nScore + 95% CI",
        facecolor=_F3_AMBER_OUT,
        edgecolor=_F3_AMBER_OUT,
        fontsize=7.5,
        fontweight="bold",
        text_color=CHARCOAL,
        linewidth=1.5,
        boxstyle="round,pad=0.06",
    )
    # Arrows from TFT to outputs
    _arrow(
        ax,
        2.8,
        tft_y,
        rf_x + rf_w / 2,
        out_y + out_h + 0.02,
        color=_F3_DARK_GRAY,
        lw=2,
        style="-|>",
    )
    _arrow(
        ax,
        4.2,
        tft_y,
        ts_x + ts_w / 2,
        out_y + out_h + 0.02,
        color=_F3_DARK_GRAY,
        lw=2,
        style="-|>",
    )

    _save(fig, output_dir, spec.get("figure_id", "F3"))


# ══════════════════════════════════════════════════════════════════════════════
# F4 — Timeline / Gantt Chart (5-Year)
# ══════════════════════════════════════════════════════════════════════════════

# Half-year index map: Y1H1 → 0 … Y5H2 → 9
_HALF_INDEX = {
    "Y1H1": 0,
    "Y1H2": 1,
    "Y2H1": 2,
    "Y2H2": 3,
    "Y3H1": 4,
    "Y3H2": 5,
    "Y4H1": 6,
    "Y4H2": 7,
    "Y5H1": 8,
    "Y5H2": 9,
}
_HALF_LABELS = [
    "Y1\nH1",
    "Y1\nH2",
    "Y2\nH1",
    "Y2\nH2",
    "Y3\nH1",
    "Y3\nH2",
    "Y4\nH1",
    "Y4\nH2",
    "Y5\nH1",
    "Y5\nH2",
]

# Gantt palette
_G_AMBER = "#E8A838"
_G_BLUE = "#3A6EA5"
_G_TEAL = "#2E8B6A"
_G_ADMIN_GRAY = "#BDBDBD"
_G_LIGHT_GRAY = "#E0E0E0"
_G_VERY_LIGHT_GRAY = "#FAFAFA"
_G_MILESTONE_FILL = "#1A1A2E"
_G_DEP_GRAY = "#616161"


def _hex_to_rgba(hexc: str, alpha: float) -> tuple:
    """Hex colour string → (r, g, b, a) tuple."""
    r = int(hexc[1:3], 16) / 255
    g = int(hexc[3:5], 16) / 255
    b = int(hexc[5:7], 16) / 255
    return (r, g, b, alpha)


def render_f4_timeline_gantt(spec: Dict[str, Any], output_dir: str) -> None:
    """Render F4: 5-year Gantt chart with milestones and dependency arrows."""

    # ── Activity definitions ─────────────────────────────────────────────
    aim1 = [
        ("Community partner recruitment & IRB", "Y1H1", "Y1H2"),
        ("Co-design workshops (3 rounds)", "Y1H2", "Y2H2"),
        ("Interface prototype development", "Y1H2", "Y2H1"),
        ("Usability testing & refinement", "Y2H1", "Y3H1"),
        ("Dissemination of HCI findings", "Y3H1", "Y3H2"),
    ]
    aim2 = [
        ("Pipeline architecture & data infrastructure", "Y1H1", "Y1H2"),
        ("Diarization model development", "Y1H1", "Y2H1"),
        ("Feature extraction module", "Y1H2", "Y2H2"),
        ("TFT model training on pilot data", "Y2H1", "Y3H1"),
        ("Pipeline validation & optimization", "Y3H1", "Y4H1"),
        ("Open-source release", "Y4H2", "Y5H2"),
    ]
    aim3 = [
        ("Site recruitment & staff training", "Y2H1", "Y2H2"),
        ("Participant enrollment", "Y2H2", "Y3H1"),
        ("24-week intervention delivery", "Y2H2", "Y4H1"),
        ("Data collection & QA", "Y2H2", "Y4H1"),
        ("Primary analysis", "Y4H1", "Y4H2"),
        ("Secondary analyses & manuscripts", "Y4H2", "Y5H2"),
    ]
    admin = [
        ("Project management", "Y1H1", "Y5H2"),
        ("DSMB reviews", "Y2H1", "Y5H1"),
        ("Progress reports to NIH", "Y1H2", "Y5H2"),
    ]

    groups = [
        ("Aim 1: HCI Co-Design", _G_AMBER, 0.80, aim1),
        ("Aim 2: AI Analytics Pipeline", _G_BLUE, 0.80, aim2),
        ("Aim 3: Clinical Validation Trial", _G_TEAL, 0.80, aim3),
        ("Administration", _G_ADMIN_GRAY, 0.70, admin),
    ]

    # Milestones: (month, short label)
    milestones = [
        (6, "M6"),
        (12, "M12"),
        (18, "M18"),
        (24, "M24"),
        (36, "M36"),
        (48, "M48"),
        (60, "M60"),
    ]

    # ── Layout ───────────────────────────────────────────────────────────
    n_cols = 10
    row_h = 0.22  # ≥ 0.18 in per spec
    hdr_h = 0.28  # aim group header height

    total_act = sum(len(acts) for _, _, _, acts in groups)
    n_hdrs = len(groups)
    chart_h = total_act * row_h + n_hdrs * hdr_h
    top_margin = 0.95
    bot_margin = 0.55
    fig_h = chart_h + top_margin + bot_margin
    fig_w = 7.0

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)
    ax.axis("off")
    fig.patch.set_facecolor(WHITE)

    label_w = 2.25
    grid_l = label_w
    grid_r = fig_w - 0.12
    grid_w = grid_r - grid_l
    col_w = grid_w / n_cols

    chart_top = fig_h - top_margin
    chart_bot = bot_margin

    # ── Title ─────────────────────────────────────────────────────────────
    ax.text(
        fig_w / 2,
        fig_h - 0.10,
        spec.get("title", "Five-Year Project Timeline"),
        ha="center",
        va="top",
        fontsize=10,
        fontweight="bold",
        color=CHARCOAL,
        fontfamily=FONT_FAMILY,
    )

    # ── Column headers ───────────────────────────────────────────────────
    hdr_y_base = chart_top + 0.04
    for i, lbl in enumerate(_HALF_LABELS):
        cx = grid_l + (i + 0.5) * col_w
        ax.text(
            cx,
            hdr_y_base + 0.18,
            lbl,
            ha="center",
            va="center",
            fontsize=6.5,
            color=CHARCOAL,
            fontweight="bold",
            fontfamily=FONT_FAMILY,
        )
    # Year bracket labels
    for yr in range(5):
        yr_cx = grid_l + (yr * 2 + 1) * col_w
        ax.text(
            yr_cx,
            hdr_y_base + 0.42,
            f"Year {yr + 1}",
            ha="center",
            va="center",
            fontsize=7.5,
            color=CHARCOAL,
            fontweight="bold",
            fontfamily=FONT_FAMILY,
        )

    # ── Vertical column dividers ─────────────────────────────────────────
    for i in range(n_cols + 1):
        x = grid_l + i * col_w
        lw_v = 0.7 if i % 2 == 0 else 0.3
        ax.plot([x, x], [chart_bot, chart_top], color=_G_LIGHT_GRAY, linewidth=lw_v, zorder=0)

    # ── Draw rows ────────────────────────────────────────────────────────
    cur_y = chart_top  # descends

    # Track bar positions for dependency arrows
    dep_bars: Dict[str, tuple] = {}  # key → (x, cy)

    for g_label, g_color, g_alpha, activities in groups:
        # Group header
        cur_y -= hdr_h
        ax.add_patch(
            plt.Rectangle(
                (0, cur_y),
                fig_w,
                hdr_h,
                facecolor=_hex_to_rgba(g_color, 0.20),
                edgecolor="none",
                zorder=1,
            )
        )
        ax.text(
            0.08,
            cur_y + hdr_h / 2,
            g_label,
            ha="left",
            va="center",
            fontsize=7.5,
            color=g_color,
            fontweight="bold",
            fontfamily=FONT_FAMILY,
        )

        for a_idx, (act_label, start_h, end_h) in enumerate(activities):
            cur_y -= row_h

            # Alternating row bg
            if a_idx % 2 == 1:
                ax.add_patch(
                    plt.Rectangle(
                        (0, cur_y),
                        fig_w,
                        row_h,
                        facecolor=_G_VERY_LIGHT_GRAY,
                        edgecolor="none",
                        zorder=0,
                    )
                )

            # Row label
            ax.text(
                label_w - 0.06,
                cur_y + row_h / 2,
                act_label,
                ha="right",
                va="center",
                fontsize=6.5,
                color=CHARCOAL,
                fontfamily=FONT_FAMILY,
            )

            # Bar
            s = _HALF_INDEX[start_h]
            e = _HALF_INDEX[end_h]
            bar_x = grid_l + s * col_w + 0.04
            bar_w = (e - s + 1) * col_w - 0.08
            bar_y = cur_y + 0.03
            bar_bh = row_h - 0.06

            bar_patch = FancyBboxPatch(
                (bar_x, bar_y),
                bar_w,
                bar_bh,
                boxstyle="round,pad=0.02",
                facecolor=g_color,
                edgecolor="none",
                linewidth=0,
                alpha=g_alpha,
                zorder=3,
            )
            ax.add_patch(bar_patch)

            # Store positions for dependency arrows
            act_lower = act_label.lower()
            if "prototype" in act_lower and "Aim 1" in g_label:
                dep_bars["aim1_proto_right"] = (bar_x + bar_w, cur_y + row_h / 2)
            if "validation" in act_lower and "Aim 2" in g_label:
                dep_bars["aim2_pipeline_right"] = (bar_x + bar_w, cur_y + row_h / 2)
            if "intervention" in act_lower and "Aim 3" in g_label:
                dep_bars["aim3_intervention_left"] = (bar_x, cur_y + row_h / 2)
            if "Data collection" in act_label and "Aim 3" in g_label:
                dep_bars["aim3_data_left"] = (bar_x, cur_y + row_h / 2)

    # ── Dependency arrows (dashed) ───────────────────────────────────────
    if "aim1_proto_right" in dep_bars and "aim3_intervention_left" in dep_bars:
        _arrow(
            ax,
            dep_bars["aim1_proto_right"][0],
            dep_bars["aim1_proto_right"][1],
            dep_bars["aim3_intervention_left"][0],
            dep_bars["aim3_intervention_left"][1],
            color=_G_DEP_GRAY,
            lw=1,
            style="-|>",
            connectionstyle="arc3,rad=0.25",
        )
    if "aim2_pipeline_right" in dep_bars and "aim3_data_left" in dep_bars:
        _arrow(
            ax,
            dep_bars["aim2_pipeline_right"][0],
            dep_bars["aim2_pipeline_right"][1],
            dep_bars["aim3_data_left"][0],
            dep_bars["aim3_data_left"][1],
            color=_G_DEP_GRAY,
            lw=1,
            style="-|>",
            connectionstyle="arc3,rad=0.20",
        )

    # ── Milestone diamonds ───────────────────────────────────────────────
    ms_y = bot_margin - 0.06
    for month, label in milestones:
        # month → column position (6 months per column)
        col_frac = month / 6  # e.g. M6 → col 1.0
        mx = grid_l + col_frac * col_w

        dsz = 0.11
        verts = np.array(
            [
                [mx, ms_y + dsz],
                [mx + dsz * 0.7, ms_y],
                [mx, ms_y - dsz],
                [mx - dsz * 0.7, ms_y],
                [mx, ms_y + dsz],
            ]
        )
        poly = plt.Polygon(
            verts,
            closed=True,
            facecolor=_G_MILESTONE_FILL,
            edgecolor=_G_MILESTONE_FILL,
            zorder=6,
        )
        ax.add_patch(poly)
        ax.text(
            mx,
            ms_y,
            label,
            ha="center",
            va="center",
            fontsize=5,
            color=WHITE,
            fontweight="bold",
            fontfamily=FONT_FAMILY,
            zorder=7,
        )
        # thin dotted reference line
        ax.plot(
            [mx, mx],
            [ms_y + dsz, chart_top],
            color=_G_LIGHT_GRAY,
            linewidth=0.4,
            linestyle=":",
            zorder=0,
        )

    # ── Milestone legend ─────────────────────────────────────────────────
    legend_items = [
        ("M6", "IRB + MOUs"),
        ("M12", "Benchmark; Prototype v1"),
        ("M18", "Pipeline v1; Final Interface"),
        ("M24", "Enrollment; TFT Trained"),
        ("M36", "Data Collection Complete"),
        ("M48", "Primary Analysis"),
        ("M60", "Project Complete"),
    ]
    legend_str = "    ".join(f"{k}: {v}" for k, v in legend_items)
    ax.text(
        fig_w / 2,
        0.06,
        legend_str,
        ha="center",
        va="center",
        fontsize=5.5,
        color=MID_GRAY,
        fontstyle="italic",
        fontfamily=FONT_FAMILY,
    )

    _save(fig, output_dir, spec.get("figure_id", "F4"))


# ══════════════════════════════════════════════════════════════════════════════
# Dispatcher
# ══════════════════════════════════════════════════════════════════════════════

RENDERER_MAP: Dict[str, Any] = {
    "system_architecture": render_f1_system_architecture,
    "study_design_flowchart": render_f2_consort_flowchart,
    "data_pipeline": render_f3_data_pipeline,
    "timeline_gantt": render_f4_timeline_gantt,
}


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════


def main(spec_dir: str | None = None, output_dir: str | None = None) -> None:
    """Load YAML specs and render all figures."""
    parser = argparse.ArgumentParser(description="Render R01 proposal figures")
    parser.add_argument(
        "--spec-dir",
        type=str,
        default=spec_dir or ".",
        help="Directory containing F*.yaml spec files",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=output_dir or "./exports",
        help="Directory for SVG/PNG output",
    )
    args = parser.parse_args()

    spec_path = pathlib.Path(args.spec_dir)
    out_path = str(args.output_dir)

    yaml_files = sorted(spec_path.glob("F*.yaml"))
    if not yaml_files:
        print(f"No F*.yaml files found in {spec_path}")
        sys.exit(1)

    print(f"Found {len(yaml_files)} spec(s) in {spec_path}")
    for yf in yaml_files:
        with open(yf, "r") as f:
            spec = yaml.safe_load(f)
        fig_type = spec.get("figure_type", "")
        fig_id = spec.get("figure_id", yf.stem)
        renderer = RENDERER_MAP.get(fig_type)
        if renderer is None:
            print(f"  ⚠ No renderer for figure_type={fig_type!r} ({fig_id})")
            continue
        print(f"  Rendering {fig_id} ({fig_type}) …")
        renderer(spec, out_path)

    print("Done.")


if __name__ == "__main__":
    main()
