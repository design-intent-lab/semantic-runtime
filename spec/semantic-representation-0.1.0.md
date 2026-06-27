# Semantic Representation Specification v0.1.0

مسودة للتجربة الأولى — إثبات التمثيل.

---

## 1. المقدمة

هذه الوثيقة تحدد بنية التمثيل الدلالي الموحد لوصف مهام التصميم ثلاثي الأبعاد. الغرض من هذا الإصدار هو توفير أداة قابلة للاختبار في التجربة الأولى (إثبات التمثيل). الكمال ليس هدفاً هنا؛ القابلية للدحض هي الهدف.

---

## 2. الوحدة الأساسية: ثنائي التحول

المعرفة تُخزن على شكل وحدات ذرية:

```yaml
transformation_pair:
  id: "tp_001"
  context_before:
    scene_state: {}
    constraints: {}
  transformation:
    type: ""
    parameters: {}
  result_observed:
    scene_state: {}
    metrics: {}
  success: true
  confidence: 1.0
```

---

## 3. كائن النية

هذا هو المدخل الذي يقدمه المستخدم أو النظام:

```yaml
intent:
  goal: ""
  constraints:
    max_render_time: null
    max_memory: null
    engine: null
    poly_budget: null
  success_criteria:
    type: "user_approval"
  confidence: 0.0
```

---

## 4. مستويات القياس

- **موضوعي (Objective):** أرقام صلبة (مثل: المسافة، العدد، الوقت).
- **تفسيري (Interpretive):** استنتاجات احتمالية تُعرض على المستخدم للموافقة أو الرفض (مثل: "هذه الإضاءة دافئة").

---

## 5. هيكل الرسالة للتنفيذ

عند إرسال مهمة للتنفيذ، يستخدم هذا الهيكل:

```yaml
task:
  intent: {}
  transformations:
    - type: ""
      parameters: {}
  dry_run: false
```

- `intent`: كائن النية الأصلي.
- `transformations`: قائمة التحولات المطلوب تنفيذها بالتسلسل.
- `dry_run`: إذا `true`، يحاكي التنفيذ دون تغيير المشهد.

---

## 6. قيود الإصدار 0.1.0

- المشاهد ثابتة فقط (Static scenes).
- لا يوجد رسوم متحركة، فيزياء، أو شخصيات.
- التقييم التفسيري استنتاجي ويحتاج موافقة المستخدم.
