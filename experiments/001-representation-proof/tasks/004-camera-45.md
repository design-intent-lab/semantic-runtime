# المهمة 4: ضع الكاميرا بزاوية 45 درجة على الهدف

## التمثيل الدلالي

```yaml
intent:
  goal: "ضع الكاميرا بزاوية 45 درجة على الهدف"
  constraints: {}
  success_criteria:
    type: "user_approval"
  confidence: 0.0

task:
  intent:
    goal: "ضع الكاميرا بزاوية 45 درجة على الهدف"
    constraints: {}
    success_criteria:
      type: "user_approval"
    confidence: 0.0
  transformations:
    - type: "set_camera"
      parameters:
        angle_horizontal: 45
        angle_vertical: 0
        distance_from_target: 5
        target_object: null
        camera_type: "PERSP"
  dry_run: false
```

## مراجعة الخبير
- **الدقة:** 4/5
- **الكفاية:** لا
- **ملاحظات:** الزاوية 45° محددة، لكن `target_object: null` — من غير الواضح ما هو الهدف الذي تدور حوله الكاميرا. المهمة تقول "على الهدف".
