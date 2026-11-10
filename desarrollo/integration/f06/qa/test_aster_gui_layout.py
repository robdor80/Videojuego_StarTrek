#!/usr/bin/env python3
"""F06 MSI human-interface contract using the actual native Aster Core runner."""
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
    parser=argparse.ArgumentParser()
    parser.add_argument("--runner", required=True, type=Path)
    args=parser.parse_args()
    assert args.runner.is_file(), args.runner
    root=tk.Tk()
    panel=None
    try:
        panel=Panel(root, args.runner.resolve())
        root.update_idletasks()
        root.update()
        assert len(panel.navigation_buttons)==4, "four operator tasks required"
        assert panel.map_box.winfo_viewable(), "main map must be visible"
        assert panel.main_text.winfo_viewable(), "central operating zone missing"
        assert panel.contacts_table.winfo_viewable(), "left operator list missing"
        assert panel.detail_text.winfo_viewable(), "right dossier missing"
        assert not panel.test_area.winfo_manager(), "QA-only options must be hidden"
        assert len(visible_contacts(panel))>=18, "GENERAL inventory missing"
        assert len(panel.state["science"])==6, "Core planetary readings missing"
        assert "PANORAMA" in panel.main_text.get("1.0","end")

        # Focused map is exactly Enterprise + ONE observed object; overview
        # exposes everything and never replaces the central workspace.
        intrepid=next(str(c[0]) for c in panel.state["contacts"]
                     if c[1]==1 and c[3]==6)
        panel.contacts_table.selection_set(intrepid)
        root.update()
        panel._draw_map()
        assert len(panel.map_positions)==1, panel.map_positions
        assert panel.map_positions[0][2]==intrepid
        initial_zoom=panel.map_zoom
        panel.zoom_map(1.33)
        assert panel.map_zoom>initial_zoom
        panel.toggle_map()
        assert len(panel.map_positions)>=18
        panel.navigate("contacts")
        assert not visible_contacts(panel), "CONTACTOS must not repeat inventory"
        panel.navigate("status")

        # A new Klingon causes automatic CONTACTOS selection and slowdown.
        panel.apply(panel.command("STEP 3600"))
        root.update()
        assert panel.current_view=="contacts", "new ship must open CONTACTOS"
        assert panel.arrival_id is not None, "naval arrival not alerted"
        subject=panel.arrival_id
        assert panel.contacts_table.selection()==(subject,), (
            "incoming ship must be selected automatically")
        klingon=panel.contact_map[subject]
        assert klingon[3]==16, "uncloaked cruiser not identified on detection"
        assert panel.speed.get()=="×1", "time must slow, not pause"
        assert panel.footer.winfo_viewable()
        assert panel.alert_bar.winfo_viewable()
        assert "VOR'CHA" in panel.alert_title.cget("text")
        assert panel.contact_report_button.winfo_manager(), (
            "communicate-to-officer action missing")
        briefing=panel.main_text.get("1.0","end")
        assert "Capitán" in briefing and "Azimut" in briefing, briefing
        assert "unidades astronómicas" in briefing
        panel.report_contact_to_officer()
        assert subject in panel.shared_report_ids
        assert panel.state["contact_briefs"][-1][0]==klingon[0]
        first_count=len(panel.state["contact_briefs"])
        panel.report_contact_to_officer()
        assert len(panel.state["contact_briefs"])==first_count, (
            "same detection reported twice")

        # Follow is a real Core order; the dedicated SEGUIMIENTO list contains
        # only selected contacts, not a copy of the system inventory.
        panel.contact_action("PRIORITY")
        assert panel.current_view=="tracking"
        assert visible_contacts(panel)==[subject],visible_contacts(panel)
        panel.apply(panel.command("STEP 20"))
        root.update()
        operative=panel.main_text.get("1.0","end")
        assert "Trayectoria:" in operative and "Se aproxima" in operative, operative
        assert "interceptación" in operative.lower(), operative
        assert panel.alert_bar.winfo_viewable()

        # The detailed Core scan runs during watch and opens ANÁLISIS.
        panel.contact_action("SCAN")
        assert panel.current_view=="results"
        assert visible_contacts(panel)==[subject]
        assert panel.scan_progress.winfo_manager()
        panel.apply(panel.command("STEP 25"))
        root.update()
        result=panel.main_text.get("1.0","end")
        assert "Análisis" in result or "ANÁLISIS" in result
        assert "Disruptores y torpedos de fotones" in result, result
        assert "no medidos" in result, "class catalogue must not fake measurements"
        assert not panel.scan_progress.winfo_manager(), (
            "completed analysis must not leave permanent progress bar")
        assert panel.tactical_report_button.winfo_manager()
        panel.send_analysis_to_tactical()
        assert subject in panel.tactical_qa_ids

        # The UI-only operator selections survive native QA checkpoints.
        panel.checkpoint("SAVE")
        panel.apply(panel.command("STEP 10"))
        panel.checkpoint("LOAD")
        assert subject in panel.followed_ids
        assert subject in panel.analyzed_ids
        assert subject in panel.shared_report_ids

        # Romulan reveal at 02:00 and actual motion in <=5 Core seconds.
        remaining=7205-panel.state["tick"]
        assert remaining>0
        panel.apply(panel.command(f"STEP {remaining}"))
        root.update()
        warbird=next(str(c[0]) for c in panel.state["contacts"]
                     if c[1]==1 and c[3]==8 and c[2]==1)
        assert panel.current_view=="contacts"
        assert panel.contacts_table.selection()==(warbird,)
        dossier=panel.detail_text.get("1.0","end").lower()
        assert "disruptores" in dossier and "camuflaje" in dossier,dossier
        assert "rumbo de desplazamiento" in dossier,dossier
        assert "consultar catálogo" not in dossier,dossier

        # Layout remains usable with a real priority banner at MSI resolution.
        root.geometry("1150x700")
        root.update()
        assert panel.footer.winfo_viewable()
        assert panel.notice_bar.winfo_viewable()
        assert panel.footer.winfo_y()+panel.footer.winfo_height()<=root.winfo_height()
        print("PASS F06 3 zones / interactive navigation / contact briefing /"
              " tracking / deep scan / tactile sharing / QA restore")
    finally:
        if panel:
            panel.close()
        else:
            root.destroy()


if __name__=="__main__":
    main()
