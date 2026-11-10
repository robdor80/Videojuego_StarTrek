#!/usr/bin/env python3
"""Windows Tk acceptance: the *real CoreRPG* Aster runner opens a usable console.

Do not replace the native runner with synthetic JSON in this smoke test.
This guards against the blank contact table found during the MSI evaluation.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import tkinter as tk

from aster_gui import Panel


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runner", required=True, type=Path)
    args = ap.parse_args()
    assert args.runner.is_file(), args.runner
    root = tk.Tk()
    panel = None
    try:
        panel = Panel(root, args.runner.resolve())
        root.update_idletasks()
        root.update()

        assert len(panel.navigation_buttons) == 10, "LCARS navigation contract"
        assert len(panel.contacts_table.get_children()) >= 18, "native contacts not visible"
        assert panel.contacts_table.winfo_viewable(), "contact table is hidden"
        assert panel.contacts_table.winfo_width() >= 250, "contact list has unusable width"
        assert panel.map_canvas.winfo_viewable(), "spatial map is hidden"
        assert len(panel.map_positions) >= 18, "map lacks the observed Core contacts"
        assert len(panel.state.get("science", [])) == 6, "six native science reports missing"

        # Operational warning must be large, visible and one-click actionable.
        alert_snapshot = panel.command("STEP 2400")
        panel.apply(alert_snapshot)
        assert alert_snapshot["attention"] > 0, alert_snapshot
        assert panel.alert_bar.winfo_viewable(), "operator warning banner not visible"
        assert panel.alert_ids == [str(cid) for cid in alert_snapshot["attention_contacts"]]
        flagged = panel.alert_ids[0]
        panel.open_alert_contact()
        assert panel.contacts_table.selection() == (flagged,), "alert did not open real contact"
        assert "ESTADO DEL EQUIPO" not in panel.detail_text.get("1.0", "end")

        panel.navigate("contacts")
        panel.select_section("unidentified")
        assert all(panel.contact_map[k][1] == 1 and panel.contact_map[k][3] == 0
                   for k in panel.contacts_table.get_children())
        panel.select_section("identified")
        assert all(panel.contact_map[k][3] != 0
                   for k in panel.contacts_table.get_children())

        panel.navigate("sensor_readout")
        panel.select_section("planets")
        listed = panel.contacts_table.get_children()
        assert len(listed) == 6, "planet filter did not show all observed planets"
        sample = listed[0]
        panel.contacts_table.selection_set(sample)
        panel.show_selected()
        dossier = panel.detail_text.get("1.0", "end")
        assert "Informe científico registrado en CoreRPG" in dossier, dossier

        panel.contacts_table.selection_remove(sample)
        panel.navigate("diagnostics")
        panel.show_selected()
        assert "ESTADO DEL EQUIPO" in panel.detail_text.get("1.0", "end")
        root.update_idletasks()
        print("PASS real Core Aster / ten menus / 3 panels / map / table / 6 dossiers")
    finally:
        if panel:
            panel.close()
        else:
            root.destroy()


if __name__ == "__main__":
    main()
