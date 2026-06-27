# تصميم التجربة 002: إثبات الربط

## الهدف
إثبات أن التمثيل الدلالي (v0.2.0) يمكن ترجمته إلى كود Python ينفذ داخل Blender وينتج النتيجة المتوقعة.

## الفرضية
التمثيل الدلالي (v0.2.0) يمكن ترجمته آلياً إلى كود `bpy` ينفذ فعلياً في Blender وينتج مشهداً يطابق وصف المهمة الأصلية.

## معايير النجاح
- 3/3 مهام تُنفذ بنجاح في Blender.
- كل مهمة تنتج مشهداً يطابق المهمة الأصلية (مراجعة بصرية من الخبير).
- لا أخطاء تنفيذية (runtime errors) في كود bpy المولد.

## المهام المختارة

| # | المهمة | المستوى | التحدي |
|---|--------|---------|--------|
| 1 | مكعب + مادة خشبية | بسيط | التحولات الأساسية (create, assign) |
| 5 | طاولة خشبية بأرجل مخروطية | متوسط | كائنات متعددة، هندسة دورانية، مواد |
| 8 | إضاءة ليلية | معقد | تحليل مشهد، إضاءة متعددة، لون، تحقق |

## المنهجية
1. كتابة مترجم (translator) أولي (`src/translator.py`) يحول YAML → bpy Python.
2. لكل مهمة: تشغيل المترجم ← تنفيذ الكود في Blender ← تسجيل النتيجة.
3. مراجعة بصرية: هل المشهد الناتج يطابق المهمة الأصلية؟

## المترجم (Translator)

`src/translator.py` يدعم جميع أنواع التحولات الـ 12 في المواصفة v0.2.0:

| نوع التحول | دالة التوليد | الحالة |
|-----------|-------------|--------|
| create_object | gen_create_object | ✅ |
| assign_material | gen_assign_material | ✅ |
| replace_material | gen_replace_material | ✅ |
| add_light | gen_add_light | ✅ |
| set_camera | gen_set_camera | ✅ |
| enable_depth_of_field | gen_enable_depth_of_field | ✅ |
| analyze_scene | gen_analyze_scene | ✅ (هيوريستك) |
| modify_world_settings | gen_modify_world | ✅ |
| adjust_scene_temperature | gen_adjust_scene_temperature | ✅ |
| adjust_light_color | gen_adjust_light_color | ✅ |
| distribute_objects_randomly | gen_distribute_random | ✅ |
| configure_render | gen_configure_render | ✅ |

**الاستخدام:**
```
python src/translator.py experiments/001-representation-proof/tasks/001-cube-wood.md task1.py
blender --python task1.py
```

## المخاطر المعروفة
- `analyze_scene` يحتاج ذكاءً خارجياً (Gemini). في هذه التجربة، سنستخدم قواعد بسيطة (heuristics) بدلاً من AI.
- `target_ref` من نوع `description` يعتمد على الهيوريستك لحل الأوصاف.
- بيئة Blender قد تختلف (إصدارات، إضافات). سنستخدم Blender 4.x LTS.
