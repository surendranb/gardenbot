#!/usr/bin/env python3
import base64
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types

BASE_DIR = "/Users/surendran/.openclaw/workspace/gardenbot"
PHOTO_PATH = os.path.join(BASE_DIR, "media/latest.jpg")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
VISION_JSON_PATH = os.path.join(BASE_DIR, "data/vision_observation.json")
VISION_MD_PATH = os.path.join(BASE_DIR, "data/vision_observation.md")
DAILY_BENCHMARK_PATH = os.path.join(ARCHIVE_DIR, "daily_benchmark.jpg")
VISION_MODEL = os.environ.get("GEMINI_VISION_MODEL", "gemma-3-27b-it")
ENV_PATH = os.path.join(BASE_DIR, ".env")
TEMPORAL_COMPARE_COUNT = int(os.environ.get("VISION_COMPARE_COUNT", "4"))

REFERENCE = {
    "rabbit_height_cm": 5.0,
    "camera_distance_cm": 30.0,
    "black_pot_diameter_cm": 12.0,
    "yellow_pot_diameter_cm": 10.0,
}

def load_env_file(path):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), value)

def ensure_paths():
    os.makedirs(os.path.dirname(PHOTO_PATH), exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(VISION_JSON_PATH), exist_ok=True)

def capture_vision():
    """Captures an image, preferring cv2, falling back to imagesnap."""
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    day_dir = os.path.join(ARCHIVE_DIR, today_str)
    os.makedirs(day_dir, exist_ok=True)
    ts = now.strftime("%H%M%S")
    archive_path = os.path.join(day_dir, f"garden_{ts}.jpg")
    latest_existing = None
    if os.path.exists(PHOTO_PATH):
        latest_existing = PHOTO_PATH
    elif os.path.exists(day_dir):
        existing = sorted(
            [os.path.join(day_dir, f) for f in os.listdir(day_dir) if f.endswith(".jpg")]
        )
        if existing:
            latest_existing = existing[-1]

    try:
        import cv2
        print("Attempting camera capture using OpenCV (cv2)...")
        camera_index = 0
        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera index {camera_index}")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("Warming up sensor...")
        for i in range(3):
            ret, frame = cap.read()
            if ret:
                print(f"  Warmup frame {i+1} captured.")
            time.sleep(0.5)

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise RuntimeError("Failed to capture image from camera.")

        success = cv2.imwrite(archive_path, frame)
        if not success:
            raise RuntimeError(f"Failed to write image to {archive_path}")

        print(f"Image captured using CV2 and saved to {archive_path}")

    except Exception as e:
        print(f"CV2 failed or not available: {e}. Attempting imagesnap fallback...")
        try:
            subprocess.run(["imagesnap", "-q", archive_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"Image captured using imagesnap and saved to {archive_path}")
        except Exception as e2:
            if latest_existing and os.path.exists(latest_existing):
                subprocess.run(["cp", latest_existing, archive_path], check=True)
                print(f"Capture unavailable; reused existing image at {latest_existing} -> {archive_path}")
            else:
                print(f"Vision failed completely: {e2}")
                return {"error": str(e2)}

    if os.path.exists(archive_path):
        subprocess.run(["cp", archive_path, PHOTO_PATH], check=True)
        print(f"Updated latest photo: {PHOTO_PATH}")
        if now.hour == 6 and now.minute < 15:
            subprocess.run(["cp", archive_path, DAILY_BENCHMARK_PATH], check=True)
            print(f"Updated Daily Benchmark: {DAILY_BENCHMARK_PATH}")
        return {"photo_path": PHOTO_PATH, "archive_path": archive_path}
    return {"error": "Archive path does not exist after capture attempts."}

def archive_to_data_url(path):
    with open(path, "rb") as handle:
        encoded = base64.b64encode(handle.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"

def extract_json_payload(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        first_newline = cleaned.find("\n")
        if first_newline != -1:
            cleaned = cleaned[first_newline + 1 :]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = cleaned[start : end + 1]
        try:
            return json.loads(candidate)
        except Exception:
            pass
    raise ValueError("No valid JSON object found in model output")

def pick_temporal_stack(archive_path):
    now = datetime.now()
    today_dir = os.path.join(ARCHIVE_DIR, now.strftime("%Y-%m-%d"))
    files = []
    if os.path.exists(today_dir):
        files = sorted(
            [os.path.join(today_dir, f) for f in os.listdir(today_dir) if f.endswith(".jpg")]
        )
    anchor = next((p for p in files if Path(p).name.startswith("garden_06") or Path(p).name.startswith("garden_07")), None)
    previous = files[-2] if len(files) >= 2 else None
    current = archive_path
    compare = files[-TEMPORAL_COMPARE_COUNT:] if len(files) >= TEMPORAL_COMPARE_COUNT else files
    compare = [p for p in compare if p != current]
    if anchor and anchor not in compare:
        compare = [anchor] + compare
    if previous and previous not in compare:
        compare = compare + [previous]
    ordered_compare = []
    seen = set()
    for path in compare:
        if path and path not in seen and os.path.exists(path):
            ordered_compare.append(path)
            seen.add(path)
    return {"anchor": anchor, "previous": previous, "current": current, "compare_set": ordered_compare}

def build_prompt():
    return (
        "You are the Garden Vision Interpreter.\n"
        "Your job is to produce a stable visual baseline and a temporal narrative from the provided images.\n"
        "Return one strict JSON object and nothing else in the model response body.\n\n"
        "Reference frame:\n"
        "- White rabbit height: 5 cm\n"
        "- Camera distance: 30 cm\n"
        "- Black pot diameter: 12 cm\n"
        "- Yellow pot diameter: 10 cm\n"
        "- Black pots should be treated as centered plants.\n"
        "- Yellow pot should be treated as a spreading/trailing plant.\n\n"
        "Plant labels for this baseline:\n"
        "- p1 = String of Nickels\n"
        "- p2 = Mexican Mint\n"
        "- p3 = Pothos\n"
        "- p4 = Silver Guest\n\n"
        "Baseline truth rules:\n"
        "- The white rabbit is the scale anchor.\n"
        "- The rabbit is inside the Pothos pot unless the image clearly proves otherwise.\n"
        "- Use the rabbit, pot rims, and wiring as fixed landmarks.\n"
        "- Do not override the human baseline if a detail is ambiguous.\n\n"
        "Interpretation rules:\n"
        "- Use only visible evidence.\n"
        "- Do not infer final care decisions.\n"
        "- Mark each plant as healthy, stressed, or unknown.\n"
        "- Count visible leaves or leaf clusters when possible.\n"
        "- State whether each plant is centered, spreading, trailing, upright, or occluded.\n"
        "- Identify the rabbit, wire paths, pot rims, and any non-plant fixtures.\n"
        "- Identify obvious new growth, damaged leaves, droop, spread, or trailing.\n"
        "- Compare the current image against the prior 3 frames plus the anchor when available.\n"
        "- Explicitly describe changes in posture, spread, new growth, droop, occlusion, object placement, and leaf condition across the sequence.\n"
        "- Call out whether changes are stable trends or likely one-off noise.\n"
        "- If fixed landmarks conflict with the baseline, mark them uncertain rather than guessing.\n"
        "- Prefer confidence-aware factual descriptions over guesses.\n\n"
        "Output format:\n"
        "Return exactly these JSON keys and no extras:\n"
        "timestamp, model, baseline_reference, image_availability, frame_sequence, plants, temporal_changes, anomalies, narrative_report, confidence.\n"
        "Required field meanings:\n"
        "- image_availability: describe which frames were present.\n"
        "- frame_sequence: an array of objects in chronological order, each with label and path summary.\n"
        "- plants: object keyed by p1, p2, p3, p4. Each plant must include name, health, leaf_count, posture, growth, damage, droop, occlusion, notes.\n"
        "- temporal_changes: object keyed by p1, p2, p3, p4.\n"
        "- anomalies: array of strings.\n"
        "- narrative_report: one short paragraph about the latest image in the context of the previous 3 frames plus anchor.\n"
        "- confidence: one of low, medium, high.\n"
        "The JSON must be parseable on its own.\n"
        "Do not wrap the JSON in markdown fences.\n"
        "After the JSON, add one short markdown paragraph only if the model supports it.\n"
        "If any visual detail is uncertain, set it to 'uncertain' and explain why in anomalies or narrative_report."
    )

def analyze_vision(archive_path):
    load_env_file(ENV_PATH)
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is missing")

    client = genai.Client(api_key=api_key)
    stack = pick_temporal_stack(archive_path)
    prompt = build_prompt()

    content = [prompt]
    compare_paths = []
    if stack["compare_set"]:
        compare_paths.extend(stack["compare_set"])
    else:
        compare_paths.extend([stack["anchor"], stack["previous"], stack["current"]])

    # Send the comparison stack in chronological order, with the current capture last.
    seen = set()
    frame_labels = []
    for path in compare_paths:
        if path and os.path.exists(path):
            if path in seen:
                continue
            seen.add(path)
            label = "comparison"
            if path == stack.get("anchor"):
                label = "anchor"
            elif path == stack.get("previous"):
                label = "previous"
            elif path == stack.get("current"):
                label = "current"
            frame_labels.append({"label": label, "path": path})
            content.append(f"[{label.upper()}] {path}")
            with open(path, "rb") as handle:
                content.append(types.Part.from_bytes(data=handle.read(), mime_type="image/jpeg"))

    try:
        response = client.models.generate_content(
            model=VISION_MODEL,
            contents=content,
            config=types.GenerateContentConfig(
                temperature=0.2
                # top_p=0.8,
                # response_mime_type="application/json",
            ),
        )
        return response.text, {"stack": stack, "frame_sequence": frame_labels}, None
    except Exception as exc:
        fallback = {
            "timestamp": datetime.now().isoformat(),
            "model": VISION_MODEL,
            "status": "vision_unavailable",
            "error": str(exc),
            "baseline_report": {
                "p1": {"name": "String of Nickels", "health": "unknown"},
                "p2": {"name": "Mexican Mint", "health": "unknown"},
                "p3": {"name": "Pothos", "health": "unknown"},
                "p4": {"name": "Silver Guest", "health": "unknown"},
            },
            "narrative_report": "Vision model could not be reached, so no new visual interpretation was generated for this run.",
        }
        fallback["frame_sequence"] = frame_labels if "frame_labels" in locals() else []
        return json.dumps(fallback, indent=2), {"stack": stack, "frame_sequence": frame_labels if "frame_labels" in locals() else []}, str(exc)

def write_outputs(vision_text, stack_info, capture_result):
    now = datetime.now().isoformat()
    parsed = None
    try:
        parsed = extract_json_payload(vision_text)
    except Exception:
        parsed = {"raw_model_output": vision_text}

    payload = {
        "timestamp": now,
        "model": VISION_MODEL,
        "baseline_reference": REFERENCE,
        "image_availability": stack_info.get("stack", stack_info),
        "frame_sequence": stack_info.get("frame_sequence", []),
        "capture": capture_result,
        "vision_report": parsed,
        "raw_model_output": vision_text,
    }
    with open(VISION_JSON_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    with open(VISION_MD_PATH, "w", encoding="utf-8") as handle:
        handle.write("# Vision Observation\n\n")
        handle.write(f"- Generated: {now}\n")
        handle.write(f"- Model: {VISION_MODEL}\n")
        handle.write(f"- Current: {stack_info.get('stack', {}).get('current')}\n")
        handle.write(f"- Previous: {stack_info.get('stack', {}).get('previous')}\n")
        handle.write(f"- Anchor: {stack_info.get('stack', {}).get('anchor')}\n\n")
        if parsed and isinstance(parsed, dict):
            handle.write("## Parsed Baseline\n\n")
            summary = parsed.get("narrative_report") or parsed.get("status") or "No narrative returned."
            handle.write(f"{summary}\n")
        else:
            handle.write("## Raw Output\n\n")
            handle.write(vision_text.strip())
            handle.write("\n")
    print(f"Vision observation saved to {VISION_JSON_PATH} and {VISION_MD_PATH}")

def main():
    ensure_paths()
    capture_result = capture_vision()
    if "error" in capture_result:
        print(json.dumps(capture_result, indent=2))
        return
    vision_text, stack, error = analyze_vision(capture_result["archive_path"])
    write_outputs(vision_text, stack, capture_result)
    if error:
        print(json.dumps({"warning": "vision_model_unavailable", "error": error}, indent=2))
        return
    print(json.dumps(capture_result, indent=2))

if __name__ == "__main__":
    main()
