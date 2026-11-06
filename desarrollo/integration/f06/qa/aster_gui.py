#!/usr/bin/env python3
"""Aster F06 acceptance panel: intentionally small, no LCARS and no fake data.

All status and contacts come via the native f06_aster_runner (same F04 Core
campaign). The Python window ONLY sends timing/control commands and translates
authorized numeric event codes to short messages. No hidden scientific truth.
"""
from __future__ import annotations

import argparse
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


def clock(tick: int) -> str:
    return f"{tick // 3600:02d}:{tick % 3600 // 60:02d}:{tick % 60:02d}"


class Panel:
    def __init__(self, root: tk.Tk, runner: Path) -> None:
        self.root = root
        root.title("Enterprise-D · Prueba F06 — Sistema Aster")
        root.geometry("780x660")
        root.minsize(660, 560)
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
        self._render()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.bind("<space>", lambda _: self.toggle())
        self.apply(self._read(), reset=True)
        self.root.after(500, self.tick)

    def _render(self) -> None:
        pad = {"padx": 15, "pady": 5}
        header = ttk.Frame(self.root, padding=15)
        header.pack(fill="x")
        ttk.Label(header, text="COMPUTADORA · SENSORES", font=("Segoe UI", 17, "bold")).pack(anchor="w")
        self.summary = ttk.Label(header, text="Preparando vigilancia automática…",
                                 font=("Segoe UI", 11))
        self.summary.pack(anchor="w", pady=(8, 0))
        self.important = ttk.Label(header, text="Sin avisos que requieran intervención.")
        self.important.pack(anchor="w", pady=(3, 0))

        controls = ttk.Frame(self.root, padding=(15, 4))
        controls.pack(fill="x")
        ttk.Label(controls, text="Prueba").pack(side="left")
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

        note = ttk.LabelFrame(self.root, text="Tus impresiones (opcional)", padding=10)
        note.pack(fill="x", **pad)
        self.notes = tk.Text(note, height=3, font=("Segoe UI", 10), wrap="word")
        self.notes.pack(fill="x")
        footer = ttk.Frame(self.root, padding=(15, 2))
        footer.pack(fill="x")
        ttk.Button(footer, text="Exportar informe", command=self.export).pack(side="right")
        ttk.Label(footer, text="Prueba técnica: datos reales de CoreRPG · Sin gráficos definitivos",
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

    def apply(self, state: dict, reset: bool = False) -> None:
        self.state = state
        self.record.append(state)
        t = state["tick"]
        self.progress["value"] = t
        self.timelabel.configure(text=f"Guardia: {clock(t)} / 08:00:00")
        if state["offline"]:
            status = "Sensores sin servicio. La computadora está supervisando la avería."
        elif state["running"]:
            status = f"Vigilancia automática · {state['running']} análisis en curso"
        else:
            status = "Vigilancia automática · Seguimiento de rutina"
        self.summary.configure(text=status)
        self.important.configure(text=(
            "Intervención recomendada: contacto por identificar."
            if state["attention"] else
            "Sin avisos que requieran intervención."
        ))
        if reset:
            self.append(t, "Comienza la guardia. La computadora controla los sensores.")
            if state["active"]:
                self.append(t, f"Detectados {state['active']} contactos; clasificación automática iniciada.")
        for kind, contact, when, category, klass in state["events"]:
            label = TYPES.get(category, "señal")
            if reset and kind == 1:
                continue  # group initial detections instead of 20 alarms
            if kind == 1 and category in (12, 13, 14, 15, 17):
                continue  # celestial background: routine monitoring, not an alarm
            if kind == 1:
                msg = f"Nuevo contacto: {label}. La computadora lo evalúa."
            elif kind == 2:
                msg = f"Se pierde el contacto con {label}; mantengo vigilancia."
            elif kind == 3:
                msg = f"Contacto recuperado ({label}). Vuelvo a analizarlo."
            elif kind == 4:
                msg = "Identificación completada; seguimiento automático."
            elif kind == 5:
                msg = f"Análisis automático iniciado: {label}."
            elif kind == 6:
                msg = f"Análisis de {label} terminado. Continúo la vigilancia."
            elif kind == 7:
                msg = f"Análisis de {label} interrumpido; comprobar sensores."
            else:
                continue
            self.append(when, msg)
        if t >= 28800:
            self.playing = False
            self.button_play.configure(text="Guardia finalizada", state="disabled")
            self.append(t, "Guardia finalizada. Puedes repetir o exportar el informe.")

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
