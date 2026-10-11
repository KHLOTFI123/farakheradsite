import urllib.error
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "frontend" / "public" / "services"
OUT.mkdir(parents=True, exist_ok=True)

FILES = {
    "devops.jpg": "https://images.unsplash.com/photo-1667372393119-3c3eacd640d7?auto=format&fit=crop&w=800&h=600&q=80",
    "mlops.jpg": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=800&h=600&q=80",
    "architecture.jpg": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=800&h=600&q=80",
    "cicd.jpg": "https://images.unsplash.com/photo-1618401471353-d51e5b0e2c0e?auto=format&fit=crop&w=800&h=600&q=80",
    "llm.jpg": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&h=600&q=80",
    "product.jpg": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=800&h=600&q=80",
    "training.jpg": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?auto=format&fit=crop&w=800&h=600&q=80",
}

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
}


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as res:
        return res.read()


for name, url in FILES.items():
    dest = OUT / name
    print(f"download {name}")
    try:
        dest.write_bytes(fetch(url))
    except urllib.error.HTTPError:
        dest.write_bytes(fetch(f"https://picsum.photos/seed/{name}/800/600"))
    print(f"  {dest.stat().st_size} bytes")
