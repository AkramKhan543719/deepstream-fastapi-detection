import json
from datetime import datetime
from pathlib import Path

from ultralytics import YOLO


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MODEL_NAME = "yolo11n.pt"

VIDEOS_DIR = Path("videos")
OUTPUT_DIR = Path("detection_json")

CONFIDENCE_THRESHOLD = 0.50

# Process one detection event every N frames.
# This prevents sending thousands of duplicate events.
FRAME_INTERVAL = 30


# ---------------------------------------------------------
# Load YOLO model
# ---------------------------------------------------------

print("Loading YOLO model...")

model = YOLO(MODEL_NAME)

print("YOLO model loaded successfully.")


# ---------------------------------------------------------
# Create output directory
# ---------------------------------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------------------------
# Process video
# ---------------------------------------------------------

def process_video(video_path: Path):

    print()
    print("=" * 60)
    print(f"Processing video: {video_path.name}")
    print("=" * 60)

    detections_output = []

    frame_count = 0

    results = model.predict(
        source=str(video_path),
        conf=CONFIDENCE_THRESHOLD,
        stream=True,
        verbose=False
    )

    for result in results:

        frame_count += 1

        # Only collect every Nth frame
        if frame_count % FRAME_INTERVAL != 0:
            continue

        timestamp = datetime.utcnow().isoformat()

        frame_detections = []

        if result.boxes is not None:

            for box in result.boxes:

                class_id = int(
                    box.cls[0].item()
                )

                confidence = float(
                    box.conf[0].item()
                )

                class_name = model.names[class_id]

                frame_detections.append(
                    {
                        "class_name": class_name,
                        "confidence": round(
                            confidence,
                            4
                        )
                    }
                )

        # Only save frames where objects were detected
        if frame_detections:

            event = {
                "video_name": video_path.name,
                "event_type": "object_detection",
                "timestamp": timestamp,
                "frame_number": frame_count,
                "detections": frame_detections
            }

            detections_output.append(event)

            print(
                f"Frame {frame_count}: "
                f"{len(frame_detections)} detection(s)"
            )

    # -----------------------------------------------------
    # Save JSON
    # -----------------------------------------------------

    output_file = (
        OUTPUT_DIR /
        f"{video_path.stem}_detections.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            detections_output,
            file,
            indent=4
        )

    print()
    print(f"Frames processed: {frame_count}")
    print(f"Detection events: {len(detections_output)}")
    print(f"JSON saved to: {output_file}")

    return detections_output


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    video_files = list(
        VIDEOS_DIR.glob("*.mp4")
    )

    if not video_files:

        print(
            "No .mp4 videos found in the videos folder."
        )

        print(
            "Please place your video files inside:"
        )

        print(
            VIDEOS_DIR.resolve()
        )

        raise SystemExit

    print(
        f"Found {len(video_files)} video(s)."
    )

    for video_file in video_files:

        process_video(video_file)

    print()
    print("=" * 60)
    print("ALL VIDEO PROCESSING COMPLETED")
    print("=" * 60)