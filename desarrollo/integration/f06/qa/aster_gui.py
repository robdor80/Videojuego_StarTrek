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
}
PLANET_CLASSES = {0: "sin determinar", 1: "M", 2: "H", 3: "J",
                  4: "L", 5: "P", 6: "Y"}
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
        self.lines: list[str] = []
        self.record: list[dict] = []
        self.state: dict = {}
        self.contact_map: dict[str, list] = {}
        self.designations: dict[int, str] = {}
        self.saved_lines: list[str] | None = None
        self.saved_notes = ""
        self.manual_jobs: dict[int, int] = {}
        self.saved_manual_jobs: dict[int, int] = {}
        self.sensor_preset = tk.StringVar(value="Estándar")
        self._render()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.apply(self._read(), reset=True)
        self.root.after(500, self.tick)

    def _render(self) -> None:
        """One functional Sensors console, three permanent logical areas.

        Left: canonical primary/secondary navigation (F07 sensor menu contract).
        Centre: sensor situation, real contacts and important notices.
        Right: selected contact dossier and context-dependent Core actions.
        No demo decorations, no fabricated measurements or LCARS graphics.
        """
        self.root.geometry("1380x860")
        self.root.minsize(1050, 680)
        self.current_view = "status"
        self.workspace_labels = {
            "status": "ESTADO DE SENSORES",
            "scans": "BARRIDOS",
            "search_localize": "BÚSQUEDA / LOCALIZACIÓN",
            "contacts": "CONTACTOS",
            "tracking": "SEGUIMIENTO",
            "sensor_readout": "LECTURA SENSORIAL",
            "interference": "INTERFERENCIAS / COMPENSACIÓN",
            "configuration": "CONFIGURACIÓN",
            "results": "RESULTADOS",
            "diagnostics": "DIAGNÓSTICO",
        }
        self.view_submenus = {
            "status": [("Resumen", "summary"), ("Actividad", "activity")],
            "scans": [("Todos los contactos", "all"), ("Planetas", "planets"),
                      ("Naves", "ships")],
            "search_localize": [("Todos", "all"), ("Naves", "ships"),
                                ("Planetas", "planets"), ("Satélites", "moons"),
                                ("Artificiales", "artificial")],
            "contacts": [("Todos", "all"), ("Sin identificar", "unidentified"),
                         ("Identificados", "identified"), ("Perdidos", "lost")],
            "tracking": [("Contactos activos", "active"), ("Contactos perdidos", "lost")],
            "sensor_readout": [("Todos", "all"), ("Planetas", "planets"),
                               ("Estrellas", "stars")],
            "interference": [("Entorno", "environment"), ("Sensores", "hardware")],
            "configuration": [("Perfiles", "profiles"), ("Diagnóstico", "hardware")],
            "results": [("Estudios actuales", "studies"), ("Ciencia planetaria", "planets")],
            "diagnostics": [("Estado del equipo", "hardware"), ("Incidencias", "activity")],
        }
        self.section_id = "summary"
        self.contact_subset = "all"
        self.map_positions: list[tuple[float, float, str]] = []
        self.alert_ids: list[str] = []
        self.alert_cursor = 0
        self.navigation_buttons = {}
        self.section_buttons = []

        header = ttk.Frame(self.root, padding=(12, 9, 12, 7))
        header.pack(fill="x")
        ttk.Label(header, text="USS ENTERPRISE-D · SENSORES",
                  font=("Segoe UI", 16, "bold")).pack(side="left")
        self.summary = ttk.Label(header, text="Conectando con CoreRPG...")
        self.summary.pack(side="left", padx=(22, 8))
        self.important = ttk.Label(header, text="")
        self.important.pack(side="right")

        # Operational incident: wide, high-contrast, actionable; hidden if nominal.
        # Navigation is a direct Core contact ID, not guessed from text or severity.
        self.alert_bar = tk.Frame(self.root, background="#ffe4a3",
                                  highlightbackground="#b45309", highlightthickness=3)
        self.alert_copy = tk.Frame(self.alert_bar, background="#ffe4a3")
        self.alert_copy.pack(side="left", fill="both", expand=True, padx=16, pady=11)
        self.alert_title = tk.Label(self.alert_copy, background="#ffe4a3",
                                    foreground="#7c2d12", anchor="w",
                                    font=("Segoe UI", 16, "bold"), text="")
        self.alert_title.pack(fill="x")
        self.alert_description = tk.Label(self.alert_copy, background="#ffe4a3",
                                          foreground="#451a03", anchor="w",
                                          font=("Segoe UI", 11), wraplength=940,
                                          justify="left", text="")
        self.alert_description.pack(fill="x", pady=(5, 0))
        self.alert_button = tk.Button(
            self.alert_bar, text="ABRIR CONTACTO",
            command=self.open_alert_contact,
            font=("Segoe UI", 11, "bold"), background="#92400e",
            foreground="#ffffff", activebackground="#78350f",
            activeforeground="#ffffff", padx=16, pady=10, relief="flat")
        self.alert_button.pack(side="right", padx=14, pady=12)

        columns = ttk.Panedwindow(self.root, orient="horizontal")
        columns.pack(fill="both", expand=True, padx=9, pady=(2, 5))
        self.workspace_panes = columns
        left = ttk.Frame(columns, width=200, padding=5)
        center = ttk.Frame(columns, width=700, padding=(6, 4))
        right = ttk.Frame(columns, width=400, padding=(6, 4))
        columns.add(left, weight=0)
        columns.add(center, weight=3)
        columns.add(right, weight=2)

        # LEFT — exactly the ten approved first-level Sensors menu entries.
        ttk.Label(left, text="MENÚ PRINCIPAL",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(3, 7))
        for view, title in self.workspace_labels.items():
            b = ttk.Button(left, text=title, command=lambda key=view: self.navigate(key))
            b.pack(fill="x", pady=2)
            self.navigation_buttons[view] = b
        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=10)
        ttk.Label(left, text="SUBMENÚ / SELECCIÓN",
                  font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.secondary_frame = ttk.Frame(left)
        self.secondary_frame.pack(fill="x", pady=6)
        ttk.Label(left, text="La vigilancia continúa\nal cambiar de pantalla.",
                  justify="left").pack(anchor="w", pady=(16, 3))

        # CENTRE — system-wide situational picture.
        self.workspace_title = ttk.Label(center, text="ESTADO DE SENSORES",
                                          font=("Segoe UI", 13, "bold"))
        self.workspace_title.pack(anchor="w", pady=(2, 4))
        overview_frame = ttk.LabelFrame(center, text="Situación general del sistema Aster", padding=6)
        overview_frame.pack(fill="x", pady=(0, 6))
        self.overview = tk.Text(overview_frame, height=4, wrap="word",
                                font=("Segoe UI", 10), state="disabled", relief="flat")
        self.overview.pack(fill="x")
        self.section_info = ttk.Label(center, text="", justify="left", wraplength=690)
        self.section_info.pack(fill="x", pady=(2, 5))

        map_box = ttk.LabelFrame(center, text="Proyección espacial 2D · posiciones observadas", padding=4)
        map_box.pack(fill="x", pady=(0, 6))
        self.map_canvas = tk.Canvas(map_box, height=170, background="#f8fafc",
                                    highlightthickness=0)
        self.map_canvas.pack(fill="x")
        self.map_canvas.bind("<Configure>", lambda _: self._draw_map())
        self.map_canvas.bind("<Button-1>", self._select_map_contact)

        contact_frame = ttk.LabelFrame(center, text="CONTACTOS OBSERVADOS · CoreRPG", padding=7)
        contact_frame.pack(fill="both", expand=True)
        filter_row = ttk.Frame(contact_frame)
        filter_row.pack(fill="x", pady=(0, 5))
        ttk.Label(filter_row, text="Filtro").pack(side="left")
        self.contact_filter = tk.StringVar(value="Todos")
        choices = ("Todos", "Planetas", "Naves", "Estrellas", "Satélites", "Artificiales")
        selector = ttk.Combobox(filter_row, textvariable=self.contact_filter,
                                 values=choices, state="readonly", width=15)
        selector.pack(side="left", padx=7)
        selector.bind("<<ComboboxSelected>>", lambda _: self._refresh_contacts(self.state))
        ttk.Label(filter_row, text="Selecciona una fila para abrir su expediente →"
                  ).pack(side="left", padx=(10, 0))
        colnames = ("ref", "tipo", "identificacion", "distancia", "confianza", "estado")
        table_area = ttk.Frame(contact_frame)
        table_area.pack(fill="both", expand=True)
        self.contacts_table = ttk.Treeview(table_area, columns=colnames,
                                            show="headings", height=12)
        headings = {"ref": "Contacto", "tipo": "Tipo", "identificacion": "Identificación",
                    "distancia": "Distancia", "confianza": "Confianza", "estado": "Estado"}
        widths = {"ref": 92, "tipo": 90, "identificacion": 220,
                  "distancia": 99, "confianza": 80, "estado": 78}
        for name in colnames:
            self.contacts_table.heading(name, text=headings[name])
            self.contacts_table.column(name, width=widths[name], minwidth=60, anchor="w")
        self.contacts_table.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(table_area, orient="vertical", command=self.contacts_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.contacts_table.configure(yscrollcommand=scrollbar.set)
        self.contacts_table.bind("<<TreeviewSelect>>", lambda _: (self.show_selected(), self._draw_map()))

        logframe = ttk.LabelFrame(center, text="Avisos operativos · solo lo relevante", padding=6)
        logframe.pack(fill="x", pady=(7, 0))
        self.log = tk.Text(logframe, height=4, wrap="word", state="disabled",
                           font=("Segoe UI", 9), relief="flat")
        self.log.pack(fill="x")

        # RIGHT — selected-object dossier; never replaced by generic backend logs.
        ttk.Label(right, text="EXPEDIENTE / ANÁLISIS ESPECIALIZADO",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(2, 6))
        detail_box = ttk.LabelFrame(right, text="Información del contacto seleccionado", padding=8)
        detail_box.pack(fill="both", expand=True)
        self.detail_text = tk.Text(detail_box, height=21, wrap="word", state="disabled",
                                   font=("Segoe UI", 10), relief="flat")
        self.detail_text.pack(side="left", fill="both", expand=True)
        detail_scroll = ttk.Scrollbar(detail_box, orient="vertical", command=self.detail_text.yview)
        detail_scroll.pack(side="right", fill="y")
        self.detail_text.configure(yscrollcommand=detail_scroll.set)

        actions = ttk.LabelFrame(right, text="Acciones sobre el contacto", padding=7)
        actions.pack(fill="x", pady=(6, 4))
        ttk.Button(actions, text="ENFOCAR / IDENTIFICAR",
                   command=lambda: self.contact_action("FOCUS")).pack(fill="x", pady=2)
        ttk.Button(actions, text="ESTUDIO DETALLADO (2 MIN)",
                   command=lambda: self.contact_action("SCAN")).pack(fill="x", pady=2)
        ttk.Button(actions, text="SEGUIMIENTO PRIORITARIO",
                   command=lambda: self.contact_action("PRIORITY")).pack(fill="x", pady=2)

        engineering = ttk.LabelFrame(right, text="Equipo de sensores", padding=7)
        engineering.pack(fill="x", pady=(4, 5))
        self.sensor_preset = tk.StringVar(value="Estándar")
        ttk.Combobox(engineering, textvariable=self.sensor_preset,
                     values=("Estándar", "Alta resolución", "Antinterferencias", "Máxima detección"),
                     state="readonly").pack(fill="x", pady=2)
        buttonrow = ttk.Frame(engineering)
        buttonrow.pack(fill="x", pady=3)
        ttk.Button(buttonrow, text="Aplicar perfil", command=self.apply_preset
                   ).pack(side="left")
        ttk.Button(buttonrow, text="Autodiagnóstico", command=self.diagnostic
                   ).pack(side="left", padx=8)

        # FOOTER — clock and scenario controls belong to the QA envelope,
        # not to Sensors: actual time management remains entirely in CoreRPG.
        footer = ttk.Frame(self.root, padding=(12, 6, 12, 9))
        footer.pack(fill="x")
        ttk.Label(footer, text="GUARDIA").pack(side="left")
        self.timelabel = ttk.Label(footer, text="00:00:00 / 08:00:00", width=26)
        self.timelabel.pack(side="left", padx=(5, 6))
        self.progress = ttk.Progressbar(footer, maximum=28800, value=0, length=135)
        self.progress.pack(side="left", padx=(0, 12))
        self.button_play = ttk.Button(footer, text="Iniciar", command=self.toggle)
        self.button_play.pack(side="left", padx=2)
        ttk.Button(footer, text="Reiniciar", command=self.restart).pack(side="left", padx=2)
        ttk.Button(footer, text="Guardar", command=lambda: self.checkpoint("SAVE")
                   ).pack(side="left", padx=2)
        ttk.Button(footer, text="Recuperar", command=lambda: self.checkpoint("LOAD")
                   ).pack(side="left", padx=2)
        ttk.Label(footer, text="Velocidad").pack(side="left", padx=(14, 2))
        ttk.Combobox(footer, textvariable=self.speed, values=("×15", "×30", "×60"),
                     state="readonly", width=5).pack(side="left")
        ttk.Label(footer, text="Incidencia").pack(side="left", padx=(14, 2))
        scenario = ttk.Combobox(footer, textvariable=self.mode, values=MODES,
                                state="readonly", width=20)
        scenario.pack(side="left")
        scenario.bind("<<ComboboxSelected>>", lambda _: self.restart())
        ttk.Button(footer, text="Exportar informe", command=self.export
                   ).pack(side="right")

        note = ttk.LabelFrame(self.root, text="Bitácora del oficial (opcional)", padding=4)
        note.pack(fill="x", padx=12, pady=(0, 5))
        self.notes = tk.Text(note, height=2, font=("Segoe UI", 9), wrap="word")
        self.notes.pack(fill="x")
        self.navigate("status")

    def _update_alert(self, state: dict) -> None:
        """Show actual actionable contacts from the native computer watch."""
        ids = [str(cid) for cid in state.get("attention_contacts", [])]
        if state.get("attention", 0) != len(ids):
            raise RuntimeError("El motor no ha proporcionado los contactos de la alerta.")
        prior = tuple(self.alert_ids)
        self.alert_ids = ids
        if not ids:
            if self.alert_bar.winfo_manager():
                self.alert_bar.pack_forget()
            return
        if prior != tuple(ids):
            self.alert_cursor = 0
        self.alert_cursor %= len(ids)
        item = self.contact_map.get(ids[self.alert_cursor])
        if item is not None:
            label = self.designations.get(item[0], "C-" + ids[self.alert_cursor][-6:])
            kind = TYPES.get(item[1], "señal desconocida")
            intro = f"{label} · {kind} · a {item[5] / 1000:.3f} UA · confianza {item[4] / 10:.1f}%."
        else:
            intro = "Contacto registrado por CoreRPG; ficha no disponible temporalmente."
        n = len(ids)
        self.alert_title.configure(text=(
            f"ATENCIÓN DEL OPERADOR · {n} CONTACTO{'S' if n != 1 else ''} POR EVALUAR"))
        self.alert_description.configure(text=(
            intro + "\nLa computadora ha intentado identificarlo automáticamente, "
            "pero su clase sigue sin confirmar. Requiere evaluación del oficial."
        ))
        self.alert_button.configure(
            text=("ABRIR CONTACTO" if n == 1 else
                  f"ABRIR CONTACTO {self.alert_cursor + 1}/{n}"))
        if not self.alert_bar.winfo_manager():
            self.alert_bar.pack(fill="x", padx=9, pady=(0, 7),
                                before=self.workspace_panes)

    def open_alert_contact(self) -> None:
        """One click: official flagged ID -> contact row -> observed dossier."""
        if not self.alert_ids:
            return
        contact_id = self.alert_ids[self.alert_cursor]
        if contact_id not in self.contact_map:
            messagebox.showwarning(
                "Sensores", "El contacto señalado ya no figura entre las observaciones.",
                parent=self.root)
            return
        self.navigate("contacts")
        self.contact_filter.set("Todos")
        self._refresh_contacts(self.state)
        if not self.contacts_table.exists(contact_id):
            messagebox.showwarning(
                "Sensores", "No se ha podido localizar el contacto en el listado actual.",
                parent=self.root)
            return
        self.contacts_table.selection_set(contact_id)
        self.contacts_table.focus(contact_id)
        self.contacts_table.see(contact_id)
        self.show_selected()
        self._draw_map()
        if len(self.alert_ids) > 1:
            self.alert_cursor = (self.alert_cursor + 1) % len(self.alert_ids)
            self._update_alert(self.state)

    def navigate(self, view: str) -> None:
        """Navigation never issues orders and never pauses the sensor watch."""
        if view not in self.workspace_labels:
            return
        self.current_view = view
        self.section_id = "summary"
        self.contact_subset = "all"
        self.contact_filter.set("Todos")
        for name, btn in self.navigation_buttons.items():
            btn.state(["disabled"] if name == view else ["!disabled"])
        for child in self.secondary_frame.winfo_children():
            child.destroy()
        self.section_buttons = []
        for label, section in self.view_submenus[view]:
            button = ttk.Button(self.secondary_frame, text=label,
                                command=lambda key=section: self.select_section(key))
            button.pack(fill="x", pady=2)
            self.section_buttons.append(button)
        self.workspace_title.configure(text=self.workspace_labels[view])
        presets = {"scans": "Todos", "search_localize": "Todos",
                   "contacts": "Todos", "sensor_readout": "Todos",
                   "results": "Todos"}
        if view in presets:
            self.contact_filter.set(presets[view])
        self._update_view_content()
        if self.state:
            self._refresh_contacts(self.state)

    def select_section(self, section: str) -> None:
        self.section_id = section
        self.contact_subset = section if section in ("unidentified", "identified", "lost", "active") else "all"
        filters = {"all": "Todos", "planets": "Planetas", "ships": "Naves",
                   "moons": "Satélites", "artificial": "Artificiales",
                   "stars": "Estrellas"}
        if section in filters:
            self.contact_filter.set(filters[section])
        self._update_view_content()
        if self.state:
            self._refresh_contacts(self.state)

    def _update_view_content(self) -> None:
        if not hasattr(self, "section_info"):
            return
        state = self.state
        details = {
            "status": "Estado del equipo, alcance, vigilancia y avisos de la sesión CoreRPG.",
            "scans": "Selecciona un contacto. Enfocar produce una observación; el estudio detallado reserva dos minutos reales de simulación.",
            "search_localize": "La lista muestra únicamente contactos observados. Los filtros no revelan objetos ocultos.",
            "contacts": "Consulta identidad, confianza, distancia y antecedentes del elemento seleccionado.",
            "tracking": "El seguimiento continúa en segundo plano; marca un contacto para darle prioridad.",
            "sensor_readout": "Abre un expediente para ver todas las lecturas autorizadas, incluidas las mediciones científicas.",
            "interference": "Las interferencias pueden reducir las detecciones. Consulta el estado y cambia la compensación del equipo.",
            "configuration": "Los perfiles cambian parámetros auténticos de la matriz de sensores.",
            "results": "Los estudios terminados y los informes científicos registrados están asociados a sus contactos.",
            "diagnostics": "El autodiagnóstico utiliza la matriz y la configuración reales de CoreRPG.",
        }
        if state:
            if self.current_view == "results":
                jobs = state.get("scans", [])
                active = sum(j[5] == 1 for j in jobs)
                done = sum(j[5] == 2 for j in jobs)
                details["results"] += f" Estudios: {active} activos, {done} terminados. Informes científicos: {len(state.get('science', []))}."
            elif self.current_view == "diagnostics":
                d = state.get("diagnostic", [0, 0, 0, 0])
                details["diagnostics"] += f" Capacidad {d[1] / 10:.0f}%, alimentación {d[2] / 10:.0f}%, integridad {d[3] / 10:.0f}%."
            elif self.current_view == "interference":
                details["interference"] += f" Índice EM observado: {state.get('interference_em', 0)}/550."
            elif self.current_view == "configuration":
                details["configuration"] += " Perfil actual (Core): " + str(state.get("config", [0, 0, 0, 0])[3]) + "."
        self.section_info.configure(text=details[self.current_view])
        if hasattr(self, "detail_text") and not self.contacts_table.selection():
            self.show_selected()

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
        line = f"{clock(tick)} · {message}"
        self.lines.append(line)
        self.log.configure(state="normal")
        self.log.insert("end", line + "\n")
        if int(self.log.index("end-1c").split(".")[0]) > 60:
            self.log.delete("1.0", "15.0")
        self.log.see("end")
        self.log.configure(state="disabled")

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
        rows = [self.contact_map[k] for k in self.contacts_table.get_children()
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
        selected = self.contacts_table.selection()
        selected_id = selected[0] if selected else None
        self.contact_map = {str(row[0]): row for row in state["contacts"]}
        stars = [c for c in state["contacts"] if c[1] == 12]
        planets = [c for c in state["contacts"] if c[1] == 13]
        if stars:
            star = stars[0]
            planets.sort(key=lambda c:
                         sum((c[8 + i] - star[8 + i]) ** 2 for i in range(3)))
            roman = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII",
                     "IX", "X", "XI", "XII")
            for i, planet in enumerate(planets):
                self.designations.setdefault(
                    planet[0], "Aster " + (roman[i] if i < len(roman) else str(i + 1))
                )
            self.designations.setdefault(star[0], "Aster (estrella central)")

        self.contacts_table.delete(*self.contacts_table.get_children())
        categories = {
            "Todos": None, "Planetas": {13}, "Naves": {1, 2},
            "Estrellas": {12}, "Satélites": {14},
            "Artificiales": {1, 2, 3, 5, 16},
        }
        allowed = categories.get(self.contact_filter.get())
        for row in state["contacts"]:
            if allowed is not None and row[1] not in allowed:
                continue
            if self.contact_subset == "unidentified" and row[1] == 1 and row[3] != 0:
                continue
            if self.contact_subset == "unidentified" and row[1] != 1:
                continue
            if self.contact_subset == "identified" and not (row[1] == 1 and row[3] != 0):
                continue
            if self.contact_subset == "lost" and row[2] != 2:
                continue
            if self.contact_subset == "active" and row[2] != 1:
                continue
            rid = str(row[0])
            short_ref = "C-" + rid[-6:]
            self.contacts_table.insert("", "end", iid=rid, values=(
                self.designations.get(row[0], short_ref), TYPES.get(row[1], "desconocido"),
                contact_identification(row), f"{row[5] / 1000:.3f} UA",
                f"{row[4] / 10:.1f}%", "Activo" if row[2] == 1 else "Perdido",
            ))
        if selected_id and selected_id in self.contact_map:
            self.contacts_table.selection_set(selected_id)
            self.contacts_table.see(selected_id)
        self.show_selected()
        self._draw_map()

    def _no_selection_dossier(self) -> str:
        """Show operational sensor data even before a contact is selected."""
        state = self.state
        if not state:
            return "Esperando el primer panorama de CoreRPG."
        d = state.get("diagnostic", [0, 0, 0, 0])
        c = state.get("config", [0, 0, 0, 0, 0])
        e = state.get("interference_em", 0)
        if self.current_view in ("status", "diagnostics", "configuration"):
            code = {1: "Nominal", 2: "Degradado", 3: "Fuera de servicio",
                    4: "Configuración limitada"}.get(d[0], "No determinado")
            return (
                "ESTADO DEL EQUIPO · lectura CoreRPG\n\n"
                f"Diagnóstico: {code}\n"
                f"Capacidad: {d[1] / 10:.1f}%\n"
                f"Potencia: {d[2] / 10:.1f}%\n"
                f"Integridad: {d[3] / 10:.1f}%\n"
                f"Sensibilidad: {c[0] / 10:.1f}%\n"
                f"Resolución: {c[1] / 10:.1f}%\n"
                f"Compensación: {c[2] / 10:.1f}%\n"
                f"Interferencia EM: {e}/550\n\n"
                "Selecciona un contacto del centro para consultar su expediente."
            )
        if self.current_view == "interference":
            return (
                "CONDICIONES DE OBSERVACIÓN\n\n"
                f"Interferencia electromagnética: {e}/550.\n"
                f"Compensación configurada: {c[2] / 10:.1f}%.\n"
                f"Matriz: {'fuera de servicio' if state.get('offline') else 'operativa'}.\n\n"
                "Puedes cambiar el perfil de sensores en esta misma columna. "
                "Un contacto perdido no implica necesariamente destrucción."
            )
        if self.current_view == "results":
            reports = state.get("science", [])
            jobs = state.get("scans", [])
            running = sum(j[5] == 1 for j in jobs)
            finished = sum(j[5] == 2 for j in jobs)
            return (
                "RESULTADOS AUTORIZADOS\n\n"
                f"Informes científicos CoreRPG: {len(reports)}\n"
                f"Estudios focales en curso: {running}\n"
                f"Estudios focales terminados: {finished}\n\n"
                "Selecciona un contacto para consultar sus resultados."
            )
        if self.current_view == "scans":
            return (
                "OPERACIONES DE SENSORES\n\n"
                "El barrido pasivo automático continúa sin intervención.\n\n"
                "ENFOCAR / IDENTIFICAR: lectura focal inmediata.\n"
                "ESTUDIO DETALLADO: operación temporizada de CoreRPG.\n"
                "SEGUIMIENTO PRIORITARIO: cambia el seguimiento de un contacto.\n\n"
                "Selecciona un contacto activo para ordenar una operación."
            )
        return (
            "INFORMACIÓN ESPECIALIZADA\n\n"
            f"Contactos observados: {state.get('active', 0)}\n"
            f"Contactos que requieren atención: {state.get('attention', 0)}\n\n"
            "Selecciona un contacto de la columna central. "
            "Los datos provienen exclusivamente de CoreRPG."
        )

    def show_selected(self) -> None:
        selection = self.contacts_table.selection()
        details = self._no_selection_dossier()
        if selection:
            contact = self.contact_map.get(selection[0])
            if contact:
                details = self._contact_description(contact)
                if contact[2] == 2:
                    cause = LOSS_CAUSES.get(contact[7], "causa no determinada")
                    details += f"\nCausa de pérdida registrada: {cause}."
                reports = [r for r in self.state.get("science", []) if r[0] == contact[0]]
                if reports:
                    report = reports[-1]
                    planet_class = PLANET_CLASSES.get(report[1], "desconocida")
                    bio = {0: "sin estudiar", 1: "sin señal detectada",
                           2: "posible", 3: "corroborada"}.get(report[10], "sin determinar")
                    details += (
                        f"\nInforme científico registrado en CoreRPG: clase {planet_class} "
                        f"({'provisional' if report[3] else 'confirmada'}), "
                        f"confianza {report[2] / 10:.1f}%; "
                        f"T {report[4]} K; presión {report[5]} mbar; "
                        f"agua superficial {report[6] / 10:.1f}%; "
                        f"N₂ {report[7] / 10:.1f}%; O₂ {report[8] / 10:.1f}%; "
                        f"CO₂ {report[9] / 10:.1f}%; biosignales: {bio}."
                    )
                    if report[8] < 100 or report[5] < 300:
                        details += "\nAtmósfera: NO se considera respirable sin asistencia "
                        details += "(oxígeno o presión medidos insuficientes)."
                    else:
                        details += "\nAtmósfera: respirabilidad NO confirmada. "
                        details += "Faltan análisis de posibles gases nocivos y condiciones locales."
                elif contact[1] in (12, 13):
                    details += "\nSin informe espectral/científico autorizado todavía. No se muestra ciencia privada del escenario."
                scans = [j for j in self.state.get("scans", []) if j[1] == contact[0]]
                for scan in scans[-3:]:
                    stage = {1: "en curso", 2: "terminado", 3: "fallido",
                             4: "cancelado"}.get(scan[5], "desconocido")
                    details += f"\nAnálisis especializado {stage} · "
                    details += f"iniciado {clock(scan[2])}, final previsto {clock(scan[3])}."
                    if scan[5] == 2:
                        details += " Resultado observado y registrado en CoreRPG."
                if contact[1] == 13:
                    details += "\nHabitabilidad: la clase M provisional NO confirma habitantes. "
                    details += "Civilización: sin informe verificable en este motor."
                if contact[1] == 12:
                    details += "\nClase espectral: sin análisis estelar publicado en CoreRPG."
                if contact[1] == 1 and contact[3] == 0:
                    details += "\nAcciones: análisis focalizado, seguimiento prioritario. La causa de la incertidumbre puede requerir nuevas mediciones."
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", "end")
        self.detail_text.insert("end", details)
        self.detail_text.configure(state="disabled")

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
                created = [j for j in state["scans"] if j[0] not in old_jobs and j[1] == contact[0]]
                for job in created:
                    self.manual_jobs[job[0]] = contact[0]
            self.apply(state)
            verb = {
                "FOCUS": "Observación focal inmediata registrada sobre ",
                "PRIORITY": "Seguimiento prioritario establecido sobre ",
                "SCAN": "Estudio detallado de dos minutos iniciado sobre ",
            }[action]
            self.append(state["tick"], verb + "C-" + selected[0][-6:] +
                        ". Consulta el expediente para ver su estado.")
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
        # The old tiny header label is NOT an operator alert.
        self.important.configure(text=(
            "Incidencia activa" if state["attention"] else "Sin incidencias activas"
        ))
        self._refresh_contacts(state)
        self._update_alert(state)
        self._update_view_content()
        current = [c for c in state["contacts"] if c[2] == 1]
        kinds = Counter(c[1] for c in current)
        classified = Counter(r[1] for r in state["science"] if r[1] != 0 and r[3] != 0)
        planets_covered = sum(1 for r in state["science"] if r[1] != 0)
        fleet = [c for c in current if c[1] == 1]
        naval = "; ".join(contact_identification(c) for c in fleet) or "sin detecciones"
        groups = ", ".join(
            f"{count} clase {PLANET_CLASSES.get(cls, '?')} (provisional)"
            for cls, count in sorted(classified.items()))
        briefing = (
            f"SISTEMA ASTER · BARRIDO AUTOMÁTICO ACTIVO\n"
            f"Observado: {kinds[12]} estrellas · {kinds[13]} planetas · "
            f"{kinds[14]} satélites naturales · {kinds[15]} nebulosas · "
            f"{kinds[16]} estaciones · {len(fleet)} naves.\n"
            f"Ciencia planetaria: {planets_covered}/{kinds[13]} planetas con "
            f"informes CoreRPG. {groups or 'Sin clasificación autorizada todavía.'}\n"
            f"Contactos navales observados: {naval}.\n"
            f"Estado: {'SENSORES NO DISPONIBLES' if state['offline'] else 'vigilancia autónoma continua'}"
            f" · perfil {state['config'][3]}"
            f" · compensación {state['config'][2] / 10:.0f}%"
            f" · diagnóstico {('nominal', 'degradado', 'sin servicio', 'revisar configuración')[state['diagnostic'][0] - 1] if 1 <= state['diagnostic'][0] <= 4 else 'no disponible'}"
            f"{' · interferencia EM activa' if state.get('interference_em', 0) else ''}."
        )
        self.overview.configure(state="normal")
        self.overview.delete("1.0", "end")
        self.overview.insert("end", briefing)
        self.overview.configure(state="disabled")
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
        if t >= 28800:
            self.playing = False
            self.button_play.configure(text="Guardia finalizada", state="disabled")
            self.append(t, "Guardia finalizada. Exporta el informe cuando quieras.")

    def tick(self) -> None:
        if self.playing and self.state.get("tick", 0) < 28800:
            try:
                sim_seconds=int(self.speed.get()[1:]) // 2
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
        self.button_play.configure(state="normal", text="Iniciar")
        self.lines.clear()
        self.record.clear()
        self.manual_jobs.clear()
        self.saved_manual_jobs.clear()
        self.designations = {}
        self.saved_lines = None
        self.saved_notes = ""
        self.state = {}
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
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
                self.record.clear()
                self.state = {}  # loading must not create a false state-transition alarm
                self.log.configure(state="normal")
                self.log.delete("1.0", "end")
                self.log.insert("end", "\n".join(self.lines) + ("\n" if self.lines else ""))
                self.log.configure(state="disabled")
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
