from PIL import Image
import math

src = Image.open("logo.png").convert("RGBA")
W, H = 600, 400
CANVAS = (W, H)

def frame(img, angle=0, scale=1.0):
    rotated = img.rotate(-angle, resample=Image.BICUBIC, expand=True)
    new_w = int(rotated.width * scale)
    new_h = int(rotated.height * scale)
    scaled = rotated.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGBA", CANVAS, (255, 255, 255, 255))
    x = (W - scaled.width) // 2
    y = (H - scaled.height) // 2
    canvas.paste(scaled, (x, y), scaled)
    return canvas.convert("P", palette=Image.ADAPTIVE, colors=256)

frames = []
durations = []

# --- Spin: 0 → 360° over ~1s (30 frames, ~33ms each) ---
SPIN_FRAMES = 30
for i in range(SPIN_FRAMES):
    t = i / SPIN_FRAMES
    # ease-in-out
    ease = t * t * (3 - 2 * t)
    angle = ease * 360
    frames.append(frame(src, angle=angle, scale=1.0))
    durations.append(33)

# Brief pause between spin and pulse
frames.append(frame(src, angle=0, scale=1.0))
durations.append(80)

# --- Pulse: scale 1 → 1.3 → 1 over ~0.6s (18 frames) ---
PULSE_FRAMES = 18
for i in range(PULSE_FRAMES):
    t = i / (PULSE_FRAMES - 1)
    scale = 1.0 + 0.3 * math.sin(t * math.pi)
    frames.append(frame(src, angle=0, scale=scale))
    durations.append(33)

# Hold last frame briefly
frames.append(frame(src, angle=0, scale=1.0))
durations.append(300)

frames[0].save(
    "logo-animation.gif",
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=1,
    disposal=2,
)
print("Done — logo-animation.gif")
