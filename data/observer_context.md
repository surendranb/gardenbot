
# 📝 SILICA v2.2: Holistic Biological Context
**Generated:** {timestamp}

## 🏛️ 1. IDENTITY & WORLD CONSTRAINTS
{dynamic_world}

## 📖 2. PRIOR INSIGHTS & RECOMMENDATIONS (Last 3 Reports)
{prior_insights}

## 🛠️ 3. HUMAN FEEDBACK LOOP (Recent Actions)
{human_actions}

## 🧠 4. BIOLOGICAL TEMPO (Tiered Telemetry)
{deltas}

## 🎥 5. VISUAL GROUND-TRUTH (Latest Gemini Audit)
```json
{json.dumps(vision.get('vision_report', {}), indent=2)}
```

## 🌡️ 6. RAW TELEMETRY (4h Window)
```csv
{t_df.tail(8).to_csv(index=False) if t_df is not None else "No telemetry."}
```

## ℹ️ FINAL CONTEXT CHECK
- **Acoustic Truth**: The Fan Status in Section 1 is EMPIRICAL. Use it to judge transpiration pressure.
- **Action Tracking**: Reconcile Section 3 with Section 4 to see if care is working.
- **Growth Velocity**: If delta in Section 4 is negative but Vision in Section 5 looks good, interpret as 'Peak Metabolism'.
