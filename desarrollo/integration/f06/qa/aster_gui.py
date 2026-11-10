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
        return "Nave sin clase confirmada"
    if category == 2:
        return "Lanzadera (tipo sin confirmar)"
    return TYPES.get(category, "señal desconocida")


def clock(tick: int) -> str:
    return f"{tick // 3600:02d}:{tick % 3600 // 60:02d}:{tick % 60:02d}"


class Panel:
    def __init__(self, root: tk.Tk, runner: Path) -> None:
        self.root = root
        root.title("USS Enterprise-D · Sensores · Sistema Aster")
        root.geometry("1100x960")
        root.minsize(820, 700)
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
        self._render()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.apply(self._read(), reset=True)
        self.root.after(500, self.tick)

    def _render(self) -> None:
        pad = {"padx": 15, "pady": 5}
        header = ttk.Frame(self.root, padding=15)
        header.pack(fill="x")
        ttk.Label(header, text="USS ENTERPRISE-D  /  DEPARTAMENTO DE SENSORES", font=("Segoe UI", 17, "bold")).pack(anchor="w")
        self.summary = ttk.Label(header, text="Preparando vigilancia automática…",
                                 font=("Segoe UI", 11))
        self.summary.pack(anchor="w", pady=(8, 0))
        self.important = ttk.Label(header, text="Sin avisos que requieran intervención.")
        self.important.pack(anchor="w", pady=(3, 0))

        overview_frame = ttk.LabelFrame(self.root, text="Informe panorámico de sistema", padding=8)
        overview_frame.pack(fill="x", padx=15, pady=(2, 6))
        self.overview = tk.Text(overview_frame, height=5, wrap="word", state="disabled",
                                font=("Segoe UI", 10), relief="flat")
        self.overview.pack(fill="both")

        controls = ttk.Frame(self.root, padding=(15, 4))
        controls.pack(fill="x")
        ttk.Label(controls, text="Incidencia de guardia").pack(side="left")
        selector = ttk.Combobox(controls, textvariable=self.mode, values=MODES,
                                state="readonly", width=23)
        selector.pack(side="left", padx=(7, 16))
        selector.bind("<<ComboboxSelected>>", lambda _: self.restart())
        ttk.Label(controls, text="Velocidad").pack(side="left")
        ttk.Combobox(controls, textvariable=self.speed, values=("×15", "×30", "×60"),
                     state="readonly", width=5).pack(side="left", padx=6)

        clockframe = ttk.Frame(self.root, padding=(15, 2))
        clockframe.pack(fill="x")
        self.timelabel = ttk.Label(clockframe, text="Guardia: 00:00 / 08:00", font=("Segoe UI", 11))
        self.timelabel.pack(anchor="w")
        self.progress = ttk.Progressbar(clockframe, maximum=28800, value=0)
        self.progress.pack(fill="x", pady=6)

        buttons = ttk.Frame(self.root, padding=(15, 4))
        buttons.pack(fill="x")
        self.button_play = ttk.Button(buttons, text="Iniciar", command=self.toggle)
        self.button_play.pack(side="left")
        ttk.Button(buttons, text="Reiniciar", command=self.restart).pack(side="left", padx=7)
        ttk.Button(buttons, text="Guardar punto", command=lambda: self.checkpoint("SAVE")).pack(side="left")
        ttk.Button(buttons, text="Recuperar punto", command=lambda: self.checkpoint("LOAD")).pack(side="left", padx=7)

        logframe = ttk.LabelFrame(self.root, text="Lo importante que comunica la computadora", padding=10)
        logframe.pack(fill="both", expand=True, **pad)
        self.log = tk.Text(logframe, height=11, wrap="word", state="disabled",
                           font=("Segoe UI", 10), relief="flat")
        self.log.pack(fill="both", expand=True)


        contact_frame = ttk.LabelFrame(self.root, text="Contactos reales observados por CoreRPG", padding=8)
        contact_frame.pack(fill="both", expand=True, **pad)
        columns = ("ref", "tipo", "identificacion", "distancia", "confianza", "estado")
        self.contacts_table = ttk.Treeview(contact_frame, columns=columns,
                                           show="headings", height=8)
        headings = {"ref": "Contacto", "tipo": "Tipo", "identificacion": "Identificación",
                    "distancia": "Distancia", "confianza": "Confianza", "estado": "Estado"}
        widths = {"ref": 88, "tipo": 112, "identificacion": 300,
                  "distancia": 102, "confianza": 95, "estado": 90}
        for key in columns:
            self.contacts_table.heading(key, text=headings[key])
            self.contacts_table.column(key, width=widths[key], anchor="w")
        self.contacts_table.pack(fill="both", expand=True)
        self.contacts_table.bind("<<TreeviewSelect>>", lambda _: self.show_selected())
        actions = ttk.Frame(contact_frame)
        actions.pack(fill="x", pady=(7, 3))
        ttk.Button(actions, text="Análisis focalizado", command=lambda: self.contact_action("FOCUS")).pack(side="left")
        ttk.Button(actions, text="Seguimiento prioritario",
                   command=lambda: self.contact_action("PRIORITY")).pack(side="left", padx=7)
        self.detail_text = tk.Text(contact_frame, height=5, wrap="word",
                                   state="disabled", font=("Segoe UI", 10))
        self.detail_text.pack(fill="x")

        note = ttk.LabelFrame(self.root, text="Bitácora del oficial (opcional)", padding=10)
        note.pack(fill="x", **pad)
        self.notes = tk.Text(note, height=3, font=("Segoe UI", 10), wrap="word")
        self.notes.pack(fill="x")
        footer = ttk.Frame(self.root, padding=(15, 2))
        footer.pack(fill="x")
        ttk.Button(footer, text="Exportar informe", command=self.export).pack(side="right")
        ttk.Label(footer, text="Fuente: observaciones y expedientes autorizados por CoreRPG",
                  foreground="#555555").pack(side="left")

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

    def _refresh_contacts(self, state: dict) -> None:
        selected = self.contacts_table.selection()
        selected_id = selected[0] if selected else None
        self.contact_map = {str(row[0]): row for row in state["contacts"]}
        self.designations = {}
        stars = [c for c in state["contacts"] if c[1] == 12 and c[2] == 1]
        planets = [c for c in state["contacts"] if c[1] == 13 and c[2] == 1]
        if stars:
            star = stars[0]
            planets.sort(key=lambda c:
                         sum((c[8 + i] - star[8 + i]) ** 2 for i in range(3)))
            roman = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII",
                     "IX", "X", "XI", "XII")
            for i, planet in enumerate(planets):
                self.designations[planet[0]] = (
                    "Aster " + (roman[i] if i < len(roman) else str(i + 1))
                )
            self.designations[star[0]] = "Aster (estrella central)"

        self.contacts_table.delete(*self.contacts_table.get_children())
        for row in state["contacts"]:
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

    def show_selected(self) -> None:
        selection = self.contacts_table.selection()
        details = "Selecciona un contacto para consultar su expediente observado y sus resultados científicos."
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
                elif contact[1] in (12, 13):
                    details += "\nSin informe espectral/científico autorizado todavía. No se muestra ciencia privada del escenario."
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
            state = self.command(f"{action} {contact[0]}")
            self.apply(state)
            self.append(state["tick"], (
                "Análisis focalizado ordenado sobre " if action == "FOCUS" else
                "Seguimiento prioritario ordenado sobre "
            ) + "C-" + selected[0][-6:] + ". Consulta los datos del contacto.")
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
        self.important.configure(text=(
            f"Atención: {state['attention']} contactos relevantes requieren evaluación."
            if state["attention"] else "Sin incidencias que requieran intervención."
        ))
        self._refresh_contacts(state)
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
        new_ids = {contact for kind, contact, *_ in state["events"] if kind == 1}
        for kind, contact_id, when, category, klass in state["events"]:
            contact = self.contact_map.get(str(contact_id))
            ident = contact_identification(contact) if contact else TYPES.get(category, "señal")
            short_ref = "C-" + str(contact_id)[-6:]
            if reset and kind == 1:
                continue
            if kind == 1 and category in (12, 13, 14, 15, 17):
                continue
            if kind == 1:
                msg = f"Nuevo contacto {short_ref}: {ident}. Seguimiento automático."
            elif kind == 2:
                cause = LOSS_CAUSES.get(contact[7], "causa no determinada") if contact else "causa no determinada"
                if cause == "causa no determinada" and state.get("interference_em", 0):
                    cause = "interferencias presentes; relación causal no confirmada"
                msg = f"Pérdida del contacto {short_ref} ({ident}). {cause}."
            elif kind == 3:
                msg = f"Contacto recuperado {short_ref}: {ident}."
            elif kind == 4:
                if contact_id in new_ids:
                    continue
                if not klass:
                    continue
                msg = f"Contacto {short_ref} identificado: {ident}."
            elif kind in (5, 6):
                continue  # backend: do not narrate ordinary automatic work
            elif kind == 7:
                msg = f"Análisis del contacto {short_ref} no disponible. Comprobar sensores."
            else:
                continue
            self.append(when, msg)
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
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        try:
            self.apply(self.command(f"RESTART {MODES.index(self.mode.get())}"), reset=True)
        except Exception as exc:
            messagebox.showerror("Prueba F06", str(exc), parent=self.root)

    def checkpoint(self, op: str) -> None:
        self.playing = False
        self.button_play.configure(text="Reanudar")
        try:
            self.apply(self.command(op))
            self.append(self.state["tick"],
                "Punto de guardado conservado en CoreRPG." if op == "SAVE" else
                "Guardia recuperada desde CoreRPG.")
        except Exception as exc:
            messagebox.showwarning("Prueba F06", str(exc), parent=self.root)

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
            *[f"Contacto {r[0]} · clase {PLANET_CLASSES.get(r[1], '?')} · confianza {r[2] / 10:.1f}% · provisional={bool(r[3])}"
              for r in self.state.get("science", [])], "",
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
