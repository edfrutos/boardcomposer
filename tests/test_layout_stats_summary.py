"""Tests for Studio solver statistics summaries."""

from collections import Counter

from boardcomposer.solver.pipeline_stats import PipelineStats
from boardcomposer.solver.validation_result import ValidationReason
from studio.services import StudioServices


def test_stats_summary_shows_general_counts():
    """The summary contains the main pipeline counters."""
    services = StudioServices()
    services.layout.stats = PipelineStats(
        generated=12,
        unique=8,
        accepted=5,
        rejected=3,
    )

    lines = services.layout.stats_summary_lines()

    assert "Candidatas generadas: 12" in lines
    assert "Candidatas únicas: 8" in lines
    assert "Aceptadas: 5" in lines
    assert "Rechazadas: 3" in lines


def test_stats_summary_shows_rejection_reasons():
    """The summary translates structured rejection reasons."""
    services = StudioServices()
    services.layout.stats = PipelineStats(
        generated=10,
        unique=6,
        accepted=2,
        rejected=4,
        rejection_reasons=Counter(
            {
                ValidationReason.OVERLAP: 3,
                ValidationReason.EXCEEDS_CONSTRAINTS: 1,
            }
        ),
    )

    lines = services.layout.stats_summary_lines()

    assert "Motivos de rechazo:" in lines
    assert "  Solapes: 3" in lines
    assert "  Fuera del tablero: 1" in lines
