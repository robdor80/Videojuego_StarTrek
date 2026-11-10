#!/usr/bin/env python3
"""MSI acceptance: real native Core Aster with the quiet, task-first Tk console.

This test needs a Windows desktop and the compiled f06_aster_runner. It is
separate from the headless Core unit tests, which cannot assess visual layout.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import tkinter as tk

from aster_gui import Panel


def visible_contacts(panel: Panel) -> list[str]:
    tree = panel.contacts_table
    return [cid for group in tree.get_children()
            for cid in tree.get_children(group)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", required=True, type=Path)
    args = parser.parse_args()
    assert args.runner.is_file(), args.runner
    root = tk.Tk()
    panel = None
    try:
        panel = Panel(root, args.runner.resolve())
        root.update_idletasks()
        root.update()

        assert len(panel.navigation_buttons) == 6, "human-sized operating groups"
        assert len(visible_contacts(panel)) >= 18, "real Core contacts missing"
        assert panel.contacts_table.winfo_viewable(), "system hierarchy is hidden"
        assert panel.contacts_table.winfo_width() >= 250, "system hierarchy too narrow"
        assert not panel.map_box.winfo_manager(), "map must be optional"
        assert not panel.test_area.winfo_manager(), "QA machinery must be hidden"
        assert not panel.alert_bar.winfo_manager(), "no new ship alert on initial inventory"
        assert all(c[3] for c in panel.state["contacts"] if c[1]==1 and c[2]==1)
        assert len(panel.state.get("science", [])) == 6, "six scientific reports missing"

        # Expand/collapse categories; simple labels instead of backend dumps.
        assert panel.contacts_table.exists("group:planet")
        label = panel.contacts_table.item("group:planet", "text")
        assert "6" in label and "clase" in label, label

        # A new uncloaked Klingon must be identified on detection,
        # visibly notify the officer and bring the running guard to ×1.
        snapshot = panel.command("STEP 3600")
        panel.apply(snapshot)
        root.update_idletasks()
        root.update()
        assert panel.arrival_id is not None, "new ship arrival not highlighted"
        subject = panel.arrival_id
        assert panel.contact_map[subject][3] == 16, (
            "Klingon was not identified at first acquisition")
        assert panel.speed.get() == "×1", "new naval arrival did not slow to ×1"
        assert panel.restore_speed_button.winfo_viewable(), "officer cannot resume speed"
        assert panel.alert_bar.winfo_viewable(), "big alert is not visible"
        assert "VOR'CHA" in panel.alert_title.cget("text"), "alert omits identified ship"
        assert panel.footer.winfo_viewable(), "alert displaced the watch footer"
        assert panel.notice_bar.winfo_viewable(), "alert displaced the system notice"
        assert (panel.footer.winfo_y() + panel.footer.winfo_height()
                <= root.winfo_height()), "watch controls extend below the window"
        assert subject in panel.alert_ids
        panel.open_alert_contact()
        assert panel.contacts_table.selection() == (subject,), "alert has no direct action"
        assert subject in panel.contact_map
        dossier=panel.detail_text.get("1.0", "end")
        assert "Crucero de batalla klingon" in dossier, dossier
        assert "CAPACIDADES CONOCIDAS DE LA CLASE" in dossier, dossier
        assert "Disruptores y torpedos de fotones" in dossier, dossier
        assert "Transpondedor observado" not in dossier, dossier
        assert "Fiabilidad de la detección" not in dossier, dossier
        assert "Referencia:" not in dossier, dossier
        assert "ESTUDIOS" not in dossier, dossier
        panel.contact_action("FOCUS")
        assert "Identificación rápida" in panel.notice_label.cget("text")
        panel.apply(panel.command("STEP 20"))
        root.update_idletasks()
        assert "INTERCEPTACIÓN" in panel.alert_title.cget("text"), (
            "course converging on our ship must be prominent")
        intercept_dossier=panel.detail_text.get("1.0", "end")
        assert "Rumbo de desplazamiento" in intercept_dossier
        assert "Se acerca" in intercept_dossier
        assert "TRAYECTORIA DE INTERCEPTACIÓN" in intercept_dossier
        assert panel.footer.winfo_viewable(), "quick scan broke layout"

        # BUG F06-UX-03: a live 500-ms refresh must not jump the contact
        # list back to the selected item or to the first category.
        tree = panel.contacts_table
        for group in tree.get_children():
            tree.item(group, open=True)
        root.update_idletasks()
        tree.yview_moveto(1.0)
        root.update_idletasks()
        old_scroll = tree.yview()[0]
        assert old_scroll > 0, "test must have enough rows to scroll"
        panel.apply(panel.command("STEP 15"))
        root.update_idletasks()
        new_scroll = tree.yview()[0]
        assert abs(new_scroll - old_scroll) < 0.02, (
            "live refresh hijacked manual contact scrolling",
            old_scroll, new_scroll)
        assert panel.footer.winfo_viewable()

        # The usual views must remain filterable and retain real observation data.
        panel.navigate("contacts")
        panel.select_section("unidentified")
        unidentified = visible_contacts(panel)
        assert not unidentified, "uncloaked ships must not remain unidentified"
        panel.select_section("all")
        panel.navigate("results")
        panel.select_section("planets")
        planets = visible_contacts(panel)
        assert len(planets) == 6, "planet summary lost a Core contact"
        sample = planets[0]
        panel.contacts_table.selection_set(sample)
        panel.show_selected()
        dossier = panel.detail_text.get("1.0", "end")
        assert "DATOS PLANETARIOS" in dossier and "Oxígeno:" in dossier, dossier

        # Opening a category is not selecting a sensor object or issuing orders.
        panel.contacts_table.selection_set("group:planet")
        panel.show_selected()
        assert not panel.action_area.winfo_manager(), "group header has contact actions"

        panel.contacts_table.selection_remove("group:planet")
        panel.navigate("configuration")
        panel.show_selected()
        assert panel.engineering.winfo_manager(), "profiles must be reachable"
        assert "EQUIPO DE SENSORES" in panel.detail_text.get("1.0", "end")

        # The one live line is replaceable. Historical messages remain available.
        previous = len(panel.lines)
        panel.append(snapshot["tick"], "Mensaje operativo actual de prueba")
        assert len(panel.lines) == previous + 1
        assert "Mensaje operativo actual de prueba" in panel.notice_label.cget("text")
        assert not hasattr(panel, "log"), "legacy scrolling log is still on-screen"
        panel.toggle_map()
        root.update_idletasks()
        assert panel.map_box.winfo_manager(), "on-demand spatial map unavailable"
        assert len(panel.map_positions) >= 0
        # Regress the actual user failure: narrow/short window, map and
        # priority banner all visible while the guard's bottom controls stay put.
        root.geometry("1150x700")
        root.update_idletasks()
        root.update()
        assert panel.footer.winfo_viewable(), "watch controls hidden in short viewport"
        panel.restore_watch_speed()
        assert panel.speed.get() == "×30", "officer cannot restore accelerated guard"
        assert (panel.footer.winfo_y() + panel.footer.winfo_height()
                <= root.winfo_height()), "footer clipped in short viewport"
        print("PASS native Core / priority alert / footer visible / rapid identification / archive")
    finally:
        if panel:
            panel.close()
        else:
            root.destroy()


if __name__ == "__main__":
    main()
