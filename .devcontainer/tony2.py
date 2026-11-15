import cv2
import numpy as np

INPUT_VIDEO = "video.mp4"
WINDOW_NAME = "IRON MAN ASCII VIDEO"
ASCII_CHARS = "@%#*+=-:. "
TARGET_WIDTH = 120


def frame_to_ascii(frame, width=TARGET_WIDTH):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    new_h = max(1, int((h / w) * width * 0.45))
    resized = cv2.resize(gray, (width, new_h), interpolation=cv2.INTER_AREA)

    lines = []
    for row in resized:
        line = ""
        for px in row:
            index = int(px / 256 * len(ASCII_CHARS))
            index = min(len(ASCII_CHARS) - 1, max(0, index))
            line += ASCII_CHARS[index]
        lines.append(line)

    return lines


def draw_ascii(frame, scale=2):
    lines = frame_to_ascii(frame)
    canvas_h = len(lines) * 12
    canvas_w = max(len(line) for line in lines) * 8
    canvas = np.zeros((canvas_h + 25, canvas_w + 40, 3), dtype=np.uint8)

    title = "IRON MAN ASCII"
    cv2.putText(
        canvas,
        title,
        (18, 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 180, 255),
        1,
        cv2.LINE_AA,
    )

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            brightness = (ord(ch) / 255.0) if ch != " " else 0.0
            color = (
                int(255 * brightness),
                int(180 + 60 * brightness),
                int(80 + 150 * brightness),
            )
            cv2.putText(
                canvas,
                ch,
                (x * 8 + 20, y * 12 + 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1,
                cv2.LINE_AA,
            )

    return canvas


def main():
    cap = cv2.VideoCapture(INPUT_VIDEO)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {INPUT_VIDEO}")

    print("Opening Iron Man ASCII video...")
    print("Press ESC to exit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        ascii_frame = draw_ascii(frame)
        cv2.imshow(WINDOW_NAME, ascii_frame)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
