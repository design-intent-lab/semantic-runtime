# Semantic Representation Specification v0.2.0

مسودة للتجربة الثانية — إعادة إثبات التمثيل.

---

## 1. المقدمة

هذه الوثيقة تحدد بنية التمثيل الدلالي الموحد لوصف مهام التصميم ثلاثي الأبعاد. هذا الإصدار هو ترقية للإصدار v0.1.0 بناءً على الدرس المستفاد من التجربة الأولى: التمثيل الدلالي يحتاج آلية ربط بالمشهد، ليس فقط وصف التحولات.

### التغييرات عن v0.1.0

1. **إضافة `rotation`** إلى معاملات التحولات الهندسية.
2. **إضافة `target_ref`** — آلية مرنة للإشارة إلى الكائنات.
3. **إضافة `analyze_scene`** — تحول جديد لتحليل المشهد وترجمة الأوصاف الدلالية.

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

## 4. أنواع التحولات (Transformations)

### 4.1 التحولات الهندسية

كل تحول هندسي يمكن أن يحتوي على `target_ref` بدلاً من اسم الكائن الثابت، و`rotation` كمعامل إضافي.

```yaml
- type: "create_object"
  parameters:
    object_type: "cube"
    name: "MyCube"
    location: [0, 0, 0]
    rotation: [0, 0, 0]      # [X, Y, Z] بالراديان — جديد في v0.2.0
    scale: [1, 1, 1]

- type: "set_camera"
  parameters:
    target_ref:               # جديد في v0.2.0
      type: "description"     # "name" | "id" | "description"
      value: "الكائن الأمامي"
    angle_horizontal: 45
    angle_vertical: 0
    distance_from_target: 5
    camera_type: "PERSP"
```

### 4.2 آلية الإشارة إلى الكائنات (target_ref) — جديد

`target_ref` تحل محل حقول `target` الثابتة. وهي مرنة وتدعم ثلاثة أنماط:

```yaml
target_ref:
  type: "name"          # بالإسم الثابت
  value: "Floor"

target_ref:
  type: "id"            # بالمعرف الفريد
  value: "obj_0001"

target_ref:
  type: "description"   # بوصف دلالي — يُحلّ بواسطة analyze_scene
  value: "الكائن الأرضي"
```

إذا كان `target_ref` من نوع `description`، يجب أن يسبق التحول تحول `analyze_scene` ليحل الوصف إلى مرجع حقيقي.

### 4.3 تحليل المشهد (analyze_scene) — جديد

هذا التحول لا يغير المشهد، بل يحلله ويرجع مراجع للكائنات المطابقة لوصف معين:

```yaml
- type: "analyze_scene"
  parameters:
    description: "الكائن الأمامي"
    target_ref:
      type: "name"
      value: "obj_001"        # يُملأ ديناميكياً بعد التحليل
```

يكون `analyze_scene` مسؤولاً عن:
- تحليل المشهد الحالي (مواقع الكائنات بالنسبة للكاميرا، أنواعها، موادها).
- ترجمة الأوصاف الدلالية ("الأمامي"، "الأرضي"، "الأكبر") إلى مراجع.
- إرجاع `target_ref` قابل للاستخدام في التحولات التالية.

---

## 5. هيكل الرسالة للتنفيذ

```yaml
task:
  intent: {}
  transformations:
    - type: ""
      parameters: {}
    - type: ""
      parameters: {}
  dry_run: false
```

---

## 6. مستويات القياس

- **موضوعي (Objective):** أرقام صلبة.
- **تفسيري (Interpretive):** استنتاجات احتمالية تُعرض على المستخدم للموافقة أو الرفض.

---

## 7. قيود الإصدار 0.2.0

- المشاهد ثابتة فقط (Static scenes).
- لا يوجد رسوم متحركة، فيزياء، أو شخصيات.
- `analyze_scene` يتم تنفيذه بواسطة Gemini (كمستشار) في الإصدار الأولي.
- التقييم التفسيري استنتاجي ويحتاج موافقة المستخدم.
