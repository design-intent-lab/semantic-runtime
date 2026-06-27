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
    - type: "analyze_scene"
      parameters:
        analysis_type: "find_target"
        description: "جميع مصادر الإضاءة الحالية في المشهد"
        target_ref:
          type: "description"
          value: "جميع مصادر الإضاءة"
    - type: "modify_world_settings"
      parameters:
        strength: 0.05
        color: [0.05, 0.05, 0.2]
    - type: "adjust_light_color"
      parameters:
        target_ref:
          type: "description"
          value: "جميع مصادر الإضاءة"
        color: [0.3, 0.4, 0.8]
        energy_multiplier: 0.25
    - type: "analyze_scene"
      parameters:
        analysis_type: "check_lighting_result"
        description: "قياس إذا كانت الإضاءة الناتجة ليلية"
        target_ref:
          type: "description"
          value: "المشهد بأكمله"
  dry_run: false
```

## مراجعة الخبير
- **الدقة:** 4/5
- **الكفاية:** نعم
- **ملاحظات:** درجة حرارة 8000K مع تعتيم مناسب. `adjust_existing_lights` يفترض وجود إضاءات موجودة — صحيح في سياق "اجعل"، لكنه غير واضح لمشهد خالٍ.
