

from PIL import Image
import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <gif-file> [output-file]")
    sys.exit(1)

fname = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) > 2 else "gif_output.h"

try:
    gif = Image.open(fname)
    frames = []
    delays = []

    # Читаем все кадры
    try:
        while True:
            frame = gif.copy().convert('RGB')
            if frame.width != 160 or frame.height != 128:
                print("Error: 160x128 frames required")
                sys.exit(2)

            frames.append(frame)
            delays.append(gif.info.get('duration', 100))
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    # Открываем файл для записи
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"// GIF: {len(frames)} frames, 160x128\n\n")

        # Записываем каждый кадр
        for frame_idx, frame in enumerate(frames):
            f.write(f"// Frame {frame_idx} (delay: {delays[frame_idx]}ms)\n")
            f.write(f"const uint16_t frame_{frame_idx}[128][160] = {{\n")

            for y in range(128):
                row = []
                for x in range(160):
                    r, g, b = frame.getpixel((x, y))
                    color565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | ((b & 0xF8) >> 3)
                    color565 = ((color565 & 0xFF00) >> 8) | ((color565 & 0xFF) << 8)
                    row.append(f"0x{color565:04X}")

                if y < 127:
                    f.write("  {" + ", ".join(row) + "},\n")
                else:
                    f.write("  {" + ", ".join(row) + "}\n")

            f.write("};\n\n")

        #массив указателей на кадры
        f.write("const uint16_t (* const gif_frames[])[160] = {\n")
        frame_ptrs = [f"frame_{i}" for i in range(len(frames))]
        f.write("  " + ", ".join(frame_ptrs) + "\n")
        f.write("};\n\n")

        f.write("const uint16_t gif_delays[] = {\n")
        f.write("  " + ", ".join(str(d) for d in delays) + "\n")
        f.write("};\n\n")

        f.write(f"#define GIF_FRAMES {len(frames)}\n")
        f.write("#define GIF_WIDTH 160\n")
        f.write("#define GIF_HEIGHT 128\n")

    print(f"Success! Converted {len(frames)} frames to {output_file}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
    print(f"#define GIF_FRAMES {len(frames)}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)