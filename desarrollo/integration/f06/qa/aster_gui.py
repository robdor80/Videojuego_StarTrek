#!/usr/bin/env python3
"""Aster F06 acceptance panel: intentionally small, no LCARS and no fake data.

All status and contacts come via the native f06_aster_runner (same F04 Core
campaign). The Python window ONLY sends timing/control commands and translates
authorized numeric event codes to short messages. No hidden scientific truth.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
import json
import hashlib
from pathlib import Path
import subprocess
import sys
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from math import ceil, cos, radians, sin

from aster_spatial import project

MODES = (
    "1. Guardia normal",
    "2. Repetición idéntica",
    "3. Interferencias",
    "4. Avería y recuperación",
    "5. ASTER_X1 · 9 min reales",
)
TYPES = {
    0: "señal desconocida", 1: "nave", 2: "lanzadera",
    3: "sonda", 4: "forma de vida", 5: "estructura artificial",
    6: "energía", 7: "señal warp", 8: "señal subespacial",
    9: "transmisión", 10: "partículas", 11: "anomalía",
    12: "estrella", 13: "planeta", 14: "luna", 15: "nebulosa",
    16: "estación", 17: "asteroide",
}



STARSHIP_CLASSES = {
    1: "Galaxy", 2: "Sovereign", 3: "Odyssey", 4: "Defiant",
    5: "Miranda", 6: "Intrepid", 7: "Akira", 8: "D'deridex",
    9: "Bird-of-Prey", 10: "Cubo Borg", 11: "Danube",
    12: "Olympic", 13: "Lanzadera tipo 6", 14: "D'Kyr",
    15: "D5", 16: "Vor'cha", 17: "K't'inga",
    18: "Transporte civil de clase Aster",
}
PLANET_CLASSES = {0: "sin determinar", 1: "M", 2: "H", 3: "J",
                  4: "L", 5: "P", 6: "Y"}
# Describe la procedencia del DISEÑO, no la identidad del operador.
STARSHIP_DESIGNS = {
    1: ("Crucero de exploración", "Flota Estelar"),
    2: ("Crucero de exploración", "Flota Estelar"),
    3: ("Crucero de exploración", "Flota Estelar"),
    4: ("Escolta táctica", "Flota Estelar"),
    5: ("Crucero ligero", "Flota Estelar"),
    6: ("Nave de exploración científica", "Flota Estelar"),
    7: ("Crucero de escolta", "Flota Estelar"),
    8: ("Ave de guerra", "Imperio Romulano"),
    9: ("Ave de presa", "Diseño asociado al Imperio Klingon"),
    10: ("Nave colectiva", "Colectivo Borg"),
    11: ("Nave auxiliar", "Flota Estelar"),
    12: ("Nave médica", "Flota Estelar"),
    13: ("Lanzadera", "Flota Estelar"),
    14: ("Nave vulcana", "Vulcano"),
    15: ("Crucero", "Imperio Klingon"),
    16: ("Crucero de batalla", "Imperio Klingon"),
    17: ("Crucero de batalla", "Imperio Klingon"),
    18: ("Transporte de mercancías", "Diseño civil del escenario Aster"),
}
EQUIPMENT_SLOTS = ("Emisores ofensivos", "Lanzadores", "Generadores de escudo",
                   "Capas de blindaje", "Motores warp", "Motores de impulso")
COMPARISONS = ("GRIS", "VERDE", "ÁMBAR", "ROJO")
LOSS_CAUSES = {
    1: "salida a curvatura observada", 2: "ocultación observada",
    3: "fuera del alcance de los sensores", 4: "sensores sin servicio",
}


def contact_identification(contact: list) -> str:
    category, ship_class, transponder = contact[1], contact[3], contact[6]
    if category == 1 and ship_class:
        name = STARSHIP_CLASSES.get(ship_class, f"clase #{ship_class}")
        suffix = f"; transpondedor {transponder}" if transponder else "; sin transpondedor confirmado"
        return name + suffix
    if category == 1:
        return ("Nave de clase sin confirmar; transpondedor " + str(transponder)
                if transponder else "Nave sin clase ni transpondedor confirmados")
    if category == 2:
        return "Lanzadera (tipo sin confirmar)"
    return TYPES.get(category, "señal desconocida")


def clock(tick: int) -> str:
    return f"{tick // 3600:02d}:{tick % 3600 // 60:02d}:{tick % 60:02d}"


class Panel:
    def __init__(self, root: tk.Tk, runner: Path, x1: bool = False, telemetry: Path | None = None) -> None:
        self.x1 = x1
        self.telemetry = telemetry
        self.telemetry_seen: set[tuple] = set()
        self.last_wall = time.monotonic()
        self.wall_origin = self.last_wall
        self.elapsed_fraction = 0.0
        self.last_receipt = self.last_wall
        self.equipment_seen: set[int] = set()
        self.root = root
        root.title("USS Enterprise-D · Sensores · Sistema Aster")
        root.geometry("1100x840")
        root.minsize(820, 650)
        self.process = subprocess.Popen(
            [str(runner)] + (["--x1"] if x1 else []), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, encoding="utf-8", bufsize=1,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        self.speed = tk.StringVar(value="×1" if x1 else "×30")
        self.mode = tk.StringVar(value=MODES[4 if x1 else 0])
        self.playing = x1
        self.speed_before_alert = "×30"
        self.slowed_for_alert = False
        self.sim_half_seconds = 0
        self.nav_events_seen: set[tuple[int, int, int]] = set()
        self.nav_priority: list[int] | None = None
        self.lines: list[str] = []
        self.record: list[dict] = []
        self.state: dict = {}
        self.contact_map: dict[str, list] = {}
        self.designations: dict[int, str] = {}
        self.saved_lines: list[str] | None = None
        self.saved_notes = ""
        self.manual_jobs: dict[int, int] = {}
        self.saved_manual_jobs: dict[int, int] = {}
        self.operator_scan_ids: set[int] = set()
        self.saved_operator_scan_ids: set[int] = set()
        # F06 3-zone operator UX state. None of these collections changes
        # Core's authoritative contacts, sensor truth, clock or duty rules.
        self.new_contact_ids: set[str] = set()
        self.followed_ids: set[str] = set()
        self.analyzed_ids: set[str] = set()
        self.shared_report_ids: set[str] = set()
        self.tactical_qa_ids: set[str] = set()
        self.saved_operator_views: dict[str, set[str]] = {}
        self.map_zoom = 1.0
        self.map_overview = False
        self.technical_expanded = False
        self.motion_samples: dict[str, tuple] = {}
        self.sensor_preset = tk.StringVar(value="Estándar")
        self.interrupted = None
        self.interrupted_stack = []
        self.seen_incidents = set()
        self.incident_started = {}
        self.active_alert = None
        self.last_detail_key = None
        self.saved_ui = None
        self._render()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.apply(self._read(), reset=True)
        if x1:
            self.button_play.configure(text="Pausar")
            self.progress.configure(maximum=540)
        self.last_wall = time.monotonic()
        self.wall_origin = self.last_wall
        self.tick_after = self.root.after(500, self.tick)

    def _render(self) -> None:
        """F06: quiet, task-first console with no decorative LCARS skin.

        Overview is an expandable human-readable system inventory.
        A single current notice replaces the previous notice; history is optional.
        Native Core alerts pre-empt everything else, with direct contact access.
        """
        self.root.geometry("1460x825")
        self.root.minsize(1130, 660)
        # The operating rows stay visible even when a priority alert appears.
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.current_view = "status"
        self.workspace_labels = {
            "status": "GENERAL",
            "contacts": "CONTACTOS",
            "tracking": "SEGUIMIENTO",
            "results": "ANÁLISIS",
        }
        self.section_id = "summary"
        self.contact_subset = "all"
        self.group_open: dict[str, bool] = {}
        self.map_positions: list[tuple[float, float, str]] = []
        self.map_visible = True
        self.alert_ids: list[str] = []
        self.alert_cursor = 0
        self.arrival_id: str | None = None
        self.acknowledged_arrivals: set[str] = set()
        self.navigation_buttons: dict[str, ttk.Button] = {}
        self.section_buttons: list[ttk.Button] = []
        self.contact_filter = tk.StringVar(value="Todos")
        self.search_text = tk.StringVar()
        self.search_text.trace_add("write", lambda *_: self._refresh_contacts(self.state) if self.state else None)

        header = ttk.Frame(self.root, padding=(14, 11, 14, 7))
        header.grid(row=0, column=0, sticky="ew")
        ttk.Label(header, text="USS ENTERPRISE-D  /  SENSORES",
                  font=("Segoe UI", 17, "bold")).pack(side="left")
        self.summary = ttk.Label(header, text="Vigilancia automática")
        self.summary.pack(side="right", padx=4)

        # A priority alert fills the entire console width, never a header footnote.
        self.alert_bar = tk.Frame(self.root, background="#ffe2a1",
                                  highlightbackground="#b45309",
                                  highlightthickness=3)
        alert_copy = tk.Frame(self.alert_bar, background="#ffe2a1")
        alert_copy.pack(side="left", fill="both", expand=True, padx=13, pady=8)
        self.alert_title = tk.Label(alert_copy, text="", anchor="w",
                                    font=("Segoe UI", 12, "bold"),
                                    background="#ffe2a1", foreground="#7c2d12")
        self.alert_title.pack(fill="x")
        self.alert_description = tk.Label(
            alert_copy, text="", anchor="w", justify="left",
            wraplength=960, font=("Segoe UI", 10),
            background="#ffe2a1", foreground="#451a03")
        self.alert_description.pack(fill="x", pady=(3, 0))
        self.alert_button = tk.Button(
            self.alert_bar, text="VER CONTACTO", command=self.open_alert_contact,
            font=("Segoe UI", 10, "bold"), background="#92400e",
            foreground="white", activebackground="#78350f",
            activeforeground="white", padx=12, pady=8, relief="flat")
        self.alert_button.pack(side="right", padx=12, pady=9)

        panes = ttk.Panedwindow(self.root, orient="horizontal")
        panes.grid(row=2, column=0, sticky="nsew", padx=12, pady=(3, 5))
        self.workspace_panes = panes
        self.zone_frames = []
        for width, color, weight in ((270, "#b94343", 20), (510, "#3b70bd", 38),
                                     (570, "#32834d", 42)):
            frame = tk.Frame(panes, width=width, highlightthickness=3,
                             highlightbackground=color, highlightcolor=color, bd=0)
            frame.pack_propagate(False)
            panes.add(frame, weight=weight)
            self.zone_frames.append(frame)
        left, center, right = [ttk.Frame(frame, padding=8) for frame in self.zone_frames]
        for frame in (left, center, right):
            frame.pack(fill="both", expand=True)
        self.workspace_panes.bind("<Configure>", self._fit_zones)


        # Four operator workflows; engineering adjustments are a separate utility.
        ttk.Label(left, text="OPERACIONES", font=("Segoe UI", 12, "bold")
                  ).pack(anchor="w", pady=(0, 13))
        for view, name in self.workspace_labels.items():
            btn = ttk.Button(left, text=name, command=lambda key=view: self.navigate(key))
            btn.pack(fill="x", pady=4)
            self.navigation_buttons[view] = btn
        ttk.Separator(left).pack(fill="x", pady=(10, 6))
        self.secondary_frame = ttk.Frame(left)
        self.secondary_frame.pack(fill="x")
        tools_row = ttk.Frame(left)
        tools_row.pack(fill="x", pady=(8, 6))
        ttk.Button(tools_row, text="EQUIPO", command=lambda: self.navigate("configuration")
                   ).pack(side="left", expand=True, fill="x", padx=(0, 3))
        ttk.Button(tools_row, text="HISTORIAL", command=self.open_history
                   ).pack(side="left", expand=True, fill="x", padx=(3, 0))
        ttk.Label(left, text="OBJETOS", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", pady=(4, 4))

        # CENTRAL WORKSPACE: the largest column follows the active operation.
        # Maps and sensor activity live here, not in the small navigation rail.
        titlebar = ttk.Frame(center)
        titlebar.pack(fill="x", pady=(2, 9))
        self.workspace_title = ttk.Label(titlebar, text="SISTEMA ASTER",
                                          font=("Segoe UI", 16, "bold"))
        self.workspace_title.pack(fill="x")
        titlebar = ttk.Frame(center)
        titlebar.pack(fill="x", pady=(0, 5))
        self.map_button = ttk.Button(titlebar, text="Ver todos",
                                      command=self.toggle_map)
        self.map_button.pack(side="right", padx=(4, 0))
        self.auto_brief = ttk.Label(center, text="", wraplength=350,
                                    font=("Segoe UI", 10), justify="left")
        # Compatibility widget retained off screen; context follows selection.
        self.auto_brief.bind("<Configure>", lambda event:
                             self.auto_brief.configure(wraplength=max(180,event.width-8)))
        self.section_info = ttk.Label(center, text="", font=("Segoe UI", 10))
        self.section_info.pack(fill="x", pady=(0, 9))

        self.map_box = ttk.Frame(center)
        self.map_box.pack(fill="both", expand=True, pady=(0, 7))
        self.map_canvas = tk.Canvas(self.map_box, height=250, background="#f8fafc",
                                    highlightthickness=0)
        self.map_canvas.pack(fill="both", expand=True)
        self.map_canvas.bind("<Configure>", lambda _: self._draw_map())
        self.map_canvas.bind("<Button-1>", self._select_map_contact)
        asset_dir = Path(__file__).resolve().parent / "assets"
        self.ship_sources = {
            "top": tk.PhotoImage(file=str(asset_dir / "zenital_ncc1701d.png")),
            "side": tk.PhotoImage(file=str(asset_dir / "perfil_ncc1701d.png")),
        }
        self.ship_images: dict[tuple[str, int], tk.PhotoImage] = {}

        main_box = ttk.Frame(center)
        main_box.pack(fill="both", expand=True)
        self.main_text = tk.Text(
            main_box, width=1, height=7, background="#ffffff", relief="flat",
            font=("Segoe UI", 11), padx=15, pady=12, wrap="word",
            state="disabled", spacing2=3, spacing3=3)
        self.main_text.tag_configure("heading", font=("Segoe UI", 15, "bold"))
        self.main_text.tag_configure("priority", foreground="#9a3412",
                                     font=("Segoe UI", 11, "bold"))
        self.main_text.pack(side="left", fill="both", expand=True)
        main_scroll = ttk.Scrollbar(main_box, orient="vertical",
                                    command=self.main_text.yview)
        main_scroll.pack(side="right", fill="y")
        self.main_text.configure(yscrollcommand=main_scroll.set)

        # Contact list belongs in OPERACIONES, never in the central workspace.
        list_area = ttk.Frame(left)
        list_area.pack(fill="both", expand=True)
        self.contacts_table = ttk.Treeview(
            list_area, show="tree", height=7, selectmode="browse")
        self.contacts_table.heading("#0", text="Sistema estelar observado")
        self.contacts_table.column("#0", minwidth=250, width=300, stretch=True)
        self.contacts_table.tag_configure("group", font=("Segoe UI", 12, "bold"))
        self.contacts_table.tag_configure("contact", font=("Segoe UI", 11))
        self.contacts_table.tag_configure("lost", foreground="#7d8289")
        self.contacts_table.tag_configure("alert", foreground="#9a3412")
        tree_horizontal = ttk.Scrollbar(list_area, orient="horizontal", command=self.contacts_table.xview)
        tree_horizontal.pack(side="bottom", fill="x")
        self.contacts_table.configure(xscrollcommand=tree_horizontal.set)
        self.contacts_table.pack(side="left", fill="both", expand=True)
        tree_scroll = ttk.Scrollbar(list_area, orient="vertical",
                                     command=self.contacts_table.yview)
        tree_scroll.pack(side="right", fill="y")
        self.contacts_table.configure(yscrollcommand=tree_scroll.set)
        self.contacts_table.bind("<<TreeviewSelect>>", self._on_contact_selected)
        self.contacts_table.bind("<<TreeviewOpen>>", self._remember_group)
        self.contacts_table.bind("<<TreeviewClose>>", self._remember_group)

        # RIGHT: nothing but the selected item, and its available actions.
        ttk.Label(right, text="LECTURAS DE SENSORES",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(2, 10))
        self.equipment_brief = ttk.LabelFrame(right, text="FICHA OPERATIVA · CORE F06", padding=5)
        self.equipment_brief.pack(fill="x", pady=(0, 5))
        self.equipment_brief_lines = []
        for _ in range(4):
            label = ttk.Label(self.equipment_brief, text="", wraplength=330,
                              font=("Segoe UI", 10))
            label.pack(fill="x")
            label.bind("<Configure>", lambda event:
                       event.widget.configure(wraplength=max(150,event.width-5)))
            self.equipment_brief_lines.append(label)
        detail_box = ttk.Frame(right)
        self.detail_box = detail_box
        detail_box.pack(fill="both", expand=True)
        self.detail_text = tk.Text(
            detail_box, width=1, height=3, state="disabled", relief="flat",
            background="#ffffff", font=("Segoe UI", 12),
            wrap="word", padx=14, pady=14, spacing2=3, spacing3=4)
        self.detail_text.tag_configure("heading", font=("Segoe UI", 16, "bold"))
        self.detail_text.tag_configure(
            "section", font=("Segoe UI", 11, "bold"), foreground="#155e75")
        self.detail_text.pack(side="left", fill="both", expand=True)
        details_scroll = ttk.Scrollbar(detail_box, orient="vertical",
                                        command=self.detail_text.yview)
        details_scroll.pack(side="right", fill="y")
        self.detail_text.configure(yscrollcommand=details_scroll.set)

        self.action_area = ttk.LabelFrame(right, text="LECTURAS OPCIONALES", padding=5)
        self.action_area.columnconfigure((0, 1, 2), weight=1)
        self.identify_button = ttk.Button(
            self.action_area, text="LECTURA",
            command=lambda: self.contact_action("FOCUS"))
        self.identify_button.grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(self.action_area, text="ANÁLISIS",
                   command=lambda: self.contact_action("SCAN")).grid(
                       row=0, column=1, sticky="ew", padx=2)
        self.follow_button = ttk.Button(self.action_area, text="SEGUIR",
                   command=lambda: self.contact_action("PRIORITY"))
        self.follow_button.grid(row=0, column=2, sticky="ew", padx=2)
        self.contact_report_button = ttk.Button(
            right, text="Enviar informe…",
            command=self.open_report_dialog)
        self.voice_button = ttk.Button(right, text="Comunicar por voz · guion QA",
                                       command=self.communicate_voice)
        self.resume_button = ttk.Button(left, text="Retomar estudio", command=self.resume_study)
        self.resume_button.pack(fill="x", before=self.secondary_frame, pady=4)
        self.resume_button.pack_forget()
        self.unfollow_button = ttk.Button(right, text="Dejar de seguir",
                                          command=lambda: self.contact_action("UNFOLLOW"))
        # The progress indicator is based on actual Core start/end ticks.
        self.scan_progress = ttk.Frame(right)
        self.scan_progress_label = ttk.Label(self.scan_progress, text="")
        self.scan_progress_label.pack(fill="x", pady=(0, 3))
        self.scan_progress_value = ttk.Progressbar(
            self.scan_progress, maximum=100, value=0)
        self.scan_progress_value.pack(fill="x")
        self.technical_button = ttk.Button(
            right, text="Lecturas complementarias",
            command=self.open_contact_details)
        self.tactical_report_button = ttk.Button(
            right, text="Enviar a Táctica · QA",
            command=self.send_analysis_to_tactical)
        self.science_transfer_button = ttk.Button(
            right, text="Enviar a Ciencia · QA",
            command=lambda: self.transfer_contact("SCIENCE_SEND"))

        self.engineering = ttk.LabelFrame(right, text="Ajustes de sensores", padding=9)
        ttk.Combobox(
            self.engineering, textvariable=self.sensor_preset,
            values=("Estándar", "Alta resolución", "Antinterferencias", "Máxima detección"),
            state="readonly").pack(fill="x", pady=4)
        ttk.Button(self.engineering, text="Aplicar perfil",
                   command=self.apply_preset).pack(side="left")
        ttk.Button(self.engineering, text="Autodiagnóstico",
                   command=self.diagnostic).pack(side="left", padx=8)

        # One live message, never an endless log at the centre of the console.
        notice_bar = ttk.Frame(self.root, padding=(13, 5, 13, 5))
        notice_bar.grid(row=3, column=0, sticky="ew")
        self.notice_bar = notice_bar
        ttk.Label(notice_bar, text="COMPUTADORA:", font=("Segoe UI", 10, "bold")
                  ).pack(side="left")
        self.notice_label = ttk.Label(notice_bar, text="Vigilancia automática activada.",
                                      font=("Segoe UI", 11))
        self.notice_label.pack(side="left", fill="x", expand=True, padx=(9, 0))
        self.notice_label.bind("<Configure>", lambda e: self.notice_label.configure(wraplength=max(80,e.width)))
        self.alert_title.bind("<Configure>", lambda e: self.alert_title.configure(wraplength=max(100,e.width)))
        self.alert_description.bind("<Configure>", lambda e: self.alert_description.configure(wraplength=max(100,e.width)))
        ttk.Button(notice_bar, text="Ver avisos anteriores",
                   command=self.open_history).pack(side="right")

        footer = ttk.Frame(self.root, padding=(13, 6, 13, 10))
        footer.grid(row=4, column=0, sticky="ew")
        self.footer = footer
        self.timelabel = ttk.Label(footer, text="00:00 / 08:00", width=21,
                                   font=("Segoe UI", 11, "bold"))
        self.timelabel.pack(side="left")
        self.progress = ttk.Progressbar(footer, maximum=28800, value=0, length=160)
        self.progress.pack(side="left", padx=(6, 14))
        self.button_play = ttk.Button(footer, text="Iniciar", command=self.toggle)
        self.button_play.pack(side="left")
        self.restore_speed_button = ttk.Button(
            footer, text="Volver a ×30", command=self.restore_watch_speed)
        ttk.Button(footer, text="Opciones de prueba", command=self.toggle_test_options
                   ).pack(side="right")

        # The scenario machinery stays accessible, but out of the operator's way.
        self.test_area = ttk.LabelFrame(self.root, text="Opciones de prueba F06", padding=8)
        testrow = ttk.Frame(self.test_area)
        testrow.pack(fill="x")
        ttk.Label(testrow, text="Velocidad").pack(side="left")
        self.speed_selector = ttk.Combobox(testrow, textvariable=self.speed,
                     values=("×1", "×15", "×30", "×60"), state="readonly", width=5)
        self.speed_selector.pack(side="left", padx=(4, 15))
        ttk.Label(testrow, text="Incidencia").pack(side="left")
        scenario = ttk.Combobox(testrow, textvariable=self.mode, values=MODES,
                                state="readonly", width=24)
        scenario.pack(side="left", padx=(5, 12))
        scenario.bind("<<ComboboxSelected>>", lambda _: self.restart())
        diskrow = ttk.Frame(self.test_area)
        diskrow.pack(fill="x", pady=(5, 0))
        ttk.Button(diskrow, text="Guardar ASTER_X1 en disco",
                   command=lambda: self.disk_checkpoint(False)).pack(side="left")
        ttk.Button(diskrow, text="Abrir guardia ASTER_X1",
                   command=lambda: self.disk_checkpoint(True)).pack(side="left", padx=6)
        ttk.Button(testrow, text="Reiniciar", command=self.restart).pack(side="left", padx=3)
        ttk.Button(testrow, text="Guardar", command=lambda: self.checkpoint("SAVE")
                   ).pack(side="left", padx=3)
        ttk.Button(testrow, text="Recuperar", command=lambda: self.checkpoint("LOAD")
                   ).pack(side="left", padx=3)
        ttk.Button(testrow, text="Exportar informe", command=self.export
                   ).pack(side="left", padx=3)
        ttk.Label(self.test_area, text="Notas del oficial (opcionales)"
                  ).pack(anchor="w", pady=(9, 1))
        self.notes = tk.Text(self.test_area, height=2, font=("Segoe UI", 10))
        self.notes.pack(fill="x")

        self.navigate("status")

    def _fit_zones(self, event):
        if getattr(self, "last_pane_width", None) == event.width:
            return
        self.last_pane_width = event.width
        self.workspace_panes.sashpos(0, round(event.width * .20))
        self.workspace_panes.sashpos(1, round(event.width * .58))

    @staticmethod
    def _write_text(widget, text, reset=False):
        if widget.get("1.0", "end-1c") == text:
            if reset: widget.yview_moveto(0)
            return
        pos = 0 if reset else widget.yview()[0]
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.tag_add("heading", "1.0", "1.end")
        for label, color in (("VERDE", "#19652a"), ("ÁMBAR", "#945200"),
                             ("ROJO", "#b42318"), ("GRIS", "#626262")):
            widget.tag_configure(label, foreground=color)
            start = "1.0"
            while found := widget.search(label + " ·", start, "end"):
                widget.tag_add(label, found, f"{found} lineend")
                start = f"{found}+1c"
        widget.configure(state="disabled")
        widget.yview_moveto(pos)

    def _deep_dossier(self, c):
        v = next((v for v in self.state.get("deep_analysis", []) if v["contact"] == c[0]), {})
        lines = ["HALLAZGOS ADICIONALES", ""]
        mask = v.get("mask", 0)
        if mask & 1:
            lines += ["ATMÓSFERA · MODELO DE DALTON",
                      f"Presión parcial de O₂: {v['oxygen_microbar']/1000:.3f} mbar",
                      f"Presión parcial de CO₂: {v['co2_microbar']/1000:.3f} mbar",
                      "Calculadas con presión y composición del informe científico observado.",
                      "Estas medidas no certifican habitabilidad ni ausencia de tóxicos.", ""]
        if mask & 2:
            lines += ["GEOMETRÍA OBSERVABLE",
                      f"Extensión angular estimada: {v['angular_nanoradian']} nrad",
                      "Modelo geométrico: eslora medida y distancia actual; no resuelve la orientación.", ""]
        if mask & 4:
            lines += ["HISTORIA CINEMÁTICA",
                      f"Desplazamiento neto: {v['displacement_micro_au']/1000000:.6f} UA en {v['interval_s']} s",
                      "Comparación de posiciones archivadas; no determina intenciones.", ""]
        if mask & 8:
            lines += ["EVOLUCIÓN TÉCNICA", f"Cambios de sistemas medidos: {v['equipment_changes']}", ""]
        if not mask: lines += ["No hay nuevas lecturas verificables.", ""]
        lines += ["LÍMITES DE LA MEDICIÓN",
                  "Sin medidas adicionales de tecnología interna, tripulación o vulnerabilidades."]
        return "\n".join(lines)

    def _tracking_dossier(self, c):
        nav = self._navigation_data(c) if c[2] == 1 else None
        lines = ["NAVEGACIÓN", f"Distancia: {c[5]/1000:.3f} UA"]
        if nav:
            lines += [f"Trayectoria estimada: {nav[2]:03d}°", f"Velocidad relativa: {nav[6]/1000000:.6f} UA/s",
                      {0:"Movimiento radial sin determinar.",1:"Se aproxima.",2:"Se aleja."}.get(nav[3], "Sin determinar.")]
            if nav[4]: lines.append("Posible convergencia hacia nuestra posición; intención no determinada.")
        else: lines.append("Trayectoria aún no determinada con lecturas actuales.")
        if any(e["contact"] == c[0] for e in self.state.get("equipment", [])):
            lines += ["", self._equipment_dossier(c)]
        events = [e for e in self.state.get("navigation_alerts", []) if e[1] == c[0] and self.state["tick"]-e[2] <= 30]
        if events:
            lines += ["", "CAMBIOS OBSERVADOS"]
            for e in events[-3:]:
                lines.append(f"{clock(e[2])} · " + {1:"cambio de rumbo medido",2:"convergencia de trayectoria",3:"aproximación",4:"alejamiento"}.get(e[0], "cambio de movimiento"))
        receipts = [r for r in self.state.get("deliveries", []) if r[1] == c[0] and r[4] == 2 and r[5] == 1]
        mode = next((r[1] for r in self.state.get("tracking", []) if r[0] == c[0]), 0)
        lines += ["", "ESTADO DEL SEGUIMIENTO",
                  "Transferencia continua a Táctica activa · cola QA." if mode else "Seguimiento suspendido; pulsa Seguir para retomarlo."]
        if receipts: lines.append("Última entrega confirmada: " + clock(receipts[-1][3]) + ".")
        lines.append("Potencia en vatios y preparación de curvatura: sin medidas suficientes.")
        return "\n".join(lines)

    def _view_context(self):
        selection = self.contacts_table.selection()
        return {"view": self.current_view, "selected": selection[0] if selection else None,
                "section": self.section_id, "zoom": self.map_zoom, "overview": self.map_overview,
                "detail_scroll": self.detail_text.yview()[0], "main_scroll": self.main_text.yview()[0],
                "list_scroll": self.contacts_table.yview()[0]}

    def _resume_label(self, context):
        c = self.contact_map.get(context.get("selected"))
        name = self.designations.get(c[0]) if c else None
        return "Retomar " + name if name and len(name) <= 16 else "Retomar estudio anterior"

    def _restore_view(self, context):
        self.navigate(context.get("view", "status"))
        self.select_section(context.get("section", "all"))
        if context.get("selected") in self.contact_map:
            self._choose_contact(context["selected"])
        self.map_zoom = max(.35, min(50, context.get("zoom", 1)))
        self.map_overview = context.get("overview", True)
        self.root.update_idletasks()
        self.detail_text.yview_moveto(context.get("detail_scroll", 0))
        self.main_text.yview_moveto(context.get("main_scroll", 0))
        self.contacts_table.yview_moveto(context.get("list_scroll", 0))
        self._draw_map()

    def resume_study(self):
        context = self.interrupted
        self.interrupted = self.interrupted_stack.pop() if self.interrupted_stack else None
        if context: self._restore_view(context)
        if self.interrupted:
            self.resume_button.configure(text=self._resume_label(self.interrupted))
        else: self.resume_button.pack_forget()

    def communicate_voice(self):
        selected = self.contacts_table.selection()
        if not selected or selected[0] not in self.contact_map: return
        c = self.contact_map[selected[0]]
        window = tk.Toplevel(self.root)
        window.title("Comunicar por voz · guion QA")
        window.geometry("680x310")
        ttk.Label(window, text="Guion de pruebas para que lo transmita el jugador.", padding=10).pack(fill="x")
        box = tk.Text(window, wrap="word", height=8, padx=12, pady=10)
        box.pack(fill="both", expand=True)
        box.insert("1.0", self._report_script(c))
        box.configure(state="disabled")
        ttk.Label(window, text="F06: sin canal de voz ni conversación NPC integrados.", padding=10).pack(fill="x")

    def open_report_dialog(self):
        selected = self.contacts_table.selection()
        if not selected or selected[0] not in self.contact_map: return
        contact_id = selected[0]
        window = tk.Toplevel(self.root)
        window.title("Enviar informe · cola QA")
        window.geometry("440x210")
        ttk.Label(window, text=self._operational_name(self.contact_map[contact_id]), padding=10,
                  wraplength=400).pack(fill="x")
        ttk.Label(window, text="Destinatario", padding=10).pack(anchor="w")
        recipient = tk.StringVar(value="Capitán / superior")
        ttk.Combobox(window, textvariable=recipient, state="readonly",
                     values=("Capitán / superior", "Táctica", "Ciencia")).pack(fill="x", padx=10)
        def send():
            command = {"Capitán / superior":"REPORT", "Táctica":"TACTICAL_SEND", "Ciencia":"SCIENCE_SEND"}[recipient.get()]
            self.transfer_contact(command, contact_id)
            window.destroy()
        ttk.Button(window, text="Enviar a la cola QA", command=send).pack(pady=12)

    def _ui_snapshot(self):
        return {"version": 1, "context": self._view_context(), "interrupted": self.interrupted,
                "interrupted_stack": list(self.interrupted_stack),
                "followed": sorted(self.followed_ids), "analyzed": sorted(self.analyzed_ids),
                "seen_incidents": list(self.seen_incidents),
                "incident_started": [[*k, v] for k, v in self.incident_started.items()],
                "groups": dict(self.group_open), "notes": self.notes.get("1.0", "end-1c"), "lines": list(self.lines)}

    def _restore_ui(self, state, ui):
        ids = {str(c[0]) for c in state["contacts"]}
        self.followed_ids = set(ui.get("followed", [])) & ids
        self.analyzed_ids = set(ui.get("analyzed", [])) & ids
        self.seen_incidents = {tuple(k) for k in ui.get("seen_incidents", [])}
        self.incident_started = {(cid, severity): when for cid, severity, when in ui.get("incident_started", [])}
        self.group_open = dict(ui.get("groups", {}))
        self.interrupted = ui.get("interrupted")
        self.interrupted_stack = list(ui.get("interrupted_stack", []))[-16:]
        self.lines = list(ui.get("lines", []))
        self.notes.delete("1.0", "end")
        self.notes.insert("1.0", ui.get("notes", ""))
        self.state = {}
        self.apply(state)
        self._restore_view(ui.get("context", {}))
        if self.interrupted:
            self.resume_button.configure(text=self._resume_label(self.interrupted))
            self.resume_button.pack(fill="x", before=self.secondary_frame, pady=4)
        else: self.resume_button.pack_forget()
        self.last_wall = time.monotonic()
        self.wall_origin = self.last_wall-state["tick"]
        self.elapsed_fraction = 0

    def checkpoint_file(self, path, restore):
        sidecar = path.with_suffix(path.suffix + ".ui.json")
        if restore:
            ui = {}
            if sidecar.is_file():
                ui = json.loads(sidecar.read_text(encoding="utf-8"))
                if ui.get("version") != 1 or ui.get("core_sha256") != hashlib.sha256(path.read_bytes()).hexdigest():
                    raise ValueError("El contexto no corresponde a esta guardia Core.")
            self._restore_ui(self.command(f"LOADFILE {path}"), ui)
        else:
            self.command(f"SAVEFILE {path}")
            ui = self._ui_snapshot()
            ui["core_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            temp = sidecar.with_suffix(sidecar.suffix + ".tmp")
            temp.write_text(json.dumps(ui, ensure_ascii=False), encoding="utf-8")
            temp.replace(sidecar)
        self.append(self.state["tick"], "Guardia y contexto restaurados." if restore else "Guardia y contexto guardados.")

    def toggle_test_options(self) -> None:
        if self.test_area.winfo_manager():
            self.test_area.grid_remove()
        else:
            self.test_area.grid(row=5, column=0, sticky="ew", padx=12, pady=(0, 7))

    def toggle_map(self) -> None:
        """Switch between the operator's focused contact and system overview."""
        self.map_overview = not self.map_overview
        self.map_button.configure(
            text="Enfocar contacto" if self.map_overview else "Ver todos")
        self._draw_map()

    def zoom_map(self, factor: float) -> None:
        # Kept for callers of the former XY map; angular placement has no zoom.
        self._draw_map()

    def open_history(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("Sensores · Historial de avisos")
        window.geometry("850x500")
        area = ttk.Frame(window, padding=12)
        area.pack(fill="both", expand=True)
        ttk.Label(area, text="Avisos de la guardia",
                  font=("Segoe UI", 15, "bold")).pack(anchor="w", pady=(0, 8))
        box = tk.Text(area, wrap="word", font=("Segoe UI", 11))
        box.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(area, command=box.yview)
        scroll.pack(side="right", fill="y")
        box.configure(yscrollcommand=scroll.set)
        box.insert("1.0", "\n".join(self.lines) or "No hay avisos registrados.")
        box.configure(state="disabled")
        box.see("end")

    def _remember_group(self, event: tk.Event) -> None:
        key = self.contacts_table.focus()
        if key.startswith("group:"):
            # Open/Close events fire before the Tk tree changes the -open flag.
            self.group_open[key] = not bool(self.contacts_table.item(key, "open"))

    def navigate(self, view: str) -> None:
        """Choose the officer's job, leaving automatic watch active."""
        if view not in self.workspace_labels and view != "configuration":
            return
        self.current_view = view
        if view in ("status", "configuration"):
            self.contacts_table.selection_remove(*self.contacts_table.selection())
        self.section_id = "summary"
        self.contact_subset = "all"
        self.contact_filter.set("Todos")
        for key, button in self.navigation_buttons.items():
            button.state(["disabled"] if key == view else ["!disabled"])
        for child in self.secondary_frame.winfo_children():
            child.destroy()
        filters = {
            "status": [("Todo el sistema", "all")],
            "contacts": [("Todos los contactos", "all"), ("Naves", "ships"),
                         ("Perdidos", "lost")],
            "tracking": [("En seguimiento", "all")],
            "results": [("Analizados", "all")],
            "configuration": [("Equipo de sensores", "all")],
        }
        for label, section in filters[view]:
            ttk.Button(self.secondary_frame, text=label,
                       command=lambda k=section: self.select_section(k)).pack(
                           fill="x", pady=2)
        self.workspace_title.configure(text={
            "status": "GENERAL · SISTEMA ASTER",
            "contacts": "CONTACTOS",
            "tracking": "SEGUIMIENTO PRIORITARIO",
            "results": "ANÁLISIS SOLICITADOS",
            "configuration": "EQUIPO DE SENSORES",
        }[view])
        self.map_overview = view in ("status", "configuration")
        self.map_button.configure(
            text="Enfocar contacto" if self.map_overview else "Ver todos")
        if self.state:
            self._refresh_contacts(self.state)
        self._update_view_content()
        self._update_main_content()
        self.show_selected()

    def select_section(self, section: str) -> None:
        self.section_id = section
        self.contact_subset = section if section in ("unidentified", "identified", "lost", "active") else "all"
        filters = {"all": "Todos", "planets": "Planetas", "ships": "Naves",
                   "moons": "Satélites", "artificial": "Artificiales", "stars": "Estrellas"}
        self.contact_filter.set(filters.get(section, "Todos"))
        if self.state:
            self._refresh_contacts(self.state)
        self._update_view_content()

    def _update_view_content(self) -> None:
        if not hasattr(self, "section_info"):
            return
        state = self.state
        if state:
            self.section_info.configure(text=(
                f"{state.get('active', 0)} contactos detectados"
                "   ·   vigilancia automática "
                + ("NO DISPONIBLE" if state.get("offline") else "ACTIVA")
            ))
        else:
            self.section_info.configure(text="Iniciando lectura del sistema...")
        if self.current_view == "configuration":
            if not self.engineering.winfo_manager():
                self.engineering.pack(fill="x", pady=(9, 0))
        else:
            self.engineering.pack_forget()
        if hasattr(self, "detail_text") and not self.contacts_table.selection():
            self.show_selected()
        if hasattr(self, "main_text"):
            self._update_main_content()

    def _update_alert(self, state):
        latest = {str(e["contact"]): e for e in state.get("equipment", [])}
        candidates = []
        current_causes = set()
        for cid, c in self.contact_map.items():
            if c[2] != 1: continue
            e = latest.get(cid)
            offense = bool(e and any(e["mask"] & (1 << k) and e["slots"][k][0]
                                     and e["slots"][k][1] == 3 for k in (0, 1)))
            discrepancy = bool(e and any(s[3] == 2 for s in e["slots"]))
            ordinary = 2 if (c[1] in (0, 11) or c[1] == 1 and
                            (not c[3] or discrepancy and c[3] != 18)) else 1 if discrepancy else 0
            if ordinary:
                current_causes.add((cid, ordinary))
                self.incident_started.setdefault((cid, ordinary), state["tick"])
            severity = 4 if c[1] == 1 and c[3] == 10 else 3 if offense else ordinary
            if not severity: continue
            # Cause identity deliberately excludes later generic position updates.
            key = (cid, severity)
            current_causes.add(key)
            self.incident_started.setdefault(key, state["tick"])
            age = state["tick"] - self.incident_started[key]
            if severity <= 2 and age > 45: continue
            reason = ("Contacto Borg identificado" if severity == 4 else
                      "Emisión ofensiva activa medida" if offense else
                      "Diferencias de equipamiento respecto al catálogo QA" if discrepancy else
                      "Firma sin identificación suficiente")
            candidates.append((severity, cid, key, reason))
        # A resolved cause can generate a genuinely new episode later. Keeping
        # its old acknowledgement would suppress the next offensive incident.
        self.seen_incidents.intersection_update(current_causes)
        self.incident_started = {k: v for k, v in self.incident_started.items() if k in current_causes}
        if state.get("offline") or not candidates:
            self.active_alert = None
            self.alert_ids = []
            self.alert_bar.grid_remove()
            return
        severity, cid, key, reason = max(candidates, key=lambda x: (x[0], self.incident_started[x[2]]))
        self.active_alert = key
        self.alert_ids = [c[1] for c in sorted(candidates, reverse=True)]
        self.alert_cursor = self.alert_ids.index(cid)
        c = self.contact_map[cid]
        self.alert_title.configure(text=("ALERTA · " if severity >= 3 else "ATENCIÓN · ") + self._operational_name(c))
        self.alert_description.configure(text=reason + ".")
        bg, ink, stroke = (("#fecaca", "#7f1d1d", "#b91c1c") if severity >= 3
                           else ("#ffe2a1", "#78350f", "#b45309"))
        for widget in (self.alert_bar, self.alert_title, self.alert_description): widget.configure(background=bg)
        self.alert_bar.configure(highlightbackground=stroke)
        self.alert_title.configure(foreground=ink)
        self.alert_description.configure(foreground=ink)
        self.alert_button.configure(text="Ver contacto", background=stroke)
        self.alert_bar.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        if key not in self.seen_incidents:
            self.seen_incidents.add(key)
            selection = self.contacts_table.selection()
            if severity >= 2 and (not selection or selection[0] != cid):
                if self.interrupted is not None:
                    self.interrupted_stack = (self.interrupted_stack + [self.interrupted])[-16:]
                self.interrupted = self._view_context()
                self.navigate("contacts")
                self._choose_contact(cid)
                self.resume_button.configure(text=self._resume_label(self.interrupted))
                self.resume_button.pack(fill="x", before=self.secondary_frame, pady=4)
            self.append(state["tick"], reason + ": " + self._operational_name(c) + ".")

    def open_alert_contact(self):
        if self.active_alert:
            self.navigate("contacts")
            self._choose_contact(self.active_alert[0])

    def _read(self) -> dict:
        assert self.process.stdout is not None
        line = self.process.stdout.readline()
        self.last_receipt = time.monotonic()
        if not line:
            raise RuntimeError("El proceso nativo de CoreRPG ha terminado inesperadamente.")
        result = json.loads(line)
        if not result.get("ok"):
            raise RuntimeError(result.get("error", "Error desconocido del motor."))
        return result

    def command(self, text: str) -> dict:
        if "\n" in text or "\r" in text:
            raise ValueError("Formato de orden no válido")
        if self.process.poll() is not None:
            raise RuntimeError("La simulación nativa ya no está activa.")
        assert self.process.stdin is not None
        self.process.stdin.write(text + "\n")
        self.process.stdin.flush()
        return self._read()

    def append(self, tick: int, message: str) -> None:
        """One current message. Older messages remain in on-demand history."""
        line = f"{clock(tick)} · {message}"
        self.lines.append(line)
        self.notice_label.configure(text=message[:180])

    def _contact_description(self, contact: list) -> str:
        kind = TYPES.get(contact[1], "señal desconocida")
        known = contact_identification(contact)
        distance = f"{contact[5] / 1000:.3f} UA"
        confidence = f"{contact[4] / 10:.1f}%"
        status = "activo" if contact[2] == 1 else "perdido"
        name = self.designations.get(contact[0], "Contacto C-" + str(contact[0])[-6:])
        return f"{name} · {kind}: {known}. Distancia a la nave {distance}. Confianza {confidence}. Estado {status}."

    def _on_contact_selected(self, event=None):
        selected = self.contacts_table.selection()
        if selected and selected[0] in self.contact_map:
            self.map_overview = False
            self.map_zoom = 1.0
            self.map_button.configure(text="Mapa general")
        self.show_selected()
        self._draw_map()
        self._update_main_content()

    def _draw_map(self) -> None:
        """Two angular views of the same public F06 observations."""
        if not hasattr(self, "map_canvas"):
            return
        cv = self.map_canvas
        cv.delete("all")
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 180 or h < 130:
            return
        self.map_positions = []
        gap, margin, footer = 8, 5, 32
        card_w = (w - gap - 2 * margin) / 2
        centers = (margin + card_w / 2, margin + card_w + gap + card_w / 2)
        cy = (h - footer) / 2 + 8
        radius = min(card_w * .34, (h - footer) * .31)
        elev_span = min((h - footer) * .34, radius * 1.18)
        for i, label in enumerate(("CENITAL · PROA ↑", "PERFIL · PROA →")):
            x0 = margin + i * (card_w + gap)
            cv.create_rectangle(x0, 2, x0 + card_w, h - footer,
                                outline="#b9cbd7", fill="#edf3f6")
            cv.create_text(x0 + 10, 12, text=label, anchor="w",
                           fill="#294a60", font=("Segoe UI", 9, "bold"))
        cx, sx = centers
        for scale in (.5, 1.0):
            cv.create_oval(cx-radius*scale, cy-radius*scale,
                           cx+radius*scale, cy+radius*scale,
                           outline="#9cb2bf", dash=(3, 3))
        cv.create_line(cx-radius-7, cy, cx+radius+7, cy, fill="#a9beca")
        cv.create_line(cx, cy-radius-7, cx, cy+radius+7, fill="#a9beca")
        for angle, label in ((0,"000°"),(90,"090°"),(180,"180°"),(270,"270°")):
            a = radians(angle)
            cv.create_text(cx + (radius+18)*sin(a), cy - (radius+18)*cos(a),
                           text=label, fill="#344f60", font=("Segoe UI", 8))
        for elevation in (-90, -45, 0, 45, 90):
            yy = cy - elev_span * elevation / 90
            cv.create_line(sx-radius-7, yy, sx+radius+7, yy,
                           fill="#7b99ab" if elevation == 0 else "#b7c9d2",
                           dash=() if elevation == 0 else (3, 3))
            cv.create_text(sx-radius-9, yy, text=f"{elevation:+d}°" if elevation else "0°",
                           anchor="e", fill="#526b7a", font=("Segoe UI", 8))
        cv.create_line(sx, cy-elev_span-5, sx, cy+elev_span+5,
                       fill="#b7c9d2", dash=(3, 3))
        self._ship_image(cv, "top", cx, cy, card_w * .42, radius * 1.12)
        self._ship_image(cv, "side", sx, cy, card_w * .58, elev_span * .78)
        cv.create_text(w/2, h-17,
                       text="Angular · fuera de escala · proa = +Y (QA)",
                       fill="#526b7a", font=("Segoe UI", 8))
        if not self.state:
            return
        selection = self.contacts_table.selection()
        chosen_id = selection[0] if selection and selection[0] in self.contact_map else None
        rows = ([self.contact_map[chosen_id]] if chosen_id and not self.map_overview else
                [c for c in self.state["contacts"] if c[2] == 1])
        if chosen_id and self.map_overview and chosen_id not in {str(c[0]) for c in rows}:
            rows.append(self.contact_map[chosen_id])
        for c in rows:
            key = str(c[0])
            p = project(c[8], c[9], c[10], radius, cx, cy, elev_span)
            if p is None:
                continue
            top, profile, bearing, elevation = p
            profile = (profile[0] + sx - cx, profile[1])
            selected, lost = key == chosen_id, c[2] != 1
            color = ("#8b949b" if lost else "#b45309" if key in self.followed_ids
                     else "#155e75")
            for view, point in (("top", top), ("side", profile)):
                px, py = point
                size = 6 if selected else 4
                tags = (f"contact:{key}", f"view:{view}")
                if lost:
                    cv.create_line(px-size,py-size,px+size,py+size,fill=color,width=2,tags=tags)
                    cv.create_line(px-size,py+size,px+size,py-size,fill=color,width=2,tags=tags)
                else:
                    cv.create_oval(px-size,py-size,px+size,py+size,
                                   fill=color,outline="#ffffff",width=1,tags=tags)
                if selected:
                    cv.create_oval(px-10,py-10,px+10,py+10,
                                   outline="#2563eb",width=2,tags=tags)
                self.map_positions.append((px, py, key))
            if selected:
                cv.create_line(cx, cy, *top, fill="#5c8299", dash=(3, 3))
                cv.create_line(sx, cy, *profile, fill="#5c8299", dash=(3, 3))
                name = self._tree_contact_label(c, {}).split(" · SEÑAL PERDIDA")[0]
                cv.create_text(cx, 29, text=f"{name} · {bearing:03.0f}°",
                               fill=color, font=("Segoe UI", 9, "bold"))
                cv.create_text(sx, 29, text=f"{name} · {elevation:+.0f}°" +
                               (" · PERDIDO" if lost else ""),
                               fill=color, font=("Segoe UI", 9, "bold"))
                if not lost:
                    nav = self._navigation_data(c)
                    if nav and 0 <= nav[2] < 360:
                        a = radians(nav[2])
                        self._motion_arrow(cv, top, (top[0]+15*sin(a), top[1]-15*cos(a)))
                    evidence = [r for r in self.state.get("position_evidence", [])
                                if str(r[1]) == key]
                    if len(evidence) >= 2 and tuple(evidence[-1][3:6]) == tuple(c[8:11]):
                        dz = evidence[-1][5] - evidence[-2][5]
                        if dz:
                            self._motion_arrow(cv, profile,
                                               (profile[0], profile[1]-(15 if dz > 0 else -15)))

    def _ship_image(self, canvas, view, x, y, max_w, max_h):
        source = self.ship_sources[view]
        step = max(1, ceil(source.width()/max_w), ceil(source.height()/max_h))
        key = (view, step)
        if key not in self.ship_images:
            self.ship_images[key] = source.subsample(step)
        canvas.create_image(x, y, image=self.ship_images[key], tags=(f"ship:{view}",))

    @staticmethod
    def _motion_arrow(canvas, start, end):
        canvas.create_line(*start, *end, fill="#7c3aed", width=2,
                           arrow="last", tags="trajectory")

    def _select_map_contact(self, event: tk.Event) -> None:
        if not self.map_positions:
            return
        distances = [( (x - event.x) ** 2 + (y - event.y) ** 2, key)
                     for x, y, key in self.map_positions]
        d2, key = min(distances)
        if d2 > 15 ** 2:
            return
        if self.contacts_table.exists(key):
            self.contacts_table.selection_set(key)
            self.contacts_table.see(key)
            self.show_selected()
            self._draw_map()

    def _refresh_contacts(self, state: dict) -> None:
        """Group ACTUAL observed contacts into a compact expandable inventory."""
        if not state:
            return
        tree = self.contacts_table
        selected = tree.selection()
        selected_id = selected[0] if selected else None
        for group in tree.get_children():
            if group.startswith("group:"):
                self.group_open[group] = bool(tree.item(group, "open"))
        self.contact_map = {str(c[0]): c for c in state["contacts"]}
        self.designations.update({int(cid): name for cid, name in state.get("chart_labels", [])})
        reports = {r[0]: r for r in state.get("science", [])}

        names = {
            "star": "Estrellas", "planet": "Planetas", "moon": "Lunas",
            "asteroid": "Asteroides", "nebula": "Nebulosas",
            "station": "Estaciones", "ship": "Naves", "shuttle": "Lanzaderas",
            "probe": "Sondas", "other": "Otras señales",
        }
        kind_groups = {12: "star", 13: "planet", 14: "moon", 17: "asteroid",
                       15: "nebula", 16: "station", 1: "ship", 2: "shuttle",
                       3: "probe"}
        ordered = ("star", "planet", "moon", "asteroid", "nebula", "station",
                   "ship", "shuttle", "probe", "other")
        grouped: dict[str, list[list]] = {k: [] for k in ordered}
        filter_kind = {
            "Planetas": {13}, "Naves": {1, 2}, "Estrellas": {12},
            "Satélites": {14}, "Artificiales": {1, 2, 3, 5, 16},
        }.get(self.contact_filter.get())
        needle = self.search_text.get().strip().casefold()
        for c in state["contacts"]:
            cid = str(c[0])
            if self.current_view == "tracking" and cid not in self.followed_ids:
                continue
            if self.current_view == "results" and cid not in self.analyzed_ids:
                continue
            if filter_kind is not None and c[1] not in filter_kind:
                continue
            if self.contact_subset == "unidentified" and not (
                    c[1] == 1 and c[3] == 0):
                continue
            if self.contact_subset == "identified" and not (
                    c[1] == 1 and c[3] != 0):
                continue
            if self.contact_subset == "lost" and c[2] != 2:
                continue
            if self.contact_subset == "active" and c[2] != 1:
                continue
            if needle and needle not in self._tree_contact_label(c, reports).casefold():
                continue
            grouped[kind_groups.get(c[1], "other")].append(c)
        # Incremental reconciliation: the real-time Core clock refreshes every
        # 500 ms. Rebuilding the Treeview or calling .see() on each tick jumps
        # to the selected contact and makes manual scrolling impossible.
        retained_groups: set[str] = set()
        for group_index, key in enumerate(ordered):
            rows = grouped[key]
            if not rows:
                continue
            extra = ""
            groupid = "group:" + key
            retained_groups.add(groupid)
            heading = f"{names[key].upper()}  ·  {len(rows)}{extra}"
            if not tree.exists(groupid):
                tree.insert("", "end", iid=groupid, text=heading,
                            open=self.group_open.get(groupid, True),
                            tags=("group",))
            elif tree.item(groupid, "text") != heading:
                tree.item(groupid, text=heading)

            desired_rows: set[str] = set()
            for index, c in enumerate(rows):
                cid = str(c[0])
                desired_rows.add(cid)
                label = self._tree_contact_label(c, reports)
                tags = ("alert",) if cid in self.alert_ids else (
                    ("lost",) if c[2] != 1 else ("contact",))
                if not tree.exists(cid):
                    tree.insert(groupid, index, iid=cid, text=label, tags=tags)
                else:
                    if tree.parent(cid) != groupid or tree.index(cid) != index:
                        tree.move(cid, groupid, index)
                    if tree.item(cid, "text") != label:
                        tree.item(cid, text=label)
                    if tuple(tree.item(cid, "tags")) != tags:
                        tree.item(cid, tags=tags)
            for cid in tree.get_children(groupid):
                if cid not in desired_rows:
                    tree.delete(cid)
        for groupid in tree.get_children():
            if groupid not in retained_groups:
                tree.delete(groupid)
        # Existing selection and scroll position belong to the operator.
        # Auto updates must never call .see() or change their viewport.
        self.show_selected()
        self._draw_map()
        self._update_main_content()

    def _tree_contact_label(self, contact: list, reports: dict) -> str:
        name = self.designations.get(contact[0])
        kind, status = contact[1], contact[2]
        if kind == 13:
            classification = reports.get(contact[0])
            label = name or "Planeta"
            if classification and classification[1]:
                label += " · clase " + PLANET_CLASSES.get(classification[1], "?")
                if classification[3]:
                    label += " (provisional)"
        elif kind in (1, 2):
            klass = STARSHIP_CLASSES.get(contact[3])
            label = (klass or ("Nave no identificada" if kind == 1
                               else "Lanzadera no identificada"))
            if contact[3] == 18:
                label = "Transporte civil"
            peers = [c for c in self.state.get("contacts", []) if c[1] == kind and c[3] == contact[3]]
            if len(peers) > 1:
                label += " · " + (str(contact[6]) if contact[6] else "C-" + str(contact[0])[-6:])
        elif kind == 12:
            label = name or "Estrella"
        else:
            label = name or TYPES.get(kind, "Objeto detectado").capitalize()
        if status != 1:
            label += " · SEÑAL PERDIDA"
        return label

    @staticmethod
    def _bearing(contact: list) -> tuple[int, int]:
        """Azimuth/elevation in the observer's sensor XY frame, NOT ship bow."""
        from math import atan2, degrees, hypot
        bearing = round((degrees(atan2(contact[8], contact[9])) + 360) % 360) % 360
        elevation = round(degrees(atan2(
            contact[10], hypot(contact[8], contact[9]))))
        return bearing, elevation

    def _navigation_data(self, contact: list) -> list | None:
        return next((n for n in self.state.get("navigation", [])
                     if n[0] == contact[0] and
                     0 <= self.state["tick"] - n[1] <= 300), None)

    def _operational_name(self, contact: list) -> str:
        klass = STARSHIP_CLASSES.get(contact[3]) if contact[1] in (1, 2) else None
        design = STARSHIP_DESIGNS.get(contact[3])
        if klass:
            return (f"{design[0]}, clase {klass}"
                    if design else f"Nave de clase {klass}")
        return self.designations.get(
            contact[0], TYPES.get(contact[1], "Objeto detectado").capitalize())

    def _report_script(self, contact: list) -> str:
        """A Starfleet-ready briefing based only on observed Core projections."""
        az, elevation = self._bearing(contact)
        lines = [
            f"Capitán, nuevo contacto de sensores. {self._operational_name(contact)}.",
            f"Azimut {az:03d} grados, elevación {elevation:+d} grados "
            f"en el marco de sensores. "
            f"Distancia {contact[5] / 1000:.3f} unidades astronómicas.",
        ]
        nav = self._navigation_data(contact)
        if nav:
            trend = {1: "Se aproxima.", 2: "Se aleja.",
                     0: "Movimiento radial no determinado."}.get(
                         nav[3], "Movimiento no determinado.")
            lines.append(f"Trayectoria estimada {nav[2]:03d} grados. {trend}")
            if len(nav) > 6:
                lines.append(f"Velocidad de desplazamiento relativa estimada "
                             f"{nav[6] / 1000000:.6f} UA por segundo.")
            if nav[4]:
                lines.append("Posible trayectoria de interceptación. "
                             "No se han determinado intenciones hostiles.")
        else:
            lines.append("Vector de movimiento todavía no determinado.")
        equipment = [e for e in self.state.get("equipment", []) if e["contact"] == contact[0]]
        if equipment:
            e = equipment[-1]
            if any(e["mask"] & (1 << k) and e["slots"][k][0] and e["slots"][k][1] == 3 for k in (0, 1)):
                lines.append("Emisión ofensiva activa medida en sus armas.")
            elif any(slot[3] == 2 for slot in e["slots"]):
                lines.append("Equipamiento observado diferente de la referencia de clase QA.")
        science = next((r for r in self.state.get("science", []) if r[0] == contact[0]), None)
        if science:
            lines.append(f"Temperatura medida {science[4]} kelvin y presión {science[5]} milibares. Habitabilidad sin confirmar.")
        return " ".join(lines)

    def _update_main_content(self):
        if not self.state or not hasattr(self, "main_text"):
            return
        selected = self.contacts_table.selection()
        c = self.contact_map.get(selected[0]) if selected else None
        if c:
            title = self._operational_name(c)
            if c[1] == 13:
                r = next((r for r in self.state.get("science", []) if r[0] == c[0]), None)
                if r and r[1]:
                    title += " · clase " + PLANET_CLASSES.get(r[1], "sin determinar")
                    if r[3]: title += " (provisional)"
            text = title + "\n\n" + ("Señal actual" if c[2] == 1 else "Última observación · señal perdida")
            text += "\nSímbolo de posición medido. Imagen del objeto aún no validada."
        else:
            counts = Counter(c[1] for c in self.state["contacts"] if c[2] == 1)
            text = ("SISTEMA ASTER\n\nEntorno de pruebas observado desde la Enterprise-D. "
                    f"{counts[12]} estrella · {counts[13]} planetas · {counts[14]} lunas.\n"
                    "Selecciona un cuerpo en el mapa o en la lista para explorarlo.")
        self._write_text(self.main_text, text)

    def report_contact_to_officer(self):
        self.transfer_contact("REPORT")

    def send_analysis_to_tactical(self) -> None:
        self.transfer_contact("TACTICAL_SEND")

    def transfer_contact(self, command, contact_id=None):
        selected = self.contacts_table.selection()
        cid = contact_id or (selected[0] if selected else None)
        if cid not in self.contact_map: return
        c = self.contact_map[cid]
        recipient = {"REPORT": 1, "TACTICAL_SEND": 2, "SCIENCE_SEND": 3}[command]
        try:
            response = self.command(f"{command} {c[0]}")
            receipts = [d for d in response["deliveries"] if d[1] == c[0] and d[4] == recipient and d[5] == 1]
            if not receipts: raise RuntimeError("La cola no ha confirmado la entrega.")
            self.apply(response)
            self.append(response["tick"], {1: "Informe enviado al capitán · cola QA.",
                        2: "Datos transferidos a Táctica · cola QA.",
                        3: "Datos transferidos a Ciencia · cola QA."}[recipient])
        except Exception as exc:
            messagebox.showwarning("Sensores", str(exc), parent=self.root)

    def _equipment_dossier(self, contact):
        readings = [e for e in self.state.get("equipment", []) if e["contact"] == contact[0]]
        if not readings: return "Sin medición de sistemas disponible."
        e = readings[-1]
        lines = ["SISTEMAS OBSERVADOS"]
        if e["length_m"]: lines.append(f"Eslora medida: {e['length_m']} m")
        for k, (count, condition, expected, comparison) in enumerate(e["slots"]):
            if not e["mask"] & (1 << k):
                lines.append(f"GRIS · {EQUIPMENT_SLOTS[k]}: no observable")
            else:
                status = ("ausente", "en reposo", "energizado", "emisión ofensiva activa")[condition]
                ref = f"; catálogo {expected}" if e["catalog"] else "; sin referencia de clase"
                lines.append(f"{COMPARISONS[comparison]} · {EQUIPMENT_SLOTS[k]}: {count} detectados ({status}){ref}")
        if e["catalog"]: lines.append("Referencia QA ficticia/no canónica. Coincidencia no implica seguridad.")
        return "\n".join(lines)

    def _no_selection_dossier(self):
        if self.current_view == "configuration":
            d = self.state.get("diagnostic", [0, 0, 0, 0])
            return ("EQUIPO DE SENSORES\n\nPerfil Galaxy modernizada · Proyecto Valhalla.\n"
                    f"Capacidad: {d[1]/10:.1f}% · potencia: {d[2]/10:.1f}% · integridad: {d[3]/10:.1f}%")
        if self.current_view == "tracking":
            return "SEGUIMIENTO\n\nMarca un objetivo con Seguir. La vigilancia pasiva del resto continúa."
        if self.current_view == "results":
            return "ANÁLISIS\n\nElige Analizar sobre un contacto para consultar conocimiento adicional verificable."
        environment = self.state.get("environment", [])
        lines = ["ENTORNO OBSERVADO", "", "Sensores sin servicio." if self.state.get("offline") else "Vigilancia automática activa."]
        if environment and self.state.get("environment_source"):
            names = ("Electromagnetismo", "Banda térmica", "Gravimetría", "Subespacio", "Banda biológica")
            detected = [f"{name}: perturbación medida ({value/10:.1f}%)." for name, value in zip(names, environment) if value]
            lines += detected or ["Sin perturbaciones medidas en las bandas ambientales supervisadas."]
        else: lines.append("Lecturas ambientales aún no disponibles.")
        if any(c[1] == 17 and c[2] == 1 for c in self.state.get("contacts", [])):
            lines.append("Cinturón de asteroides observado en el mapa.")
        return "\n".join(lines)

    def show_selected(self):
        selection = self.contacts_table.selection()
        c = self.contact_map.get(selection[0]) if selection else None
        self.equipment_brief.pack_forget()
        self.technical_details = ""
        details = self._no_selection_dossier()
        if c:
            active = c[2] == 1
            historical = "" if active else "ÚLTIMA LECTURA · SEÑAL PERDIDA\n" + LOSS_CAUSES.get(c[7], "Causa no determinada") + "\n\n"
            if self.current_view == "results":
                details = self._deep_dossier(c)
            elif self.current_view == "tracking":
                details = self._tracking_dossier(c)
            else:
                lines = ["LECTURAS DEL OBJETO", "", f"Distancia: {c[5]/1000:.3f} UA",
                         f"Confianza de observación: {c[4]/10:.1f}%"]
                if c[1] in (1, 2):
                    design = STARSHIP_DESIGNS.get(c[3])
                    if design: lines.append("Diseño: " + design[1])
                    lines += ["Afiliación actual: sin acreditar.",
                              "Transpondedor declarado: " + (str(c[6]) if c[6] else "sin señal"),
                              "Nombre, matrícula, misión y tripulación: sin datos autorizados.", "", self._equipment_dossier(c)]
                elif c[1] == 13:
                    r = next((r for r in self.state.get("science", []) if r[0] == c[0]), None)
                    if r:
                        lines += ["", "CIENCIA PLANETARIA", f"Temperatura: {r[4]} K", f"Presión: {r[5]} mbar",
                                  f"Agua superficial: {r[6]/10:.1f}%", f"Nitrógeno: {r[7]/10:.1f}%",
                                  f"Oxígeno: {r[8]/10:.1f}%", f"CO₂: {r[9]/10:.1f}%",
                                  "Biosignales: " + {0:"sin determinar",1:"no detectadas",2:"posibles",3:"corroboradas"}.get(r[10], "sin determinar"),
                                  "Respirabilidad y civilización: sin confirmar."]
                    else: lines += ["", "Sin medición científica suficiente para clasificar el planeta."]
                elif c[1] == 12: lines += ["", "Espectro y composición estelar: no medidos por este contrato."]
                else: lines += ["", "Composición y estructura interna: sin lecturas verificables."]
                if self.technical_expanded:
                    az, el = self._bearing(c)
                    lines += ["", f"Azimut observado: {az:03d}° · elevación: {el:+d}°"]
                details = "\n".join(lines)
            details = historical + details
        key = (self.current_view, str(c[0]) if c else None)
        self._write_text(self.detail_text, details, reset=key != self.last_detail_key)
        self.last_detail_key = key
        for widget in (self.action_area, self.contact_report_button, self.voice_button,
                       self.tactical_report_button, self.science_transfer_button,
                       self.unfollow_button, self.technical_button): widget.pack_forget()
        if c:
            self.technical_button.pack(fill="x", pady=2)
            if c[2] == 1:
                self.action_area.pack(fill="x", pady=(4, 2))
                self.voice_button.pack(fill="x", pady=2)
                self.contact_report_button.pack(fill="x", pady=2)
                tracking = next((r[1] for r in self.state.get("tracking", []) if r[0] == c[0]), 0)
                if tracking:
                    self.follow_button.state(["disabled"])
                    self.unfollow_button.pack(fill="x", pady=2)
                else:
                    self.follow_button.state(["!disabled"])
                    if c[1] in (1,2): self.tactical_report_button.pack(fill="x", pady=2)
                if c[1] == 13 or self.current_view == "results": self.science_transfer_button.pack(fill="x", pady=2)
        self.scan_progress.pack_forget()

    def _update_scan_progress(self, contact):
        self.scan_progress.pack_forget()

    def open_contact_details(self) -> None:
        """Reveal meaningful readings in the RIGHT pane, not debug popups."""
        if not self.contacts_table.selection():
            return
        self.technical_expanded = not self.technical_expanded
        self.technical_button.configure(
            text="Ocultar lecturas complementarias" if self.technical_expanded
            else "Ver ficha técnica")
        self.show_selected()


    def apply_preset(self) -> None:
        name = self.sensor_preset.get()
        presets = {"Estándar": 0, "Alta resolución": 1,
                   "Antinterferencias": 2, "Máxima detección": 3}
        try:
            state = self.command(f"CONFIG {presets[name]}")
            self.apply(state)
            self.append(state["tick"], f"Configuración {name} aplicada mediante CoreRPG. "
                        "Sensores recalibrados; comprobar cambios en los contactos.")
        except Exception as exc:
            messagebox.showwarning("Sensores", f"No se pudo aplicar el perfil: {exc}", parent=self.root)

    def diagnostic(self) -> None:
        try:
            state = self.command("DIAG")
            self.apply(state)
            names = {1: "nominal", 2: "degradado", 3: "fuera de servicio",
                     4: "configuración deficiente"}
            code, capability, power, integrity = state["diagnostic"]
            self.append(state["tick"], f"Autodiagnóstico CoreRPG: {names.get(code, 'desconocido')}. "
                        f"Capacidad {capability / 10:.1f}%; alimentación {power / 10:.1f}%; "
                        f"integridad {integrity / 10:.1f}%.")
        except Exception as exc:
            messagebox.showwarning("Sensores", f"Autodiagnóstico no disponible: {exc}", parent=self.root)

    def contact_action(self, action):
        selected = self.contacts_table.selection()
        if not selected or selected[0] not in self.contact_map: return
        cid = selected[0]
        try:
            state = self.command(f"{action} {cid}")
            if action == "SCAN": self.analyzed_ids.add(cid)
            elif action == "PRIORITY": self.followed_ids.add(cid)
            elif action == "UNFOLLOW": self.followed_ids.discard(cid)
            self.apply(state)
            if action in ("SCAN", "PRIORITY"):
                self.navigate("results" if action == "SCAN" else "tracking")
                self._choose_contact(cid)
            self.append(state["tick"], {"SCAN":"Análisis disponible; consulta los hallazgos y sus límites.",
                        "PRIORITY":"Seguimiento activo. Datos compartidos automáticamente con Táctica · QA.",
                        "UNFOLLOW":"Seguimiento finalizado; vigilancia pasiva activa.",
                        "FOCUS":"Lectura actualizada."}[action])
        except Exception as exc:
            messagebox.showwarning("Sensores", str(exc), parent=self.root)

    def _choose_contact(self, cid: str) -> None:
        tree=self.contacts_table
        if tree.exists(cid):
            parent=tree.parent(cid)
            if parent:
                tree.item(parent, open=True)
                self.group_open[parent]=True
            tree.selection_set(cid)
            tree.focus(cid)
            tree.see(cid)
        self.show_selected()
        self._update_main_content()
        self._draw_map()

    def apply(self, state, reset=False):
        previous = self.state
        self.state = state
        self.x1 = state.get("mode") == 4
        self.speed_selector.configure(values=("×1",) if self.x1 else ("×1", "×15", "×30", "×60"))
        if self.x1: self.speed.set("×1")
        self.record.append(state)
        t = state["tick"]
        self.followed_ids.update(str(r[0]) for r in state.get("tracking", []) if r[1])
        self.new_contact_ids.update(str(c[0]) for c in state["contacts"])
        latest = {e["contact"]: e["id"] for e in state.get("equipment", [])}
        self.shared_report_ids = {str(d[1]) for d in state.get("deliveries", [])
                                  if d[4] == 1 and latest.get(d[1]) == d[2]}
        self.tactical_qa_ids = {str(d[1]) for d in state.get("deliveries", []) if d[4] == 2 and d[5] == 1}
        self.progress.configure(value=t, maximum=state.get("duration", 28800))
        self.timelabel.configure(text=f"{clock(t)} / {clock(state.get('duration', 28800))}")
        self.summary.configure(text="Sensores sin servicio" if state.get("offline") else "Vigilancia automática activa")
        self._refresh_contacts(state)
        self._update_view_content()
        if reset:
            self.append(t, "Sistema Aster observado. Vigilancia automática activa.")
        if previous and previous.get("offline") != state.get("offline"):
            self.append(t, "Sensores sin servicio; lecturas conservadas como histórico." if state.get("offline")
                        else "Sensores recuperados. Vigilancia automática restablecida.")
        self._update_alert(state)
        self._record_latency(state)
        if t >= state.get("duration", 28800):
            self.playing = False
            self.button_play.configure(text="Guardia finalizada", state="disabled")
            if previous.get("tick", -1) < t: self.append(t, "Guardia finalizada. Informe disponible para exportar.")

    def restore_watch_speed(self) -> None:
        """A new ship slows the clock, but the operator chooses when to accelerate."""
        self.speed.set(self.speed_before_alert)
        self.slowed_for_alert = False
        self.sim_half_seconds = 0
        self.restore_speed_button.pack_forget()
        self.append(self.state.get("tick", 0),
                    f"Guardia a velocidad {self.speed.get()} por decisión del oficial.")

    def _record_latency(self, state: dict) -> None:
        self.root.update_idletasks()
        displayed = time.monotonic()
        for row in state.get("latency", []):
            cid, tick, source, received, published = row
            key = (cid, source)
            if key in self.telemetry_seen:
                continue
            self.telemetry_seen.add(key)
            record = {"contact": cid, "tick": tick, "source_native_ns": source,
                      "core_receive_native_ns": received, "f06_publish_native_ns": published,
                      "gui_receive_monotonic_s": self.last_receipt,
                      "gui_display_monotonic_s": displayed,
                      "native_latency_s": (published-source)/1e9,
                      "mode": "ASTER_X1" if self.x1 else "eight_hours",
                      "realtime": self.playing and self.x1,
                      "source_to_gui_s": max(0, displayed-(self.wall_origin+tick))}
            if self.telemetry:
                self.telemetry.parent.mkdir(parents=True, exist_ok=True)
                with self.telemetry.open("a", encoding="utf-8") as log:
                    log.write(json.dumps(record) + "\n")

    def tick(self) -> None:
        now = time.monotonic()
        elapsed, self.last_wall = now-self.last_wall, now
        if self.playing and self.state.get("tick", 0) < self.state.get("duration", 28800):
            try:
                speed = 1 if self.x1 else int(self.speed.get()[1:])
                self.elapsed_fraction += elapsed*speed
                seconds = int(self.elapsed_fraction)
                self.elapsed_fraction -= seconds
                if seconds:
                    self.apply(self.command(f"STEP {seconds}"))
            except Exception as exc:
                self.playing = False
                self.button_play.configure(text="Reanudar")
                messagebox.showerror("Prueba F06", str(exc), parent=self.root)
        elif self.x1:
            # Pausing shifts the real-time origin; it never fabricates an SLA.
            self.wall_origin += elapsed
        self.tick_after = self.root.after(500, self.tick)

    def toggle(self) -> None:
        if self.state.get("tick", 0) >= self.state.get("duration", 28800):
            return
        self.last_wall = time.monotonic()
        self.wall_origin = self.last_wall-self.state.get("tick", 0)-self.elapsed_fraction
        self.playing = not self.playing
        self.button_play.configure(text="Pausar" if self.playing else "Reanudar")

    def restart(self) -> None:
        self.playing = False
        self.x1 = MODES.index(self.mode.get()) == 4
        self.last_wall = self.wall_origin = time.monotonic()
        self.elapsed_fraction = 0.0
        self.telemetry_seen.clear()
        self.equipment_seen.clear()
        self.speed.set("×1" if self.x1 else "×30")
        self.speed_before_alert = "×30"
        self.slowed_for_alert = False
        self.sim_half_seconds = 0
        self.restore_speed_button.pack_forget()
        self.button_play.configure(state="normal", text="Iniciar")
        self.lines.clear()
        self.record.clear()
        self.manual_jobs.clear()
        self.saved_manual_jobs.clear()
        self.operator_scan_ids.clear()
        self.saved_operator_scan_ids.clear()
        self.new_contact_ids.clear()
        self.followed_ids.clear()
        self.analyzed_ids.clear()
        self.shared_report_ids.clear()
        self.tactical_qa_ids.clear()
        self.saved_operator_views.clear()
        self.map_zoom=1.0
        self.map_overview=True
        self.designations = {}
        self.arrival_id = None
        self.alert_ids = []
        self.acknowledged_arrivals.clear()
        self.nav_events_seen.clear()
        self.nav_priority = None
        self.group_open.clear()
        self.saved_lines = None
        self.saved_notes = ""
        self.state = {}
        self.interrupted = None
        self.interrupted_stack.clear()
        self.seen_incidents.clear()
        self.incident_started.clear()
        self.active_alert = None
        self.resume_button.pack_forget()
        self.navigate("status")
        self.notice_label.configure(text="Vigilancia automática activada.")
        try:
            self.apply(self.command(f"RESTART {MODES.index(self.mode.get())}"), reset=True)
            self.playing = self.x1
            self.button_play.configure(text="Pausar" if self.x1 else "Iniciar")
        except Exception as exc:
            messagebox.showerror("Prueba F06", str(exc), parent=self.root)

    def disk_checkpoint(self, restore):
        if not self.x1: return
        self.playing = False
        self.button_play.configure(text="Reanudar")
        chooser = filedialog.askopenfilename if restore else filedialog.asksaveasfilename
        path = chooser(parent=self.root, defaultextension=".aster", filetypes=[("Guardia ASTER_X1", "*.aster")])
        if not path: return
        try:
            self.checkpoint_file(Path(path), restore)
        except Exception as exc:
            messagebox.showwarning("Sensores", str(exc), parent=self.root)

    def checkpoint(self, op):
        self.playing = False
        self.button_play.configure(state="normal", text="Reanudar")
        try:
            if op == "SAVE":
                self.saved_ui = self._ui_snapshot()
                self.apply(self.command("SAVE"))
            elif self.saved_ui is not None:
                self._restore_ui(self.command("LOAD"), self.saved_ui)
            else: return
            self.append(self.state["tick"], "Guardia y contexto conservados." if op == "SAVE" else "Guardia y estudio recuperados.")
        except Exception as exc:
            messagebox.showwarning("Sensores", str(exc), parent=self.root)

    def export(self) -> None:
        path = filedialog.asksaveasfilename(
            parent=self.root, defaultextension=".txt",
            filetypes=[("Texto", "*.txt")],
            initialfile=f"F06_Aster_{datetime.now():%Y%m%d_%H%M}.txt",
        )
        if not path:
            return
        contents = "\n".join([
            "F06 — SISTEMA ASTER · INFORME DE PRUEBA",
            f"Fecha: {datetime.now():%Y-%m-%d %H:%M}",
            f"Escenario: {self.mode.get()}",
            f"Último tiempo simulado: {clock(self.state.get('tick', 0))}",
            "",
            "EVENTOS PRESENTADOS AL OFICIAL:",
            *self.lines, "",
            "CONTACTOS REALMENTE OBSERVADOS POR CORERPG:",
            *[self._contact_description(c) for c in self.state.get("contacts", [])], "",
            "INFORMES CIENTÍFICOS REGISTRADOS EN CORERPG:",
            *[
                f"{self.designations.get(r[0], str(r[0]))}: clase {PLANET_CLASSES.get(r[1], '?')} "
                f"({'provisional' if r[3] else 'confirmada'}); confianza {r[2] / 10:.1f}%; "
                f"T={r[4]} K; P={r[5]} mbar; agua {r[6] / 10:.1f}%; "
                f"N2={r[7] / 10:.1f}%; O2={r[8] / 10:.1f}%; CO2={r[9] / 10:.1f}%; "
                f"biosignales={r[10]}."
                for r in self.state.get("science", [])
            ], "",
            "MEDICIONES SIN INFORME (diagnóstico técnico):",
            *[f"Contacto={e[0]}, fase={e[1]}, codigo_Core={e[2]}"
              for e in self.state.get("science_issues", [])], "",
            "ESTADO ACTUAL:",
            f"Sensores fuera de servicio: {bool(self.state.get('offline'))}",
            f"Interferencias EM: {self.state.get('interference_em', 0)}/550",
            f"Configuración: {self.state.get('config')}", "",
            "IMPRESIONES DEL JUGADOR:",
            self.notes.get("1.0", "end").strip(), "",
            "AUDITORÍA TÉCNICA CORE (fuentes públicas y acuses QA):",
            json.dumps({key: self.state.get(key, []) for key in
                        ("deliveries", "equipment", "position_evidence", "deep_analysis", "tracking")},
                       ensure_ascii=False, indent=2), "",
            "NOTA: prueba de CoreRPG con fixture QA Aster, no universo F13 ni UI LCARS final.",
        ])
        Path(path).write_text(contents, encoding="utf-8")
        messagebox.showinfo("Prueba F06", f"Informe guardado en:\n{path}", parent=self.root)

    def close(self) -> None:
        self.playing = False
        self.root.after_cancel(self.tick_after)
        try:
            self.process.terminate()
            self.process.wait(timeout=2)
        except Exception:
            self.process.kill()
        self.root.destroy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", required=True, type=Path)
    parser.add_argument("--mode", choices=("x1", "eight-hours"), default="x1")
    parser.add_argument("--telemetry", type=Path)
    args = parser.parse_args()
    if not args.runner.is_file():
        raise SystemExit(f"No existe el ejecutable nativo: {args.runner}")
    root = tk.Tk()
    try:
        Panel(root, args.runner, x1=args.mode == "x1", telemetry=args.telemetry)
    except Exception as exc:
        messagebox.showerror("Prueba F06", str(exc), parent=root)
        root.destroy()
        raise SystemExit(1) from exc
    root.mainloop()


if __name__ == "__main__":
    main()
