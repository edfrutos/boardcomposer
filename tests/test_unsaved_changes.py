from studio.unsaved_changes import unsaved_changes_message


def test_unsaved_message_includes_project_name_and_file():
    text = unsaved_changes_message("Cocina", "/tmp/demo.bcproj", language="es")
    assert "Cocina" in text
    assert "/tmp/demo.bcproj" in text
    assert "guardar" in text.casefold()


def test_unsaved_message_for_never_saved_project():
    text = unsaved_changes_message("Borrador", None, language="es")
    assert "Borrador" in text
    assert "Todavía no se ha guardado" in text


def test_unsaved_message_falls_back_to_unnamed():
    text = unsaved_changes_message("  ", None, language="en")
    assert "Untitled" in text
    assert "has not been saved" in text
