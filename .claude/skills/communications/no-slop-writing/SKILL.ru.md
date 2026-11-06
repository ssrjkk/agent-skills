---
name: no-slop-writing
description: "Eliminates AI slop, corporate buzzwords, filler transitions, and ungrounded claims from technical documents, PRDs, and agent outputs. Use as a strict quality gate for high-density engineering and product writing."
category: communications
tags: [writing, editing, quality-gate, communications, documentation, anti-slop, prd]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: no-slop-writing
author: ssrjkk
---
# No-Slop High-Density Writing Gate (Защита текста от ИИ-воды и штампов)

> Жесткий фильтр против нейросетевой «воды», корпоративных штампов и голословных утверждений в документации и ТЗ.

## Быстрый старт
```python
# Ban-list scanner that flags high-entropy AI slop and corporate filler phrases
SLOP_PHRASES = (
    "delve into", "testament to", "tapestry of", "paradigm shift",
    "synergistic", "holistic approach", "unlock the full potential",
    "инновационные решения", "синергия", "комплексный подход", "вывести на новый уровень",
)

def scan_for_slop(text: str) -> list[str]:
    low = text.lower()
    return [phrase for phrase in SLOP_PHRASES if phrase in low]

assert scan_for_slop("Deploy CloudNativePG with 3 replicas across 3 AZs for RPO=0.") == []
```

```markdown
# High-Density Claim Rule: [Subject] + [Exact Action] + [Quantified Effect] + [Verification]
- Bad (Slop): "Our next-gen platform utilizes holistic caching to dramatically boost performance."
- Good (Dense): "Redis Cache-Aside with a 60s jittered TTL serves 85% of product reads in 1.8ms, reducing PostgreSQL CPU from 78% to 19%."
```

## Когда использовать
- Проверка технических спецификаций (RFC, ADR, PRD), статей и README на наличие «воды» и корпоративных лозунгов
- Повышение информационной плотности системных промптов и ответов ИИ-агентов без потери смысла
- Удаление пустых мета-анонсов («В данном разделе мы рассмотрим...», «Подводя итоги, можно с уверенностью сказать...»)
- Контроль того, чтобы каждое архитектурное решение сопровождалось компромиссами (trade-offs) и командой проверки

## Лучшие практики
- Начинайте каждый раздел сразу с решения или главного вывода в первом предложении без вводных абзацев.
- Запретите мета-анонсы («Ниже представлена таблица...», «В этом разделе мы разберем...») — заголовок уже говорит, о чем блок.
- Для каждого технического выбора указывайте его цену («Синхронная репликация дает RPO=0 ценой +1.5 мс к записи»).
- Заменяйте пустые заголовки-существительные («Масштабируемость», «Безопасность») на тезисные утверждения («Горизонтальное масштабирование до 30k RPS через KEDA»).
- Удаляйте трюизмы: если отрицание фразы звучит абсурдно («Мы делаем качественный продукт»), значит фраза не несет информации.
- Сжимайте объем без потери фактов: оставляйте схемы, контракты API, пороговые цифры и план отката.

## Зависимости
```bash
# Run automated slop and word-density checks
python3 --version
```

## Примеры
```python
# Calculate information density ratio (numbers, code tokens, and concrete identifiers per 100 words)
import re

def info_density_per_100_words(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    signals = re.findall(r"(`[^`]+`|\b\d+[a-zA-Z%/.:-]*\b|\b[A-Z]{2,}\b)", text)
    return round(len(signals) / len(words) * 100.0, 1)

assert info_density_per_100_words("Set `max_connections=200` on PostgreSQL 16 and route via PgBouncer on port 6432 for <2ms p99.") >= 25.0
```

```markdown
# Declarative Section Headers (Assertion-Evidence Pattern)
- Weak header: "Database Architecture"
- Strong header: "CloudNativePG 3-Node Quorum Guarantees RPO=0 and <10s Failover"
```

## Пошаговое руководство
1. Прогоните черновик через scan_for_slop() и удалите все найденные штампы вместе с вводными конструкциями.
2. Вырежьте вступительные разогревы и финальные блоки «В заключение / Подводя итоги», дублирующие уже сказанное.
3. Перепишите назывные заголовки в форму тезисных утверждений с главной цифрой или архитектурным выбором.
4. Измерьте плотность фактов через info_density_per_100_words() и замените общие слова на параметры конфигов и метрики.
5. Добавьте явный пункт «Компромиссы и сценарии отказа» для каждого предлагаемого технического решения.

## Валидация
1. Функция scan_for_slop() возвращает 0 совпадений по всему тексту документа
2. Плотность фактов info_density_per_100_words() составляет не менее 12.0 на технических разделах
3. Ни одна секция не начинается с пустых анонсов («Ниже приведена...», «В данном разделе...»)
4. Каждая рекомендация содержит как оцифрованную выгоду, так и цену решения (trade-off)

## Устранение неполадок
- Текст кажется слишком сухим для новичков — добавьте в начале короткий жизненный пример на 2 предложения вместо разбавления каждого абзаца водой.
- Нет точных исторических цифр — укажите целевой инженерный норматив или SLA («латентность p99 < 200 мс при 5000 RPS»).
- Модель продолжает вставлять клише — добавьте явный стоп-лист слов в системный промпт или файл AGENTS.md.
- Список буллетов дословно повторяет соседнюю таблицу — удалите дублирующий список и оставьте только компактную таблицу.
