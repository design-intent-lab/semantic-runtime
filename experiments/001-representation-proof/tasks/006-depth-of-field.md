# المهمة 6: أضف عمق مجال للمشهد (التركيز على الكائن الأمامي)

## التمثيل الدلالي

```yaml
intent:
  goal: "أضف عمق مجال للمشهد، التركيز على الكائن الأمامي"
  constraints: {}
  success_criteria:
    type: "user_approval"
  confidence: 0.0

task:
  intent:
    goal: "أضف عمق مجال للمشهد، التركيز على الكائن الأمامي"
    constraints: {}
    success_criteria:
      type: "user_approval"
    confidence: 0.0
  transformations:
    - type: "enable_depth_of_field"
      parameters:
        camera_name: "Camera"
        focus_object: null
        focus_distance: 2.0
        aperture_fstop: 2.8
        aperture_blades: 6
  dry_run: false
```

## مراجعة الخبير
- **الدقة:**
- **الكفاية:**
- **ملاحظات:**
