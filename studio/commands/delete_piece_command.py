"""Command for deleting a piece and its placement."""

from studio.commands.command import Command


class DeletePieceCommand(Command):
    name: str = "Eliminar pieza"

    def __init__(self, services, piece_id: str):
        self.services = services
        self.piece_id = piece_id
        self._piece = None
        self._placement = None
        self._piece_index: int | None = None
        self._placement_index: int | None = None

    def execute(self):
        project = self.services.projects.current_project
        if project is None:
            return

        try:
            self._piece = project.piece_by_id(self.piece_id)
        except KeyError:
            return

        self._placement = project.placement_by_piece_id(self.piece_id)

        self._piece_index = project.pieces.index(self._piece)
        project.pieces.remove(self._piece)

        if self._placement is not None:
            self._placement_index = project.placements.index(self._placement)
            project.placements.remove(self._placement)

    def undo(self):
        project = self.services.projects.current_project
        if project is None or self._piece is None:
            return

        piece_index = self._piece_index or 0
        project.pieces.insert(piece_index, self._piece)

        if self._placement is not None:
            placement_index = self._placement_index or 0
            project.placements.insert(placement_index, self._placement)

    def redo(self):
        self.execute()
