# المهمة 7: استبدل مادة الأرضية بالرخام

## التمثيل الدلالي

```yaml
intent:
  goal: "استبدل مادة الأرضية بالرخام"
  constraints: {}
  success_criteria:
    type: "user_approval"
  confidence: 0.0

task:
  intent:
    goal: "استبدل مادة الأرضية بالرخام"
    constraints: {}
    success_criteria:
      type: "user_approval"
    confidence: 0.0
  transformations:
    - type: "replace_material"
      parameters:
        target: "Floor"
        old_material: null
        new_material_type: "marble"
        new_material_name: "MarbleFloor"
  dry_run: false
```

## مراجعة الخبير
- **الدقة:**
- **الكفاية:**
- **ملاحظات:**
