---
name: humanize-copy-pro
description: "Rewrites stiff, robotic AI-generated text into natural, rhythmic, concrete human copywriting in English and Russian. Use for technical articles, product pages, documentation, release notes, and developer communications."
category: communications
tags: [copywriting, writing, communications, editing, bilingual, documentation, content]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: humanize-copy-pro
author: ssrjkk
---
# Humanize Copy Pro (Живой технический и продуктовый текст)

> Превращение сухих нейросетевых канцеляризмов в живой, ритмичный и конкретный текст на русском и английском языках.

## Быстрый старт
```python
# Measure sentence-length variance (burstiness) to detect monotonous robotic cadence
import re
import statistics

def sentence_burstiness(text: str) -> float:
    sents = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    lengths = [len(s.split()) for s in sents if len(s.split()) > 1]
    return round(statistics.stdev(lengths), 2) if len(lengths) >= 2 else 0.0

assert sentence_burstiness("Ship the fix now. If the canary error rate stays under 0.5% for ten minutes, promote the rollout to all three availability zones.") > 5.0
```

```markdown
# Before (Robotic AI Cadence) -> After (Human Engineering Voice)
- Before: "In today's fast-paced digital landscape, organizations must leverage robust observability solutions to ensure seamless reliability."
- After: "When a deploy spikes 502 errors at 3 AM, you need one trace_id that links the nginx log to the slow Postgres lock."
```

## Когда использовать
- Редактура черновиков статей, README, лендингов и релиз-ноутов, которые звучат как шаблонный перевод нейросети
- Очистка русского текста от калек с английского («в современном быстро меняющемся мире», «давайте углубимся», «является ключевым»)
- Замена абстрактных обещаний на конкретные инженерные сценарии «было / стало» с цифрами и командами
- Настройка живого экспертного тона для разработчиков без рекламного пафоса и канцелярита

## Лучшие практики
- Чередуйте длину предложений: ставьте короткую ударную фразу на 4–6 слов рядом с развернутым техническим пояснением.
- Заменяйте отглагольные существительные («осуществление маршрутизации», «произведение валидации») на живые глаголы («маршрутизируйте», «проверьте»).
- Безжалостно удаляйте вступительные разогревы («В современном мире высоких технологий...», «Ни для кого не секрет, что...»).
- Избавляйтесь от пассивного залога и страдательных причастий («данные были обработаны сервером» -> «сервер обработал данные»).
- Подкрепляйте каждый тезис фактом: флагом утилиты, временем ответа в миллисекундах, кодом ошибки или путем к файлу.
- Переводите смысл и идиоматику, а не порядок слов английского предложения (избегайте конструкции «это позволяет вам делать X»).

## Зависимости
```bash
# Run burstiness and passive-voice checks with Python
python3 --version
```

## Примеры
```markdown
# Russian Calque Cleanup (Канцелярит -> Живой инженерный язык)
- Calque: "Данный инструмент обеспечивает осуществление мониторинга состояния подов в реальном времени."
- Clean: "Утилита следит за подами в реальном времени и шлет алерт, если контейнер уходит в OOMKilled."
```

```python
# Flag common Russian bureaucratic and AI-calque phrases
BAD_RU_PHRASES = (
    "в современном мире",
    "давайте погрузимся",
    "является ключевым",
    "осуществление",
    "в рамках данного",
)

def find_ru_calques(text: str) -> list[str]:
    low = text.lower()
    return [p for p in BAD_RU_PHRASES if p in low]
```

## Пошаговое руководство
1. Удалите первый абзац, если он состоит из общих рассуждений вместо немедленного перехода к сути проблемы или результату.
2. Проверьте ритмику текста через sentence_burstiness() и разбейте монотонные конструкции одинаковой длины.
3. Замените оценочные прилагательные («быстрый», «надежный», «удобный») на проверяемые факты («отклик 12 мс», «SLO 99.95%», «запуск в 1 команду»).
4. Прогоните русский текст через find_ru_calques() и замените канцелярит на прямое действие.
5. Вместо абстрактных примеров («представьте некоторую компанию») приводите реальные команды терминала и фрагменты конфигов.
6. Проверьте, что все заголовки написаны в обычном регистре предложения и несут конкретный смысл.

## Валидация
1. Индекс вариативности длины предложений sentence_burstiness() превышает 4.5 на абзацах из 3+ предложений
2. Проверка find_ru_calques() возвращает пустой список по всему русскому тексту
3. В тексте нет ни одного вступления со штампами «В современном мире...» или «Стоит отметить, что...»
4. Каждое техническое утверждение подкреплено цифрой, названием утилиты или примером кода

## Устранение неполадок
- Текст стал рубленым после сокращения фраз — чередуйте короткие тезисы со сложноподчиненными предложениями, объясняющими причину («потому что», «поэтому»).
- Русский перевод звучит неестественно при правильной грамматике — переформулируйте мысль так, как объяснили бы ее коллеге в код-ревью.
- После удаления прилагательных текст кажется сухим — добавьте конкретику результата («сократили сборку с 24 до 5 минут на 15 сервисах»).
- В каждом предложении стоит тире («X — это Y») — замените половину связок с тире на живые глаголы действия.
