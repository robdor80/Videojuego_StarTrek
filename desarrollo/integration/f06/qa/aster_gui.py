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
from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

MODES = (
    "1. Guardia normal",
    "2. Repetición idéntica",
    "3. Interferencias",
    "4. Avería y recuperación",
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
# Tactical class data are *known catalog capabilities*, not live proof of
# activated weapons. Keep the operator's panel focused on decisions.
NAVAL_CAPABILITIES = {
    16: ("Crucero de batalla klingon",
         "Disruptores y torpedos de fotones",
         "Escudos deflectores; capacidad de camuflaje"),
    18: ("Transporte civil", "Armamento no acreditado", "Defensas no acreditadas"),
    6: ("Explorador científico de la Flota Estelar",
        "Capacidades tácticas: consultar el archivo de la clase",
        "Escudos: no verificados"),
}
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
    def __init__(self, root: tk.Tk, runner: Path) -> None:
        self.root = root
        root.title("USS Enterprise-D · Sensores · Sistema Aster")
        root.geometry("1100x840")
        root.minsize(820, 650)
        self.process = subprocess.Popen(
            [str(runner)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, encoding="utf-8", bufsize=1,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        self.speed = tk.StringVar(value="×30")
        self.mode = tk.StringVar(value=MODES[0])
        self.playing = False
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
        self.sensor_preset = tk.StringVar(value="Estándar")
        self._render()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.apply(self._read(), reset=True)
        self.root.after(500, self.tick)

    def _render(self) -> None:
        """F06: quiet, task-first console with no decorative LCARS skin.

        Overview is an expandable human-readable system inventory.
        A single current notice replaces the previous notice; history is optional.
        Native Core alerts pre-empt everything else, with direct contact access.
        """
        self.root.geometry("1330x850")
        self.root.minsize(1020, 640)
        # The operating rows stay visible even when a priority alert appears.
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.current_view = "status"
        self.workspace_labels = {
            "status": "SISTEMA",
            "contacts": "CONTACTOS",
            "scans": "BARRIDOS",
            "tracking": "SEGUIMIENTO",
            "results": "RESULTADOS",
            "configuration": "EQUIPO",
        }
        self.section_id = "summary"
        self.contact_subset = "all"
        self.group_open: dict[str, bool] = {}
        self.map_positions: list[tuple[float, float, str]] = []
        self.map_visible = False
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
                                    font=("Segoe UI", 16, "bold"),
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
        left = ttk.Frame(panes, width=180, padding=(0, 5))
        center = ttk.Frame(panes, width=710, padding=(8, 3))
        right = ttk.Frame(panes, width=440, padding=(8, 3))
        panes.add(left, weight=0)
        panes.add(center, weight=3)
        panes.add(right, weight=2)

        # The operator sees six task groups, not every technical F06 contract.
        ttk.Label(left, text="OPERACIONES", font=("Segoe UI", 12, "bold")
                  ).pack(anchor="w", pady=(0, 13))
        for view, name in self.workspace_labels.items():
            btn = ttk.Button(left, text=name, command=lambda key=view: self.navigate(key))
            btn.pack(fill="x", pady=4)
            self.navigation_buttons[view] = btn
        ttk.Separator(left).pack(fill="x", pady=(16, 9))
        self.secondary_frame = ttk.Frame(left)
        self.secondary_frame.pack(fill="x")
        ttk.Button(left, text="HISTORIAL DE AVISOS", command=self.open_history
                   ).pack(fill="x", pady=(20, 5))

        # CENTRE: the default view is a concise, expandable inventory.
        titlebar = ttk.Frame(center)
        titlebar.pack(fill="x", pady=(2, 9))
        self.workspace_title = ttk.Label(titlebar, text="SISTEMA ASTER",
                                          font=("Segoe UI", 16, "bold"))
        self.workspace_title.pack(side="left")
        self.map_button = ttk.Button(titlebar, text="Ver mapa", command=self.toggle_map)
        self.map_button.pack(side="right")
        self.section_info = ttk.Label(center, text="", font=("Segoe UI", 10))
        self.section_info.pack(fill="x", pady=(0, 9))

        self.map_box = ttk.Frame(center)
        self.map_canvas = tk.Canvas(self.map_box, height=126, background="#f8fafc",
                                    highlightthickness=0)
        self.map_canvas.pack(fill="both", expand=True)
        self.map_canvas.bind("<Configure>", lambda _: self._draw_map())
        self.map_canvas.bind("<Button-1>", self._select_map_contact)

        list_area = ttk.Frame(center)
        list_area.pack(fill="both", expand=True)
        self.contacts_table = ttk.Treeview(
            list_area, show="tree", height=7, selectmode="browse")
        self.contacts_table.heading("#0", text="Sistema estelar observado")
        self.contacts_table.column("#0", minwidth=290, width=550, stretch=True)
        self.contacts_table.tag_configure("group", font=("Segoe UI", 12, "bold"))
        self.contacts_table.tag_configure("contact", font=("Segoe UI", 11))
        self.contacts_table.tag_configure("lost", foreground="#7d8289")
        self.contacts_table.tag_configure("alert", foreground="#9a3412")
        self.contacts_table.pack(side="left", fill="both", expand=True)
        tree_scroll = ttk.Scrollbar(list_area, orient="vertical",
                                     command=self.contacts_table.yview)
        tree_scroll.pack(side="right", fill="y")
        self.contacts_table.configure(yscrollcommand=tree_scroll.set)
        self.contacts_table.bind(
            "<<TreeviewSelect>>", lambda _: (self.show_selected(), self._draw_map()))
        self.contacts_table.bind("<<TreeviewOpen>>", self._remember_group)
        self.contacts_table.bind("<<TreeviewClose>>", self._remember_group)

        # RIGHT: nothing but the selected item, and its available actions.
        ttk.Label(right, text="INFORMACIÓN DEL CONTACTO",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(2, 10))
        detail_box = ttk.Frame(right)
        detail_box.pack(fill="both", expand=True)
        self.detail_text = tk.Text(
            detail_box, height=7, state="disabled", relief="flat",
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

        self.action_area = ttk.LabelFrame(right, text="ÓRDENES", padding=8)
        self.identify_button = ttk.Button(
            self.action_area, text="IDENTIFICAR",
            command=lambda: self.contact_action("FOCUS"))
        self.identify_button.pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(self.action_area, text="ANÁLISIS DETALLADO",
                   command=lambda: self.contact_action("SCAN")).pack(
                       side="left", expand=True, fill="x", padx=2)
        ttk.Button(self.action_area, text="SEGUIR",
                   command=lambda: self.contact_action("PRIORITY")).pack(
                       side="left", expand=True, fill="x", padx=2)
        # The progress indicator is based on actual Core start/end ticks.
        self.scan_progress = ttk.Frame(right)
        self.scan_progress_label = ttk.Label(self.scan_progress, text="")
        self.scan_progress_label.pack(fill="x", pady=(0, 3))
        self.scan_progress_value = ttk.Progressbar(
            self.scan_progress, maximum=100, value=0)
        self.scan_progress_value.pack(fill="x")
        self.technical_button = ttk.Button(
            right, text="Consultar datos técnicos del contacto",
            command=self.open_contact_details)

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
        ttk.Combobox(testrow, textvariable=self.speed, values=("×15", "×30", "×60"),
                     state="readonly", width=5).pack(side="left", padx=(4, 15))
        ttk.Label(testrow, text="Incidencia").pack(side="left")
        scenario = ttk.Combobox(testrow, textvariable=self.mode, values=MODES,
                                state="readonly", width=24)
        scenario.pack(side="left", padx=(5, 12))
        scenario.bind("<<ComboboxSelected>>", lambda _: self.restart())
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

    def toggle_test_options(self) -> None:
        if self.test_area.winfo_manager():
            self.test_area.grid_remove()
        else:
            self.test_area.grid(row=5, column=0, sticky="ew", padx=12, pady=(0, 7))

    def toggle_map(self) -> None:
        self.map_visible = not self.map_visible
        self.map_button.configure(text="Ocultar mapa" if self.map_visible else "Ver mapa")
        if self.map_visible:
            self.map_box.pack(fill="x", after=self.section_info, pady=(0, 8))
            self._draw_map()
        else:
            self.map_box.pack_forget()

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
        """Switch only the operator's view; never stop autonomous sensors."""
        if view not in self.workspace_labels:
            return
        self.current_view = view
        self.contact_subset = "all"
        self.section_id = "summary"
        self.contact_filter.set("Todos")
        for key, button in self.navigation_buttons.items():
            button.state(["disabled"] if key == view else ["!disabled"])
        for child in self.secondary_frame.winfo_children():
            child.destroy()
        options = {
            "status": [("Todo el sistema", "all")],
            "contacts": [("Todos", "all"), ("Naves", "ships"),
                         ("Planetas", "planets"), ("Sin identificar", "unidentified"),
                         ("Perdidos", "lost")],
            "scans": [("Todos", "all"), ("Naves", "ships"), ("Planetas", "planets")],
            "tracking": [("Todos", "all"), ("Naves", "ships"), ("Perdidos", "lost")],
            "results": [("Todos", "all"), ("Planetas", "planets")],
            "configuration": [("Todos", "all")],
        }
        for label, section in options[view]:
            b = ttk.Button(self.secondary_frame, text=label,
                           command=lambda k=section: self.select_section(k))
            b.pack(fill="x", pady=3)
        self.workspace_title.configure(text={
            "status": "SISTEMA ASTER", "contacts": "CONTACTOS",
            "scans": "BARRIDOS", "tracking": "SEGUIMIENTO",
            "results": "RESULTADOS", "configuration": "EQUIPO",
        }[view])
        if self.state:
            self._refresh_contacts(self.state)
        self._update_view_content()
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

    def _update_alert(self, state: dict) -> None:
        """Large, persistent, direct-entry warning for observed sensor threats."""
        core_ids = [str(x) for x in state.get("attention_contacts", [])]
        if len(core_ids) != state.get("attention", 0):
            raise RuntimeError("Incoherencia en los contactos señalados por CoreRPG.")
        observed = {str(c[0]): c for c in state.get("contacts", [])}
        borg = [str(c[0]) for c in state.get("contacts", [])
                if c[1] == 1 and c[2] == 1 and c[3] == 10]
        arrival = self.arrival_id if self.arrival_id in observed and (
            observed[self.arrival_id][2] == 1) else None
        # New arrivals must be visible even if an earlier unknown ship is
        # still awaiting operator attention. Never bury them under old alerts.
        nav_target = (str(self.nav_priority[1]) if self.nav_priority
                      and str(self.nav_priority[1]) in observed else None)
        if borg:
            ids = borg
        else:
            ids = list(dict.fromkeys(
                ([nav_target] if nav_target else []) +
                ([arrival] if arrival else []) + core_ids))
        if not ids:
            self.alert_ids = []
            self.alert_bar.grid_remove()
            return
        if tuple(ids) != tuple(self.alert_ids):
            self.alert_cursor = 0
        self.alert_ids = ids
        self.alert_cursor %= len(ids)
        chosen = ids[self.alert_cursor]
        severity = "critical" if chosen in borg else "warning"
        if chosen in borg:
            title = "ALERTA PRIORITARIA · CONTACTO BORG"
            explanation = "Clase Borg identificada. Evaluación inmediata del oficial."
        elif chosen == nav_target and self.nav_priority:
            nav_kind, _, _, heading, trend, intercept = self.nav_priority
            if intercept:
                title = "ATENCIÓN · POSIBLE CURSO DE INTERCEPTACIÓN"
                explanation = (
                    f"Rumbo de desplazamiento {heading:03d}°. "
                    "La trayectoria observada converge hacia nuestra posición. "
                    "Aviso disponible para Táctica. Intención no determinada.")
            else:
                title = "ATENCIÓN · CAMBIO DE RUMBO"
                explanation = (
                    f"Nuevo rumbo estimado: {heading:03d}°. "
                    + ("El contacto se aproxima. " if trend == 1
                       else "El contacto se aleja. " if trend == 2 else "")
                    + "Seguimiento compartido con Táctica.")
        elif chosen == arrival:
            arriving = observed.get(chosen)
            class_name = STARSHIP_CLASSES.get(arriving[3]) if arriving else None
            title = ("NAVE DETECTADA · " + class_name.upper()
                     if class_name else "NUEVA NAVE DETECTADA")
            design = STARSHIP_DESIGNS.get(arriving[3]) if arriving else None
            explanation = (
                "Identificación inmediata completada. "
                + (f"Diseño: {design[1]}. " if design else "")
                + "Afiliación actual sin verificar. Velocidad de guardia reducida a ×1."
                if class_name else
                "Detección naval bajo investigación. Velocidad ×1; revisar sensores.")
        else:
            title = "ATENCIÓN · NAVE SIN IDENTIFICAR"
            explanation = ("La computadora intentó identificar este contacto "
                           "y no ha conseguido confirmar su clase.")
        contact = observed.get(chosen)
        if contact:
            label = self.designations.get(contact[0], "C-" + ids[self.alert_cursor][-6:])
            identity = contact_identification(contact)
            summary = (f"{label}  ·  {identity}  ·  "
                       f"{contact[5] / 1000:.3f} UA")
        else:
            summary = "Señal observada: ficha no disponible temporalmente."
        bg, ink, stroke = (
            ("#fecaca", "#7f1d1d", "#b91c1c") if severity == "critical"
            else ("#ffe2a1", "#78350f", "#b45309")
        )
        for widget in (self.alert_bar, self.alert_title, self.alert_description):
            widget.configure(background=bg)
        self.alert_bar.configure(highlightbackground=stroke)
        self.alert_title.configure(text=title, foreground=ink)
        self.alert_description.configure(text=summary + "\n" + explanation,
                                          foreground=ink)
        self.alert_button.configure(text=(
            "ABRIR CONTACTO" if len(ids) == 1 else
            f"ABRIR CONTACTO {self.alert_cursor + 1}/{len(ids)}"),
            background=stroke, activebackground=ink)
        if not self.alert_bar.winfo_manager():
            self.alert_bar.grid(row=1, column=0, sticky="ew",
                                padx=12, pady=(0, 6))

    def open_alert_contact(self) -> None:
        if not self.alert_ids:
            return
        cid = self.alert_ids[self.alert_cursor]
        if cid not in self.contact_map:
            return
        self.navigate("contacts")
        self.select_section("all")
        if self.contacts_table.exists(cid):
            parent = self.contacts_table.parent(cid)
            if parent:
                self.contacts_table.item(parent, open=True)
                self.group_open[parent] = True
            self.contacts_table.selection_set(cid)
            self.contacts_table.focus(cid)
            self.contacts_table.see(cid)
            self.show_selected()
            self._draw_map()
        if self.nav_priority and cid == str(self.nav_priority[1]):
            self.nav_priority = None
        if cid == self.arrival_id:
            self.acknowledged_arrivals.add(cid)
            self.arrival_id = None
        if len(self.alert_ids) > 1:
            self.alert_cursor = (self.alert_cursor + 1) % len(self.alert_ids)
        self._update_alert(self.state)


    def _read(self) -> dict:
        assert self.process.stdout is not None
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError("El proceso nativo de CoreRPG ha terminado inesperadamente.")
        result = json.loads(line)
        if not result.get("ok"):
            raise RuntimeError(result.get("error", "Error desconocido del motor."))
        return result

    def command(self, text: str) -> dict:
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

    def _draw_map(self) -> None:
        """XY projection of observed positions; no hidden world coordinates."""
        if not hasattr(self, "map_canvas"):
            return
        cv = self.map_canvas
        cv.delete("all")
        w, h = cv.winfo_width(), cv.winfo_height()
        if w < 60 or h < 60:
            return
        cx, cy = w / 2, h / 2
        cv.create_line(12, cy, w - 12, cy, fill="#cbd5e1")
        cv.create_line(cx, 12, cx, h - 12, fill="#cbd5e1")
        cv.create_text(16, 14, text="Y+", anchor="w", fill="#475569")
        cv.create_text(w - 16, cy - 12, text="X+", anchor="e", fill="#475569")
        cv.create_text(cx + 5, cy + 12, text="NAVE", anchor="nw",
                       fill="#1e40af")
        cv.create_polygon(cx, cy - 6, cx - 5, cy + 5, cx + 5, cy + 5,
                          fill="#1e40af")
        self.map_positions = []
        if not self.state:
            return
        rows = [self.contact_map[k] for group in self.contacts_table.get_children()
                for k in self.contacts_table.get_children(group)
                if k in self.contact_map]
        if not rows:
            cv.create_text(w / 2, h - 18, text="Sin contactos visibles en este filtro")
            return
        radius = max(100, max(abs(c[8]) for c in rows), max(abs(c[9]) for c in rows))
        scale = 0.44 * min(w, h) / radius
        cv.create_text(w - 10, h - 9,
                       text=f"±{radius / 1000:.2f} UA · plano XY",
                       anchor="se", fill="#475569")
        selected = self.contacts_table.selection()
        selected_id = selected[0] if selected else None
        for c in rows:
            key = str(c[0])
            px, py = cx + c[8] * scale, cy - c[9] * scale
            size = 6 if c[1] in (1, 2) else 4
            color = "#155e75" if c[2] == 1 else "#9ca3af"
            if c[1] in (12, 13, 14):
                color = "#64748b" if c[2] == 1 else "#cbd5e1"
            if key == selected_id:
                cv.create_oval(px - 10, py - 10, px + 10, py + 10,
                              outline="#2563eb", width=2)
                size = 7
            if c[2] != 1:
                cv.create_line(px - size, py - size, px + size, py + size,
                               fill=color, width=2)
                cv.create_line(px - size, py + size, px + size, py - size,
                               fill=color, width=2)
            else:
                cv.create_oval(px - size, py - size, px + size, py + size,
                              fill=color, outline="")
            self.map_positions.append((px, py, key))
        cv.create_text(10, h - 9, text=f"{len(rows)} contactos representados",
                       anchor="sw", fill="#475569")

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
        stars = [c for c in state["contacts"] if c[1] == 12]
        planets = [c for c in state["contacts"] if c[1] == 13]
        if stars:
            star = stars[0]
            planets.sort(key=lambda c: sum(
                (c[8 + i] - star[8 + i]) ** 2 for i in range(3)))
            roman = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII",
                     "IX", "X", "XI", "XII")
            for idx, planet in enumerate(planets):
                self.designations.setdefault(
                    planet[0], "Aster " + (roman[idx] if idx < len(roman)
                                                  else str(idx + 1)))
            self.designations.setdefault(star[0], "Aster · estrella central")
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
            if key == "planet":
                classes = Counter(PLANET_CLASSES.get(reports[c[0]][1], "?")
                                  for c in rows if c[0] in reports
                                  and reports[c[0]][1] != 0)
                if classes:
                    extra = "   ·   " + ", ".join(
                        f"{n} clase {cls}" for cls, n in sorted(classes.items()))
            groupid = "group:" + key
            retained_groups.add(groupid)
            heading = f"{names[key].upper()}  ·  {len(rows)}{extra}"
            if not tree.exists(groupid):
                tree.insert("", "end", iid=groupid, text=heading,
                            open=self.group_open.get(groupid, False),
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

    def _tree_contact_label(self, contact: list, reports: dict) -> str:
        name = self.designations.get(
            contact[0], "C-" + str(contact[0])[-6:])
        kind, status = contact[1], contact[2]
        suffix = ""
        if kind == 13 and contact[0] in reports:
            r = reports[contact[0]]
            if r[1]:
                suffix = "   ·   clase " + PLANET_CLASSES.get(r[1], "?")
                if r[3]:
                    suffix += " (provisional)"
        elif kind in (1, 2):
            klass = STARSHIP_CLASSES.get(contact[3]) if contact[3] else None
            suffix = "   ·   " + (klass or "sin identificar")
            if contact[6]:
                suffix += f"   ·   TP {contact[6]}"
        if status != 1:
            suffix += "   ·   SEÑAL PERDIDA"
        return name + suffix


    def _no_selection_dossier(self) -> str:
        state = self.state
        if not state:
            return "INFORMACIÓN\n\nEsperando datos del sistema."
        if self.current_view == "configuration":
            diagnostic = state.get("diagnostic", [0, 0, 0, 0])
            status = {1: "Nominal", 2: "Degradado", 3: "Sin servicio",
                      4: "Revisar configuración"}.get(diagnostic[0], "No disponible")
            return (
                "EQUIPO DE SENSORES\n\n"
                f"Estado: {status}\n"
                f"Potencia: {diagnostic[2] / 10:.1f}%\n"
                f"Integridad: {diagnostic[3] / 10:.1f}%\n"
                f"Capacidad: {diagnostic[1] / 10:.1f}%\n"
                f"Interferencia EM: {state.get('interference_em', 0)}/550\n\n"
                "Elige un perfil o ejecuta un autodiagnóstico."
            )
        if self.current_view == "results":
            jobs = state.get("scans", [])
            return (
                "ESTUDIOS\n\n"
                f"En curso: {sum(j[5] == 1 for j in jobs)}\n"
                f"Terminados: {sum(j[5] == 2 for j in jobs)}\n"
                f"Informes planetarios: {len(state.get('science', []))}\n\n"
                "Selecciona un objeto para consultar sus resultados."
            )
        return (
            "SISTEMA ASTER\n\n"
            "Selecciona un elemento de la lista para ver lo que "
            "los sensores saben de él.\n\n"
            "Despliega las categorías que quieras consultar. "
            "La computadora continúa vigilando en automático."
        )

    def show_selected(self) -> None:
        selection = self.contacts_table.selection()
        c = self.contact_map.get(selection[0]) if selection else None
        details = self._no_selection_dossier()
        self.technical_details = ""
        if c is not None:
            name = self.designations.get(c[0], "Contacto C-" + str(c[0])[-6:])
            typ = TYPES.get(c[1], "Señal desconocida")
            klass_name = STARSHIP_CLASSES.get(c[3]) if c[1] in (1, 2) else None
            heading = (
                f"{'LANZADERA' if c[1] == 2 else 'NAVE'} · CLASE {klass_name.upper()}"
                if klass_name else
                "NAVE · IDENTIDAD PENDIENTE" if c[1] == 1 else name.upper())
            if c[1] in (1, 2):
                klass = STARSHIP_CLASSES.get(c[3])
                profile = NAVAL_CAPABILITIES.get(c[3])
                description = profile[0] if profile else (
                    STARSHIP_DESIGNS.get(c[3], ("Clase de nave no catalogada",))[0])
                heading = (
                    f"{description.upper()} · {klass.upper()}"
                    if klass else "NAVE · IDENTIFICACIÓN PENDIENTE"
                )
                nav = next(
                    (row for row in self.state.get("navigation", [])
                     if row[0] == c[0]), None)
                details = f"{heading}\n\n"
                details += f"Distancia: {c[5] / 1000:.3f} UA\n"
                if nav and c[2] == 1:
                    _, measured_at, direction, tendency, intercept, closest = nav
                    age = max(0, self.state["tick"] - measured_at)
                    if age <= 300:
                        tendency_es = {1: "Se acerca", 2: "Se aleja",
                                       0: "Sin variación apreciable"}
                        details += (
                            f"Rumbo de desplazamiento: {direction:03d}° (estimado)\n"
                            f"Movimiento: {tendency_es.get(tendency, 'Sin determinar')}\n"
                        )
                        if intercept:
                            details += (
                                "\n¡POSIBLE TRAYECTORIA DE INTERCEPTACIÓN!\n"
                                "La trayectoria observada apunta hacia nuestra posición.\n"
                            )
                    else:
                        details += "Trayectoria: esperando actualización de sensores.\n"
                else:
                    details += "Rumbo y movimiento: calculando trayectoria…\n"
                if profile:
                    details += (
                        "\nCAPACIDADES CONOCIDAS DE LA CLASE\n"
                        f"Armamento habitual: {profile[1]}\n"
                        f"Defensas habituales: {profile[2]}\n"
                    )
                else:
                    details += (
                        "\nCAPACIDADES CONOCIDAS DE LA CLASE\n"
                        "Armamento: consultar catálogo táctico.\n"
                    )
                details += (
                    "\nTÁCTICA\n"
                    "Seguimiento compartido con el canal de sensores.\n"
                    "Esta ficha no confirma intenciones hostiles.\n"
                )
            else:
                details = f"{heading}\n\n"
                details += f"Distancia: {c[5] / 1000:.3f} UA\n"
            if c[2] == 2:
                details += ("\nSEÑAL PERDIDA\n"
                            + LOSS_CAUSES.get(c[7], "Causa desconocida") + "\n")
            reports = [r for r in self.state.get("science", []) if r[0] == c[0]]
            if reports:
                r = reports[-1]
                bio = {0: "Sin estudiar", 1: "No detectadas", 2: "Posibles",
                       3: "Corroboradas"}.get(r[10], "No determinado")
                details += (
                    "\nDATOS PLANETARIOS\n"
                    f"Clase: {PLANET_CLASSES.get(r[1], '?')}"
                    f"{' · provisional' if r[3] else ''}\n"
                    f"Temperatura: {r[4]} K\n"
                    f"Presión: {r[5]} mbar\n"
                    f"Agua superficial: {r[6] / 10:.0f}%\n"
                    f"Oxígeno: {r[8] / 10:.1f}%\n"
                    f"Biosignales: {bio}\n"
                )
                if r[8] < 100 or r[5] < 300:
                    details += "\nAVISO: atmósfera no respirable sin asistencia.\n"
                else:
                    details += "\nRespirabilidad: no confirmada.\n"
                self.technical_details += (
                    "INFORME CIENTÍFICO CORE\n"
                    f"Confianza informe: {r[2] / 10:.1f}%\n"
                    f"Nitrógeno: {r[7] / 10:.1f}%\n"
                    f"CO₂: {r[9] / 10:.1f}%\n"
                    "Habitantes y civilización: sin determinar.\n\n"
                )
            elif c[1] == 13:
                details += "\nDATOS PLANETARIOS\nTodavía sin informe científico.\n"
            elif c[1] == 12:
                details += "\nTipo espectral: no determinado.\n"
            jobs = [j for j in self.state.get("scans", []) if j[1] == c[0]]
            active = [j for j in jobs if j[5] == 1]
            complete = [j for j in jobs if j[5] == 2]
            # Routine job counts are backend metadata, never part of the
            # operator's naval or astronomical decision panel.
            if jobs and self.current_view == "results" and c[1] not in (1, 2):
                details += "\nESTUDIOS\n"
                if active:
                    details += f"En curso: {len(active)}\n"
                if complete:
                    details += (f"Terminados: {len(complete)}\n"
                                f"Último: {clock(complete[-1][3])}\n")
            comparison = next(
                (row for row in self.state.get("comparisons", [])
                 if row[0] == c[0]), None)
            if comparison and c[1] not in (1, 2):
                _, count, old_tick, new_tick, dc, dd, changed = comparison
                details += (
                    "\nARCHIVO DE SENSORES · COMPARACIÓN\n"
                    f"Comparadas: {clock(old_tick)} y {clock(new_tick)}\n"
                    f"Variación de distancia: {dd / 1000:+.3f} UA\n"
                    f"Clasificación: {'Ha cambiado' if changed else 'Sin cambios confirmados'}\n"
                )
            if str(c[0]) in self.alert_ids:
                details += "\nREQUIERE ATENCIÓN DEL OFICIAL\n"
            self.technical_details += self._contact_description(c) + "\n"
            for j in jobs:
                self.technical_details += (
                    f"\nEstudio {j[0]}: inicio {clock(j[2])}; "
                    f"fin previsto {clock(j[3])}; estado {j[5]}; "
                    f"resultado Core {j[4]}."
                )

        # Leave the dossier scroll where the officer placed it. Its text
        # may change as Core publishes new readings, but the 500-ms refresh
        # must not forcibly jump to the first line.
        old_details = self.detail_text.get("1.0", "end-1c")
        if old_details != details:
            y_before = self.detail_text.yview()[0]
            self.detail_text.configure(state="normal")
            self.detail_text.delete("1.0", "end")
            self.detail_text.insert("1.0", details)
            self.detail_text.tag_add("heading", "1.0", "1.end")
            for section in ("CAPACIDADES CONOCIDAS DE LA CLASE", "TÁCTICA",
                            "DATOS PLANETARIOS",
                            "ARCHIVO DE SENSORES · COMPARACIÓN", "ESTUDIOS",
                            "SEÑAL PERDIDA", "REQUIERE ATENCIÓN DEL OFICIAL",
                            "¡POSIBLE TRAYECTORIA DE INTERCEPTACIÓN!"):
                start = self.detail_text.search(section, "2.0", "end")
                if start:
                    self.detail_text.tag_add(
                        "section", start, f"{start}+{len(section)}c")
            self.detail_text.configure(state="disabled")
            self.detail_text.yview_moveto(y_before)
        if c is not None:
            if c[2] == 1:
                self.identify_button.configure(
                    text="IDENTIFICAR" if c[1] in (1, 2) else "ANÁLISIS RÁPIDO")
                if not self.action_area.winfo_manager():
                    self.action_area.pack(fill="x", pady=(7, 4))
            else:
                self.action_area.pack_forget()
            if not self.technical_button.winfo_manager():
                self.technical_button.pack(fill="x", pady=4)
        else:
            self.action_area.pack_forget()
            self.technical_button.pack_forget()
        self._update_scan_progress(c)

    def _update_scan_progress(self, contact: list | None) -> None:
        """Only operator-requested long scans get a progress indicator."""
        if contact is None:
            self.scan_progress.pack_forget()
            return
        jobs = [j for j in self.state.get("scans", [])
                if j[1] == contact[0] and j[0] in self.operator_scan_ids]
        if not jobs:
            self.scan_progress.pack_forget()
            return
        job = max(jobs, key=lambda row: (row[2], row[0]))
        duration = max(1, job[3] - job[2])
        percent = min(100, max(0, round(
            100 * (self.state["tick"] - job[2]) / duration)))
        if job[5] == 2:
            percent = 100
            label = "Análisis detallado · 100 % · lectura conservada"
        elif job[5] == 1:
            label = f"Análisis detallado · {percent} % · en curso"
        else:
            label = "Análisis interrumpido · sin resultado confirmado"
            percent = 0
        self.scan_progress_label.configure(text=label)
        self.scan_progress_value["value"] = percent
        if not self.scan_progress.winfo_manager():
            self.scan_progress.pack(fill="x", pady=(3, 6))

    def open_contact_details(self) -> None:
        if not self.technical_details:
            return
        window = tk.Toplevel(self.root)
        window.title("Sensores · Datos de la observación")
        window.geometry("730x420")
        area = tk.Text(window, font=("Segoe UI", 11), wrap="word", padx=15, pady=15)
        area.pack(fill="both", expand=True)
        area.insert("1.0", self.technical_details)
        area.configure(state="disabled")


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

    def contact_action(self, action: str) -> None:
        selected = self.contacts_table.selection()
        if not selected:
            messagebox.showinfo("Sensores", "Selecciona primero un contacto.", parent=self.root)
            return
        contact = self.contact_map[selected[0]]
        if contact[2] != 1:
            messagebox.showwarning("Sensores", "Ese contacto está perdido y no puede analizarse todavía.", parent=self.root)
            return
        try:
            old_jobs = {j[0] for j in self.state.get("scans", [])}
            state = self.command(f"{action} {contact[0]}")
            if action == "SCAN":
                created = [j for j in state["scans"]
                           if j[0] not in old_jobs and j[1] == contact[0]]
                for job in created:
                    self.manual_jobs[job[0]] = contact[0]
                    self.operator_scan_ids.add(job[0])
            self.apply(state)
            reference = "C-" + selected[0][-6:]
            if action == "FOCUS":
                updated = self.contact_map.get(str(contact[0]), contact)
                if updated[1] in (1, 2):
                    klass = STARSHIP_CLASSES.get(updated[3])
                    message = (
                        f"Identificación rápida de {reference}: clase {klass}."
                        if klass else
                        f"Lectura rápida de {reference} terminada: clase sin confirmar. "
                        "No hay firma suficiente para identificarla.")
                else:
                    message = (
                        f"Análisis rápido de {reference}: "
                        f"{TYPES.get(updated[1], 'señal')} observado. "
                        "El expediente contiene los datos disponibles.")
            elif action == "SCAN":
                message = (
                    f"Análisis detallado de {reference} iniciado. "
                    "Progreso y resultados en el expediente del contacto.")
            else:
                message = f"Seguimiento prioritario establecido sobre {reference}."
            self.append(state["tick"], message)
        except Exception as exc:
            messagebox.showwarning("Sensores", f"No ha sido posible: {exc}", parent=self.root)

    def apply(self, state: dict, reset: bool = False) -> None:
        previous = self.state
        self.state = state
        self.record.append(state)
        t = state["tick"]
        self.progress["value"] = t
        self.timelabel.configure(text=f"Guardia: {clock(t)} / 08:00:00")
        if state["offline"]:
            status = "Sensores fuera de servicio · vigilancia degradada"
        else:
            status = f"Vigilancia activa · {state['active']} contactos"
        self.summary.configure(text=status)
        # Dynamic course and interception warnings come from consecutive
        # observed positions in the native Core sensor projection.
        self._refresh_contacts(state)
        for evt in state.get("navigation_alerts", []):
            kind, cid, when, heading, trend, intercept = evt
            key = (kind, cid, when)
            if key in self.nav_events_seen:
                continue
            self.nav_events_seen.add(key)
            contact = self.contact_map.get(str(cid))
            if not contact:
                continue
            klass = STARSHIP_CLASSES.get(contact[3], "nave")
            if kind == 2:
                msg = (f"ALERTA DE SENSORES: {klass}, posible rumbo de "
                       f"interceptación ({heading:03d}°). Informar a Táctica.")
                self.nav_priority = evt
            elif kind == 1:
                msg = (f"Maniobra detectada: {klass} cambia de rumbo a "
                       f"{heading:03d}°. "
                       + ("Se aproxima." if trend == 1 else
                          "Se aleja." if trend == 2 else
                          "Trayectoria lateral."))
                self.nav_priority = evt
            elif kind == 3:
                msg = f"Seguimiento: {klass} se aproxima. Rumbo {heading:03d}°."
            else:
                msg = f"Seguimiento: {klass} se aleja. Rumbo {heading:03d}°."
            self.append(when, msg)
        self._update_alert(state)
        self._update_view_content()
        if reset:
            visible = [c for c in state["contacts"] if c[2] == 1]
            counts = Counter(c[1] for c in visible)
            def amount(key: int, singular: str, plural: str) -> str:
                n = counts.get(key, 0)
                return f"{n} {singular if n == 1 else plural}"
            summary = ", ".join([
                amount(12, "estrella", "estrellas"),
                amount(13, "planeta", "planetas"),
                amount(14, "luna", "lunas"),
                amount(15, "nebulosa", "nebulosas"),
                amount(16, "estación", "estaciones"),
                amount(1, "nave", "naves"),
                amount(2, "lanzadera", "lanzaderas"),
                amount(3, "sonda", "sondas"),
            ])
            self.append(t, "Barrido panorámico: " + summary + ".")
            classes = Counter(
                r[1] for r in state["science"] if r[1] and r[3]
            )
            if classes:
                found = ", ".join(
                    f"{n} clase {PLANET_CLASSES.get(cls, '?')} provisional"
                    for cls, n in sorted(classes.items())
                )
                self.append(t, "Informe científico inicial autorizado: " + found + ".")
            interesting = [r for r in state["science"] if r[10] >= 2 and r[2] >= 650]
            for report in interesting:
                designation = self.designations.get(report[0], "contacto " + str(report[0])[-6:])
                self.append(t, f"Atención científica: indicios de biosignales en {designation}. "
                            "Vida inteligente y civilización NO determinadas.")
            for report in state["science"]:
                if report[1] == 1 and report[8] < 100:
                    designation = self.designations.get(report[0], "contacto " + str(report[0])[-6:])
                    self.append(t, f"Precaución: {designation} presenta clasificación M provisional, "
                                "pero el oxígeno medido no permite asumir una atmósfera respirable.")
            unidentified = sum(1 for c in visible if c[1] == 1 and c[3] == 0)
            if unidentified:
                self.append(t, f"{unidentified} contacto(s) navales sin clase confirmada. "
                            "El operador puede consultarlos o priorizarlos.")
            self.append(t, "Vigilancia automática establecida. Los análisis rutinarios quedan en segundo plano.")
        if previous and previous.get("interference_em", 0) != state.get("interference_em", 0):
            level = state["interference_em"]
            self.append(t, (
                f"Interferencias electromagnéticas detectadas (índice {level}/550). "
                "La detección puede estar degradada." if level else
                "Interferencias electromagnéticas remitidas. Sensores recuperando contactos."
            ))
        if previous and previous.get("offline", 0) != state["offline"]:
            self.append(t, "Avería: sensores sin servicio." if state["offline"] else
                        "Sensores nuevamente operativos.")
        background_losses: Counter = Counter()
        background_reacquired: Counter = Counter()
        for kind, contact_id, when, category, klass in state["events"]:
            if not reset and when > 0 and kind == 1 and category in (1, 2):
                candidate = str(contact_id)
                observed = self.contact_map.get(candidate)
                if (observed and observed[2] == 1 and
                        candidate not in self.acknowledged_arrivals):
                    self.arrival_id = candidate
                    if not self.slowed_for_alert:
                        self.speed_before_alert = self.speed.get()
                    self.slowed_for_alert = True
                    self.speed.set("×1")
                    self.sim_half_seconds = 0
                    self.restore_speed_button.configure(
                        text=f"Volver a {self.speed_before_alert}")
                    if not self.restore_speed_button.winfo_manager():
                        self.restore_speed_button.pack(
                            side="left", padx=(12, 0))
            contact = self.contact_map.get(str(contact_id))
            ident = contact_identification(contact) if contact else TYPES.get(category, "señal")
            short_ref = "C-" + str(contact_id)[-6:]
            if reset and kind in (1, 4):
                continue  # the initial panoramic briefing already covers these
            if kind == 1 and category in (12, 13, 14, 15, 17):
                continue  # normal astronomical detections are inventory, not alarms
            if kind == 1:
                label = TYPES.get(category, "señal de naturaleza desconocida")
                msg = f"Nuevo contacto {short_ref}: {label}. Identificación bajo vigilancia."
            elif kind == 2:
                if category in (12, 13, 14, 15, 17) and state.get("interference_em", 0):
                    background_losses[when] += 1
                    continue
                cause = LOSS_CAUSES.get(contact[7], "causa no determinada") if contact else "causa no determinada"
                if cause == "causa no determinada" and state.get("interference_em", 0):
                    cause = "interferencias presentes; relación causal no confirmada"
                msg = f"Se pierde el contacto {short_ref} ({ident}). Causa: {cause}."
            elif kind == 3:
                if category in (12, 13, 14, 15, 17):
                    background_reacquired[when] += 1
                    continue
                msg = f"Contacto recuperado {short_ref}: {ident}."
            elif kind == 4:
                if not klass:
                    continue
                msg = f"Identificación: contacto {short_ref}, {ident}."
            elif kind in (5, 6):
                continue  # automatic routine operations are recorded only in Core
            elif kind == 7:
                if category in (12, 13, 14, 15, 17):
                    continue
                msg = f"No ha sido posible completar el análisis de {short_ref}. Consultar expediente."
            else:
                continue
            self.append(when, msg)
        for when, count in sorted(background_losses.items()):
            self.append(when, f"Vigilancia astronómica degradada: {count} señales temporalmente no detectables. "
                        "Revisar condiciones de los sensores.")
        for when, count in sorted(background_reacquired.items()):
            self.append(when, f"Vigilancia astronómica restablecida: {count} señales recuperadas.")

        for job in state.get("scans", []):
            if job[0] not in self.manual_jobs or job[5] == 1:
                continue
            target = self.manual_jobs.pop(job[0])
            result = {2: "completado y registrado", 3: "fallido",
                      4: "cancelado"}.get(job[5], "estado desconocido")
            self.append(t, f"Estudio solicitado de C-{str(target)[-6:]}: {result}.")
        self._update_alert(state)
        if t >= 28800:
            self.playing = False
            self.button_play.configure(text="Guardia finalizada", state="disabled")
            self.append(t, "Guardia finalizada. Exporta el informe cuando quieras.")

    def restore_watch_speed(self) -> None:
        """A new ship slows the clock, but the operator chooses when to accelerate."""
        self.speed.set(self.speed_before_alert)
        self.slowed_for_alert = False
        self.sim_half_seconds = 0
        self.restore_speed_button.pack_forget()
        self.append(self.state.get("tick", 0),
                    f"Guardia a velocidad {self.speed.get()} por decisión del oficial.")

    def tick(self) -> None:
        if self.playing and self.state.get("tick", 0) < 28800:
            try:
                # Advance one simulated second every two 500-ms ticks at ×1.
                # Integer half-seconds also preserve exact ×15 cadence.
                self.sim_half_seconds += int(self.speed.get()[1:])
                sim_seconds, self.sim_half_seconds = divmod(
                    self.sim_half_seconds, 2)
                if sim_seconds:
                    self.apply(self.command(f"STEP {sim_seconds}"))
            except Exception as exc:
                self.playing = False
                self.button_play.configure(text="Reanudar")
                messagebox.showerror("Prueba F06", str(exc), parent=self.root)
        self.root.after(500, self.tick)

    def toggle(self) -> None:
        if self.state.get("tick", 0) >= 28800:
            return
        self.playing = not self.playing
        self.button_play.configure(text="Pausar" if self.playing else "Reanudar")

    def restart(self) -> None:
        self.playing = False
        self.speed.set("×30")
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
        self.notice_label.configure(text="Vigilancia automática activada.")
        try:
            self.apply(self.command(f"RESTART {MODES.index(self.mode.get())}"), reset=True)
        except Exception as exc:
            messagebox.showerror("Prueba F06", str(exc), parent=self.root)

    def checkpoint(self, op: str) -> None:
        self.playing = False
        self.button_play.configure(state="normal", text="Reanudar")
        try:
            if op == "SAVE":
                state = self.command(op)
                self.saved_lines = list(self.lines)
                self.saved_manual_jobs = dict(self.manual_jobs)
                self.saved_operator_scan_ids = set(self.operator_scan_ids)
                self.saved_notes = self.notes.get("1.0", "end").strip()
                self.apply(state)
                self.append(state["tick"], "Bitácora y estado de guardia conservados.")
            else:
                if self.saved_lines is None:
                    messagebox.showinfo("Sensores", "Todavía no hay ningún punto guardado.", parent=self.root)
                    return
                state = self.command(op)
                self.lines = list(self.saved_lines)
                self.manual_jobs = dict(self.saved_manual_jobs)
                self.operator_scan_ids = set(self.saved_operator_scan_ids)
                self.record.clear()
                self.state = {}  # loading must not create a false state-transition alarm
                self.arrival_id = None
                self.alert_ids = []
                self.notice_label.configure(text=self.lines[-1] if self.lines else "")
                self.notes.delete("1.0", "end")
                self.notes.insert("1.0", self.saved_notes)
                self.apply(state)
                self.append(state["tick"], "Guardia recuperada desde el estado persistido en CoreRPG.")
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
            "NOTA: prueba de CoreRPG con fixture QA Aster, no universo F13 ni UI LCARS final.",
        ])
        Path(path).write_text(contents, encoding="utf-8")
        messagebox.showinfo("Prueba F06", f"Informe guardado en:\n{path}", parent=self.root)

    def close(self) -> None:
        self.playing = False
        try:
            self.process.terminate()
            self.process.wait(timeout=2)
        except Exception:
            self.process.kill()
        self.root.destroy()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runner", required=True, type=Path)
    args = parser.parse_args()
    if not args.runner.is_file():
        raise SystemExit(f"No existe el ejecutable nativo: {args.runner}")
    root = tk.Tk()
    try:
        Panel(root, args.runner)
    except Exception as exc:
        messagebox.showerror("Prueba F06", str(exc), parent=root)
        root.destroy()
        raise SystemExit(1) from exc
    root.mainloop()


if __name__ == "__main__":
    main()
