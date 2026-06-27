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
        rotation: [0, 0, 0]
        scale: [0.8, 0.5, 0.05]
    - type: "assign_material"
      parameters:
        target_ref:
          type: "name"
          value: "TableTop"
        material_type: "wood"
        material_name: "WoodTableTop"
    - type: "create_object"
      parameters:
        object_type: "cone"
        name: "Leg1"
        location: [-0.65, -0.35, 0.35]
        rotation: [3.1416, 0, 0]
        scale: [0.05, 0.05, 0.35]
    - type: "create_object"
      parameters:
        object_type: "cone"
        name: "Leg2"
        location: [0.65, -0.35, 0.35]
        rotation: [3.1416, 0, 0]
        scale: [0.05, 0.05, 0.35]
    - type: "create_object"
      parameters:
        object_type: "cone"
        name: "Leg3"
        location: [-0.65, 0.35, 0.35]
        rotation: [3.1416, 0, 0]
        scale: [0.05, 0.05, 0.35]
    - type: "create_object"
      parameters:
        object_type: "cone"
        name: "Leg4"
        location: [0.65, 0.35, 0.35]
        rotation: [3.1416, 0, 0]
        scale: [0.05, 0.05, 0.35]
    - type: "assign_material"
      parameters:
        target_ref:
          type: "description"
          value: "جميع الأرجل"
        material_type: "wood"
        material_name: "WoodLegs"
  dry_run: false
```

## مراجعة الخبير
- **الدقة:** 4/5
- **الكفاية:** لا
- **ملاحظات:** الأرجل المخروطية (cone) تُنشأ في Blender برأسها للأعلى افتراضياً. التمثيل يفتقد `rotation` لقلب الأرجل 180°. الأبعاد والتوزيع صحيحان.
