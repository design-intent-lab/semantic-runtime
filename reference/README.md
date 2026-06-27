# Semantic Runtime — Reference Executable

**شغّل هذا وسترى دورة Semantic Runtime الكاملة في أقل من 15 دقيقة.**

## المتطلبات

- Python 3.10+
- Blender 4.x (في PATH: `blender --version`)

## التشغيل

```bash
cd semantic-runtime/reference
./run.sh
```

ماذا سيحدث:
1. `runtime.py` يقرأ `example.intent.yaml` — مهمة "اجعل الإضاءة دافئة"
2. ينشئ مشهداً افتراضياً (3 إضاءات، كاميرا) إن لم يكن هناك مشهد
3. يحلل المشهد قبل التحول (BEFORE)
4. ينفذ التحولات: تدفئة الإضاءة، تخفيف العالم
5. يحلل المشهد بعد التحول (AFTER)
6. يحسب Semantic Diff
7. يحفظ `output/result.blend` و `output/result.png`
8. يكتب تقرير الأدلة `output/evidence.md`

## النتيجة المتوقعة

```
output/
├── result.blend          # مشهد Blender بعد التحول
├── result.png            # صورة م rendered
├── semantic_diff.json    # الفرق قبل/بعد (آلي)
└── evidence.md           # تقرير الأدلة (قابل للقراءة)
```

## ماذا لو فشل؟

| المشكلة | الحل |
|---------|------|
| `blender: not found` | ثبّت Blender 4.x من blender.org |
| `Python module not found` | `pip install pyyaml` أو سيستخدم المترجم المدمج |
| المخرج صورة سوداء | Cycles يحتاج وقتاً لتحميل الـ kernels — انتظر دقيقة |

## المبادئ

- **قابل للإعادة:** نفس المهمة على نفس المشهد تعطي نفس النتيجة
- **قابل للقياس:** Semantic Diff يقيس التغيير كمياً
- **قابل للدحض:** نعرف بالضبط ماذا تعلمنا من هذه التجربة

## الملفات

| الملف | الحجم | الوظيفة |
|-------|-------|---------|
| `runtime.py` | <200 سطر | محرك الدورة |
| `example.intent.yaml` | 7 أسطر | نية المستخدم |
| `run.sh` | 20 سطر | مشغّل الدورة |
| `output/` | — | النتائج (في .gitignore) |
