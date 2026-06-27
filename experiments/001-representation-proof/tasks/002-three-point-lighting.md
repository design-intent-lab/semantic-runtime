# المهمة 2: أضف إضاءة استوديو ثلاثية النقاط

## التمثيل الدلالي

```yaml
intent:
  goal: "أضف إضاءة استوديو ثلاثية النقاط"
  constraints: {}
  success_criteria:
    type: "user_approval"
  confidence: 0.0

task:
  intent:
    goal: "أضف إضاءة استوديو ثلاثية النقاط"
    constraints: {}
    success_criteria:
      type: "user_approval"
    confidence: 0.0
  transformations:
    - type: "add_light"
      parameters:
        light_type: "AREA"
        name: "KeyLight"
        location: [5, -5, 5]
        energy: 1000
        color: [1, 1, 1]
    - type: "add_light"
      parameters:
        light_type: "AREA"
        name: "FillLight"
        location: [-4, -4, 3]
        energy: 500
        color: [1, 1, 1]
    - type: "add_light"
      parameters:
        light_type: "AREA"
        name: "RimLight"
        location: [0, 6, 4]
        energy: 800
        color: [1, 1, 1]
  dry_run: false
```

## مراجعة الخبير
- **الدقة:**
- **الكفاية:**
- **ملاحظات:**
