# المهمة 3: اجعل المشهد يبدو دافئاً

## التمثيل الدلالي

```yaml
intent:
  goal: "اجعل المشهد يبدو دافئاً"
  constraints: {}
  success_criteria:
    type: "user_approval"
  confidence: 0.0

task:
  intent:
    goal: "اجعل المشهد يبدو دافئاً"
    constraints: {}
    success_criteria:
      type: "user_approval"
    confidence: 0.0
  transformations:
    - type: "adjust_scene_temperature"
      parameters:
        method: "color_temperature"
        value: "warm"
        light_color_temp: 3500
        background_color: [1, 0.85, 0.6]
    - type: "modify_world_settings"
      parameters:
        strength: 0.3
        color: [1, 0.9, 0.7]
  dry_run: false
```

## مراجعة الخبير
- **الدقة:**
- **الكفاية:**
- **ملاحظات:**
