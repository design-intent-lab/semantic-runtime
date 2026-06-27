# المهمة 5: أنشئ طاولة خشبية مستطيلة بأرجل مخروطية

## التمثيل الدلالي

```yaml
intent:
  goal: "أنشئ طاولة خشبية مستطيلة بأرجل مخروطية"
  constraints: {}
  success_criteria:
    type: "user_approval"
  confidence: 0.0

task:
  intent:
    goal: "أنشئ طاولة خشبية مستطيلة بأرجل مخروطية"
    constraints: {}
    success_criteria:
      type: "user_approval"
    confidence: 0.0
  transformations:
    - type: "create_object"
      parameters:
        object_type: "cube"
        name: "TableTop"
        location: [0, 0, 0.8]
        scale: [0.8, 0.5, 0.05]
    - type: "assign_material"
      parameters:
        target: "TableTop"
        material_type: "wood"
        material_name: "WoodTableTop"
    - type: "create_object"
      parameters:
        object_type: "cone"
        name: "Leg1"
        location: [-0.65, -0.35, 0.35]
        scale: [0.05, 0.05, 0.35]
    - type: "create_object"
      parameters:
        object_type: "cone"
        name: "Leg2"
        location: [0.65, -0.35, 0.35]
        scale: [0.05, 0.05, 0.35]
    - type: "create_object"
      parameters:
        object_type: "cone"
        name: "Leg3"
        location: [-0.65, 0.35, 0.35]
        scale: [0.05, 0.05, 0.35]
    - type: "create_object"
      parameters:
        object_type: "cone"
        name: "Leg4"
        location: [0.65, 0.35, 0.35]
        scale: [0.05, 0.05, 0.35]
    - type: "assign_material"
      parameters:
        target_mode: "all_selected"
        material_type: "wood"
        material_name: "WoodLegs"
  dry_run: false
```

## مراجعة الخبير
- **الدقة:**
- **الكفاية:**
- **ملاحظات:**
