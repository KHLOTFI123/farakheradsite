from pathlib import Path

from PIL import Image

src = Path(
    r"C:\Users\khalil\.cursor\projects\c-farakheradsite\assets"
    r"\c__Users_khalil_AppData_Roaming_Cursor_User_workspaceStorage_"
    r"1bfbb5e39f0bfb9e32fafa47e72bd8f1_images_nf-a6db1924-9b56-4c71-bb79-fd801095ce10.png"
)
out_dir = Path(r"C:\farakheradsite\frontend\public")

img = Image.open(src).convert("RGBA")
pixels = img.load()
w, h = img.size

for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        brightness = (r + g + b) / 3.0
        maxc = max(r, g, b)
        minc = min(r, g, b)
        saturation = maxc - minc
        blue_dominance = b - max(r, g)

        # Soft white-background removal
        white_score = max(0.0, min(1.0, (brightness - 228) / 27.0)) * max(
            0.0, min(1.0, (45 - saturation) / 45.0)
        )
        near_white = max(0.0, min(1.0, (minc - 232) / 23.0))
        mask = max(white_score, near_white)
        new_a = a * (1.0 - mask)

        is_logo = saturation > 12 or blue_dominance > 4 or brightness < 240
        if is_logo and mask < 0.98:
            keep = min(255.0, saturation * 5 + (255 - brightness) * 0.8)
            if keep > new_a:
                new_a = keep

        if r > 250 and g > 250 and b > 250:
            new_a = 0

        if new_a < 1:
            pixels[x, y] = (0, 0, 0, 0)
            continue

        # Undo compositing over white on fringes
        alpha_n = new_a / 255.0
        if alpha_n < 0.999:
            fr = max(0, min(255, int(round((r - (1 - alpha_n) * 255) / max(alpha_n, 0.02)))))
            fg = max(0, min(255, int(round((g - (1 - alpha_n) * 255) / max(alpha_n, 0.02)))))
            fb = max(0, min(255, int(round((b - (1 - alpha_n) * 255) / max(alpha_n, 0.02)))))
            pixels[x, y] = (fr, fg, fb, int(round(new_a)))
        else:
            pixels[x, y] = (r, g, b, int(round(new_a)))

bbox = img.getbbox()
if bbox:
    pad = 10
    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(w, right + pad)
    bottom = min(h, bottom + pad)
    img = img.crop((left, top, right, bottom))

dest_png = out_dir / "logo.png"
img.save(dest_png, optimize=True)

fav = img.copy()
fav.thumbnail((64, 64), Image.Resampling.LANCZOS)
fav.save(out_dir / "favicon.png", optimize=True)

sample = img.load()
sw, sh = img.size
print("saved", dest_png, img.size)
print(
    "corner alpha",
    sample[0, 0][3],
    sample[sw - 1, 0][3],
    sample[0, sh - 1][3],
    sample[sw - 1, sh - 1][3],
)
