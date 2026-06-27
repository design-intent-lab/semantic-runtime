# المهمة 8: اجعل الإضاءة ليلية (خافتة، زرقاء)

## التمثيل الدلالي

```yaml
intent:
  goal: "اجعل الإضاءة ليلية - خافتة وزرقاء"
  constraints: {}
  success_criteria:
    type: "user_approval"
  confidence: 0.0

task:
  intent:
    goal: "اجعل الإضاءة ليلية - خافتة وزرقاء"
    constraints: {}
    success_criteria:
      type: "user_approval"
    confidence: 0.0
  transformations:
    - type: "adjust_scene_temperature"
      parameters:
        method: "color_temperature"
        value: "cold"
        light_color_temp: 8000
    - type: "modify_world_settings"
      parameters:
        strength: 0.1
        color: [0.1, 0.1, 0.3]
    - type: "adjust_existing_lights"
      parameters:
        energy_multiplier: 0.3
  dry_run: false
```

## مراجعة الخبير
- **الدقة:**
- **الكفاية:**
- **ملاحظات:**
