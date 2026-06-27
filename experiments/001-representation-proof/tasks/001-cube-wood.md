# المهمة 1: أنشئ مكعباً وأضف له مادة خشبية

## التمثيل الدلالي

```yaml
intent:
  goal: "أنشئ مكعباً وأضف له مادة خشبية"
  constraints: {}
  success_criteria:
    type: "user_approval"
  confidence: 0.0

task:
  intent:
    goal: "أنشئ مكعباً وأضف له مادة خشبية"
    constraints: {}
    success_criteria:
      type: "user_approval"
    confidence: 0.0
  transformations:
    - type: "create_object"
      parameters:
        object_type: "cube"
        name: "Cube"
        location: [0, 0, 0]
        rotation: [0, 0, 0]
        scale: [1, 1, 1]
    - type: "assign_material"
      parameters:
        target_ref:
          type: "name"
          value: "Cube"
        material_type: "wood"
        material_name: "WoodMaterial"
  dry_run: false
```

## مراجعة الخبير
- **الدقة:** 5/5
- **الكفاية:** نعم
- **ملاحظات:** التمثيل واضح وكامل. `material_type: "wood"` عام لكنه مقبول في الإصدار 0.1.0.
