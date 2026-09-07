# TeeAI 👕

منصة تصميم تيشيرت مخصص بالذكاء الاصطناعي — يصف المستخدم ذوقه، يولّد AI تصميمًا أصليًا على Mockup تيشيرت، ثم يرسل التصميم عبر صفحة الطلب. يضيف صاحب الموقع رابط منتج Zazzle من لوحة الإدارة، ويرى العميل زر الشراء في صفحة طلبه.

**صمّم تيشيرتك بالذكاء الاصطناعي — صف ذوقك فقط، ودع AI يتكفل بالباقي.**

---

## التقنيات

| طبقة | التقنية |
|---|---|
| Frontend | React 19 + TypeScript + Vite 8 + Tailwind CSS v4 + Lucide icons + React Router |
| Backend | Node.js (Express 5) + SQLite عبر `node:sqlite` (بدون اعتماديات أصلية) |
| AI | واجهة `aiService` قابلة للتبديل — مولد Mock محلي افتراضيًا، ويدعم OpenAI-compatible API |

## متطلبات التشغيل

- Node.js ≥ 22.9 (مُطوَّر واختبَر على Node 24)
- npm ≥ 10

## التشغيل

```bash
npm install          # تثبيت الاعتماديات
cp .env.example .env # إعداد المتغيرات (إن لم يوجد)
npm run dev          # API على :3001 + موقع على :5173 (مع Vite Proxy)
```

الإنتاج:

```bash
npm run build        # بناء الواجهة في dist/
npm start            # خادم واحد يقدم الـ API والموقع على :3001
```

> قاعدة البيانات تنشأ تلقائيًا في `data/teeai.db` وتُملأ بطلبات تجريبية عند أول تشغيل.
> `npm run dev` يحتاج تشغيلًا منفصلًا للـ API (يعمل تلقائيًا عبر `concurrently`).

## إعدادات `.env`

```env
PORT=3001                          # منفذ الخادم
ADMIN_USERNAME=admin               # دخول لوحة الإدارة
ADMIN_PASSWORD=teeai123            # ⚠️ غيّرها فورًا قبل النشر
SESSION_SECRET=change-me-...       # سر توقيع جلسة الإدارة
AI_PROVIDER=mock                   # mock (بدون مفتاح) | custom
AI_API_KEY=                        # مفتاح مزود AI الحقيقي
AI_API_URL=                        # نقاط نهاية الصور (OpenAI-compatible)
AI_MODEL=                          # نموذج الصور (مثال: gpt-image-1)
VITE_INSTAGRAM_URL=                # رابط متجرك على إنستغرام
VITE_CONTACT_EMAIL=                # بريد التواصل
```

> ⚠️ `.env` مستثنى من Git. لا تضع أي مفتاح حقيقي في الكود. القيم المعروضة سابقة افتراضية للتطوير فقط.

## ربط AI حقيقي (لاحقًا)

كل ما يتعلق بالـ AI معزول في **خادم** واحد:

- `server/ai.js` — يُرسل إلى الموفر الحقيقي ويعيد التصميم بصيغة SVG نصية.
- `src/services/aiService.ts` — الجهة الوحيدة التي تستهلكها الواجهة (`POST /api/generate`).

لتغيير المزود: اضبط `AI_PROVIDER=custom` واملأ `AI_API_KEY` / `AI_API_URL` / `AI_MODEL`. عندما يستجيب مزود جديد بتنسيق مختلف، عدّل ملف `server/ai.js` فقط — لن تتغير الواجهة أو بقية التطبيق. يستخدم المولد المحلي (Mock) prompt محسّنًا للطباعة يحظر الشعارات والشخصيات المحمية ويطلب خلفية شفافة.

## بنية المشروع

```
server/                # خادم Express (Node ESM)
  index.js             # المسارات: توليد، طلبات، إدارة، استضافة dist
  ai.js                # طبقة مزود AI (mock | custom)
  mockGenerator.js     # مولد التصاميم SVG المحلي (محدد البذرة، بدون حقوق محمية)
  db.js                # SQLite (node:sqlite) + سكيم الطلبات + بيانات تجريبية
  auth.js              # جلسة الإدارة (HMAC + httpOnly cookie)
  rateLimit.js         # حد طلبات لكل IP (توليد/طلبات/دخول)
src/
  pages/               # Landing, Designer, Submit, Success, OrderStatus, Admin, Login, Privacy, Terms
  components/          # TeeShirtMockup (Vector mockup مع ملمس قماش), Navbar, Footer, ...
  services/aiService.ts# العقدة الوحيدة للـ AI في الواجهة
  lib/                 # api client, draft (localStorage), downloadPng, trademark check, constants
```

## الصفحات

| المسار | الوظيفة |
|---|---|
| `/` | Landing: Hero + كيف يعمل + تصاميم تجريبية + قسم إنستغرام |
| `/designer` | المصمم: وصف، لون، ستايل، نص، توليد، إعادة توليد، تعديل، تحميل، حفظ |
| `/submit` | إدخال الاسم/البريد/إنستغرام وإرسال التصميم |
| `/success` | تأكيد الإرسال + رقم الطلب |
| `/order/:id` | صفحة الطلب: قيد المراجعة أو «تصميمك جاهز» + زر شراء Zazzle |
| `/admin` | لوحة الإدارة (محمية): إحصائيات، حالات، إضافة رابط المنتج |
| `/login` | دخول الإدارة |
| `/privacy` `/terms` | سياسة الخصوصية والشروط |

## سير العمل

```
Instagram Reel → /designer → /submit → Admin (إضافة رابط Zazzle + Ready) → /order/:id → زر شراء
```

أضف زر رابط المنتج في لوحة الإدارة، تُغيّر الحالة تلقائيًا إلى `ready`، ويظهر للعميل «🛒 شراء المنتج».

حالات الطلب: `new` → `processing` → `ready` → `completed`.

## الأمان

- لا مفاتيح في الواجهة؛ `AI_API_KEY` تُقرأ في الخادم فقط.
- جلسة إدارة بملف تعريف httpOnly + توقيع HMAC + منع الوصول غير المصرح (401 → صفحة الدخول).
- Rate limiting لتوليد التصاميم والطلبات وتسجيل الدخول.
- تحقق من كل المدخلات على الخادم (قوائم بيضاء للألوان/الستايلات/الأحجام، حدود أطوال، رابط صالح فقط).
- `helmet` لترويسات HTTP، وحد أقصى لحجم الطلب 200kb، ولا يوجد رفع ملفات.
- التوليد المحلي لا يرسم شعارات أو شخصيات محمية أبدًا + تنبيه للمستخدم عند ذكر أسماء تجارية في الوصف.

## اختبار

```bash
npm run lint         # oxlint
npm run build        # tsc -b + vite build (فحص الأنواع)
```

اختبارات المتصفح الآلية متوفرة (تتطلب تشغيل الخوادم):

```bash
node scripts/verify.cjs        # مسار كامل: توليد ← إرسال ← إدارة ← رابط ← شراء
node scripts/verify-deep.cjs   # فحوصات DOM: تموضع التصميم، الخطوط، التنزيل، الجوال
```

## ملاحظات MVP

- نظام الدفع خارج الموقع عمدًا (الطلب عبر Zazzle يدويًا).
- الصور المخزنة هي ملفات SVG شفافة جاهزة للطباعة — الموقع يعرض Mockup Vectorًا مرسومًا بالكامل.
- النقل لاحقًا إلى PostgreSQL/Supabase: كل الوصول إلى البيانات معزول في `server/db.js`.