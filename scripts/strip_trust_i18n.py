from pathlib import Path

p = Path(r"C:\farakheradsite\frontend\src\i18n.tsx")
lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
out = [
    line
    for line in lines
    if '"footer.trust"' not in line and '"trust.alt"' not in line
]
p.write_text("".join(out), encoding="utf-8")
print("removed", len(lines) - len(out))
