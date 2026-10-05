#!/usr/bin/env python3
"""
Per-unit phasor diagram (back EMF, stator current, stator voltage) for a
PM synchronous machine in "constant power" operation with voltage and
current held at their limits, animated as electrical frequency is swept.

Model (resistance neglected, per-unit, E taken as the reference phasor):
    E      = E_rated  * w
    Xs     = Xs_rated * w
    Vs     = E + j*Xs*Is
    P      = Re{ E * conj(Is) } = E*|Is|*cos(phi)     (phi = angle of Is vs. E)

Current strategy:
  1. Use Is = Is_max in phase with E (phi = 0, max torque/amp) while |Vs| <= Vs_max.
  2. Once Vs would exceed Vs_max, rotate the current phasor (field weakening,
     phi > 0 -> Is lags... i.e. leads E in the diagram) with |Is| = Is_max so that
     |Vs| = Vs_max exactly.
  3. If even phi = 90 deg cannot hold |Vs| <= Vs_max (past the characteristic
     speed, w > Vs_max / (Xs_rated - E_rated) for E < Xs*Is), the current
     magnitude is reduced to Vs_max / (Xs - E).

Usage:
    python phasor_sweep.py --wmax 2.0
    python phasor_sweep.py --wmax 3.0 --E 0.5 --X 0.8 --out sweep.gif
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def solve_phasors(w, E_rated, X_rated, I_max, V_max):
    """Return (E, Is, Vs, jXsIs) complex phasors and power P at per-unit frequency w."""
    E_mag = E_rated * w
    X = X_rated * w

    # |Vs|^2 = E^2 + (X*I)^2 + 2*E*X*I*sin(phi)... with phi = angle of Is vs E:
    #   Vs = E + jX*I*(cos phi + j sin phi)  ->  |Vs|^2 = E^2 + (XI)^2 - 2*E*X*I*sin(phi)
    # Vs is FIXED at V_max: solve for phi with |Is| = I_max.
    I_mag = I_max
    s = (E_mag**2 + (X * I_mag) ** 2 - V_max**2) / (2 * E_mag * X * I_mag)
    if s > 1.0:
        # voltage can't be held at V_max with I_max: shrink current at phi = 90 deg
        phi = np.pi / 2
        I_mag = min(I_max, (V_max + E_mag) / X)
    elif s < -1.0:
        # too slow to reach V_max even with the current fully aligned (phi=-90 deg)
        phi = -np.pi / 2
    else:
        phi = np.arcsin(s)

    E = E_mag + 0j
    Is = I_mag * np.exp(1j * phi)
    jXI = 1j * X * Is
    Vs = E + jXI
    P = np.real(E * np.conj(Is))
    return E, Is, Vs, jXI, P


def arrow(ax, start, end, color, lw=2.5, ls="-", z=3):
    ax.annotate("", xy=(end.real, end.imag), xytext=(start.real, start.imag),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=18),
                zorder=z)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wmax", type=float, default=None,
                    help="upper limit of electrical frequency sweep (p.u.)")
    ap.add_argument("--wmin", type=float, default=1.0, help="start frequency (p.u.)")
    ap.add_argument("--E", type=float, default=0.5, help="rated back EMF (p.u.)")
    ap.add_argument("--X", type=float, default=0.8, help="rated synchronous reactance (p.u.)")
    ap.add_argument("--Imax", type=float, default=1.0, help="current limit (p.u.)")
    ap.add_argument("--Vmax", type=float, default=1.0, help="voltage limit (p.u.)")
    ap.add_argument("--frames", type=int, default=90, help="number of GIF frames")
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--out", default="phasor_sweep.gif")
    args = ap.parse_args()

    if args.wmax is None:
        args.wmax = float(input("Enter maximum electrical frequency (p.u., e.g. 1.5): "))
    if args.wmax <= args.wmin:
        raise SystemExit("wmax must be greater than wmin")

    ws = np.linspace(args.wmin, args.wmax, args.frames)
    # hold the last frame for a moment
    ws = np.concatenate([ws, np.full(args.fps, ws[-1])])

    # axis limits from the full sweep
    Vs_all = [solve_phasors(w, args.E, args.X, args.Imax, args.Vmax) for w in ws]
    pts = np.array([p for sol in Vs_all for p in (sol[0], sol[1], sol[2])])
    xlim = (min(-0.25, pts.real.min() - 0.15), max(1.25, pts.real.max() + 0.2))
    ylim = (min(-0.25, pts.imag.min() - 0.15), max(1.25, pts.imag.max() + 0.2))

    fig, ax = plt.subplots(figsize=(7, 7), dpi=100)
    th = np.linspace(0, 2 * np.pi, 400)

    def draw(i):
        ax.clear()
        w = ws[i]
        E, Is, Vs, jXI, P = Vs_all[i]
        delta = np.degrees(np.angle(Vs))        # angle of V leading E
        phi = np.degrees(np.angle(Is))          # angle of I leading E

        # limit circles
        ax.plot(args.Vmax * np.cos(th), args.Vmax * np.sin(th), ":", color="gray", lw=1)
        ax.plot(args.Imax * np.cos(th), args.Imax * np.sin(th), ":", color="firebrick", lw=1, alpha=0.5)
        ax.text(-0.02, args.Vmax + 0.02, "|V| = fixed", color="gray", fontsize=8, ha="right")

        # phasors
        arrow(ax, 0, Vs, "black", z=4)
        arrow(ax, 0, Is, "crimson", z=4)
        arrow(ax, 0, E, "blue", z=5)
        ax.plot([E.real, Vs.real], [E.imag, Vs.imag], "--", color="dimgray", lw=1.5, zorder=2)

        # labels
        ax.text(Vs.real, Vs.imag + 0.04, rf"$V_s={abs(Vs):.2f}$", color="black", ha="center", fontsize=11)
        ax.text(Is.real + 0.03, Is.imag + 0.03, rf"$I_s={abs(Is):.2f}$", color="crimson", fontsize=11)
        ax.text(E.real, -0.07, rf"$E={abs(E):.2f}$", color="blue", ha="center", va="top", fontsize=11)
        mid = (E + Vs) / 2
        ax.text(mid.real + 0.03, mid.imag, r"$jX_s I_s$", color="dimgray", fontsize=10)

        info = (rf"$\omega_e = {w:.2f}$" + "\n" +
                rf"$P = {P:.3f}$" + "\n" +
                rf"$\delta = {delta:.1f}^\circ$  (V lead E)" + "\n" +
                rf"$\phi_I = {phi:.1f}^\circ$  (I lead E)")
        ax.text(0.02, 0.98, info, transform=ax.transAxes, va="top", fontsize=11,
                bbox=dict(boxstyle="round", fc="white", ec="gray"))

        ax.axhline(0, color="k", lw=0.5)
        ax.axvline(0, color="k", lw=0.5)
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal")
        ax.set_xlabel("Re (p.u.)  -  E reference")
        ax.set_ylabel("Im (p.u.)")
        ax.set_title(f"Per-unit phasors: E_rated={args.E}, Xs_rated={args.X}, "
                     f"Is,max={args.Imax}, Vs,max={args.Vmax}", fontsize=10)

    anim = FuncAnimation(fig, draw, frames=len(ws), interval=1000 / args.fps)
    anim.save(args.out, writer=PillowWriter(fps=args.fps))
    print(f"Saved {args.out}")

    # Quick text summary of end points
    for w in (args.wmin, args.wmax):
        E, Is, Vs, jXI, P = solve_phasors(w, args.E, args.X, args.Imax, args.Vmax)
        print(f"w={w:.2f}: |E|={abs(E):.3f} |Is|={abs(Is):.3f} |Vs|={abs(Vs):.3f} "
              f"P={P:.3f} delta={np.degrees(np.angle(Vs)):.1f} deg")


if __name__ == "__main__":
    main()
