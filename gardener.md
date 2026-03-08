# The Arid Architect: Cactus Management Protocol

## Patient Profile
- **Species:** Cactus (Unspecified Arid Variety)
- **Location:** Chennai, India (High Humidity, High Heat)
- **Environment:** Indoor, Window-side Table
- **Water Source:** 400ml Coffee Sipper (Submersible Pump)

## Monitoring Logic
- **Frequency:** 4 "Pulses" per day (08:00, 12:00, 16:00, 20:00)
- **Soil Threshold:** 
  - < 400: Drenched (Risk of Root Rot)
  - 400 - 750: Healthy/Moist
  - > 850: Bone Dry (Potential Watering Trigger)
- **Light Target:** Minimum 4 hours of "Bright" (< 450) per day.
- **Water Tank:** 
  - Tank Height: 15cm
  - Low Water Warning: > 12cm distance
  - Pump Cutoff: > 14cm distance (Protect Pump)

## Growth Tracking (Visual)
- **Daily Photo Requirement:** One photo in `/photos` per 24h.
- **Analysis:** Compare current photo to `baseline.jpg` to detect pixel-shift or volume increase.

## Decision Matrix
1. **Watering:** ONLY if (Soil > 850) AND (Days since last water > 10) AND (Water Tank > 100ml).
2. **Alerts:** 
   - "Tank Low": Please refill the sipper.
   - "Insufficient Light": Move closer to window.
   - "Photo Missing": Request user upload.
