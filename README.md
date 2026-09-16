# Ollama Agent Demo

یک مجموعه آموزشی ساده برای کار با **LangChain** و **LangGraph** همراه با مدل‌های سازگار با Ollama.

این پروژه قدم‌به‌قدم ویژگی‌های زیر را نشان می‌دهد:
- چت ساده با حافظه (Memory)
- اضافه کردن Tool
- پاسخ Streaming
- پاک کردن حافظه
- انجام Summarization به صورت خودکار
- ردیابی مصرف توکن

---

## پیش‌نیازها

- Python 3.12 یا بالاتر
- یک سرور Ollama (یا API سازگار با آن)
- فایل `.env` با مقادیر زیر:

```env
OLLAMA_API_KEY=your_api_key_here
OLLAMA_API_URL=http://localhost:11434/v1   # یا آدرس سرور شما
OLLAMA_API_MODEL=ollama3.2                 # یا هر مدل دیگری
```

---

## راه‌اندازی

### ۱. نصب وابستگی‌ها

از ریشه پروژه:

```bash
uv sync
```

این دستور محیط مجازی (`.venv`) را می‌سازد یا به‌روز می‌کند و پروژه را نصب می‌کند.

### ۲. تنظیم متغیرهای محیطی

یک فایل `.env` بسازید جایی که `load_dotenv()` بتواند آن را پیدا کند (معمولاً کنار اسکریپت‌ها داخل `src/` یا در ریشه پروژه). 

```env
OLLAMA_API_KEY=your-api-key-here
OLLAMA_API_URL=http://localhost:11434/v1
OLLAMA_API_MODEL=llama3.2
```

| متغیر | کاربرد |
|--------|--------|
| `OLLAMA_API_KEY` | کلید API برای endpoint سازگار با OpenAI (بعضی نصب‌های لوکال Ollama با مقدار ساختگی هم کار می‌کنند) |
| `OLLAMA_API_URL` | آدرس پایه همراه با مسیر `/v1` وقتی از حالت OpenAI-compatible استفاده می‌کنید |
| `OLLAMA_API_MODEL` | شناسه مدلی که به `init_chat_model` پاس داده می‌شود |

آدرس و مدل را مطابق سرویس‌دهنده خود تنظیم کنید.

### ۳. نحوه اجرا

**نسخه کامل:**

برنامه تعاملی اصلی در `src/__init__.py` قرار دارد (وقتی به صورت اسکریپت اجرا شود یک حلقه چت راه‌اندازی می‌کند):

```bash
uv run python src/__init__.py
```

**اسکریپت‌های آموزشی (قدم‌به‌قدم):**

این اسکریپت‌ها داخل `src/` هستند و مفاهیم را مرحله‌به‌مرحله آموزش می‌دهند:

| اسکریپت | آنچه نشان می‌دهد |
|---------|------------------|
| `1_app.py` | یک‌بار `agent.invoke` همراه با حافظه؛ پرسیدن نام، محاسبه، سپس یادآوری نام |
| `2_while.py` | حلقه تعاملی با invoke (بدون Tool و بدون Streaming) |
| `3_tool.py` | اضافه کردن `get_user_department_info` و استریم کردن تکه‌های پاسخ |
| `4_clear_memory.py` | همان Tool + Streaming به همراه دستور `clear` برای پاک کردن thread |

```bash
uv run python src/1_app.py
uv run python src/2_while.py
uv run python src/3_tool.py
uv run python src/4_clear_memory.py
```

### دستورات چت

در نسخه کامل (`src/__init__.py`):

| ورودی | عمل |
|--------|-----|
| متن عادی | ارسال به ایجنت (پاسخ به صورت استریم) |
| `exit` یا `quit` | خروج از حلقه چت |
| `clear` | حذف checkpoint مربوط به thread فعلی و ریست کردن شمارنده‌های توکن |
| `token` | نمایش مجموع توکن‌های input / output / total |

- اسکریپت‌های `2_while.py`، `3_tool.py` و `4_clear_memory.py` از `exit` / `quit` پشتیبانی می‌کنند.
- فقط `4_clear_memory.py` و نسخه کامل از `clear` پشتیبانی می‌کنند.
- فقط نسخه کامل از `token` پشتیبانی می‌کند.

---

## ویژگی‌های نسخه کامل

### ۱. Tool سفارشی
```python
@tool("get_user_department_info", description="LOOK FOR USER DEPATMENT")
def get_user_department_info(user_Id: str) -> str:
    ...
```
کاربر می‌تواند با دادن `user_Id` دپارتمان را بپرسد (`1` = HR، `2` = Marketing، `3` = Sale).

### ۲. حافظه کوتاه‌مدت
با استفاده از `InMemorySaver` و `thread_id` مکالمه در طول جلسه حفظ می‌شود.

### ۳. Streaming
پاسخ مدل به صورت زنده (token by token) چاپ می‌شود.

### ۴. Summarization خودکار
با `SummarizationMiddleware`:
- وقتی تعداد توکن‌ها از ۴۰۰۰ بیشتر شود، تاریخچه خلاصه می‌شود
- ۱۰ پیام اخیر نگه داشته می‌شود

### ۵. ردیابی توکن
با دستور `token` می‌توانید آمار مصرف توکن را ببینید.

---

## نکات مهم

- همه اسکریپت‌ها از یک `thread_id` ثابت (`"123"`) استفاده می‌کنند. برای مکالمه‌های جداگانه می‌توانید آن را تغییر دهید.
- `SummarizationMiddleware` فقط در نسخه کامل فعال است.
- برای استفاده در پروژه واقعی بهتر است `thread_id` را به صورت پویا (مثلاً بر اساس کاربر) تولید کنید.

---

## لایسنس

این پروژه فقط برای یادگیری ساخته شده است.
