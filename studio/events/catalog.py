"""Studio event catalog (ADR-003 / ADR-005)."""

from __future__ import annotations

# Wildcard for EventBus.subscribe / TimelineStore.
ALL_EVENTS = "*"

# Initial catalog from ADR-003.
PROJECT_CREATED = "ProjectCreated"
PROJECT_MODIFIED = "ProjectModified"
PROJECT_SAVED = "ProjectSaved"
PROJECT_OPENED = "ProjectOpened"
CSV_IMPORTED = "CsvImported"
SOLUTION_GENERATION_STARTED = "SolutionGenerationStarted"
SOLUTION_GENERATED = "SolutionGenerated"
SOLUTION_SELECTED = "SolutionSelected"
SOLUTIONS_MARKED_OUTDATED = "SolutionsMarkedOutdated"
ALGORITHM_STARTED = "AlgorithmStarted"
ALGORITHM_FINISHED = "AlgorithmFinished"
EVALUATION_FINISHED = "EvaluationFinished"
EXPORT_COMPLETED = "ExportCompleted"
WORKSPACE_UPDATED = "WorkspaceUpdated"

CATALOG: tuple[str, ...] = (
    PROJECT_CREATED,
    PROJECT_MODIFIED,
    PROJECT_SAVED,
    PROJECT_OPENED,
    CSV_IMPORTED,
    SOLUTION_GENERATION_STARTED,
    SOLUTION_GENERATED,
    SOLUTION_SELECTED,
    SOLUTIONS_MARKED_OUTDATED,
    ALGORITHM_STARTED,
    ALGORITHM_FINISHED,
    EVALUATION_FINISHED,
    EXPORT_COMPLETED,
    WORKSPACE_UPDATED,
)
