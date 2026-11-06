---
name: catalog-photo-mapper
description: "Audits, maps, and synchronizes e-commerce product catalog images across brands, series, and categories with zero cross-brand collisions, 1:1 studio aspect ratios, SQLite/CMS sync, and automated integrity tests. Use when fixing mismatched or broken product imagery."
category: frontend
tags: [ecommerce, frontend, catalog, images, sqlite, testing, automation]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: catalog-photo-mapper
author: ssrjkk
---
# E-Commerce Catalog Photo Mapper & Integrity Auditor (Маппинг фото каталога)

> Безошибочная привязка студийных фотографий 1:1 по брендам, сериям и категориям без коллизий и с автосинхронизацией SQLite и статики.

## Быстрый старт
```bash
# Run catalog photo collision tests and synchronize static pages + CMS exports
node --test tests/seo.test.js
node sync-pages.js
```

```javascript
// Assert zero cross-brand image collisions across all catalog items
const brandByImg = new Map();
for (const p of products) {
  const prev = brandByImg.get(p.image);
  if (prev && prev !== p.brand) {
    throw new Error(`Cross-brand collision on ${p.image}: ${prev} vs ${p.brand}`);
  }
  brandByImg.set(p.image, p.brand);
}
```

## Когда использовать
- В карточках товаров перепутаны фотографии брендов или категорий (например, у часов Suunto/Polar/Coros стоит фото Garmin)
- В папке каталога есть бракованные исходники (перевернутые приборы, вид задней крышки с датчиками, узкие обрезки ремешков)
- Необходима синхронизация путей картинок между products-data.js, папками uploads/ и public/uploads/, базой SQLite и выгрузками CMS
- Настройка переключения ракурсов главного фото (#product-main-img) в модальном окне карточки товара

## Лучшие практики
- Соблюдайте жесткий инвариант: товары разных брендов или несовместимых категорий никогда не должны ссылаться на один и тот же файл фото.
- Приводите все фотографии каталога к единому квадратному формату 1:1 (800x800 студийный анфас) для идеальной сетки карточек.
- Дублируйте каждое обновленное изображение одновременно в uploads/catalog/ и public/uploads/catalog/ для прохождения проверок сборки.
- Выполняйте автоматическую миграцию колонки products.image в SQLite из эталонного файла products-data.js при старте сервера.
- Разделяйте фотографии аксессуаров строго по типу (кабели зарядки, защитные сапфировые стекла 9H, силиконовые бамперы).
- Присваивайте id="product-main-img" главному изображению внутри #product-photo-pane для надежного переключения миниатюр галереи.

## Зависимости
```bash
# Verify image dimensions with Python Pillow and run Node catalog tests
python3 -c "from PIL import Image; print(Image.__name__)"
node --test
```

## Примеры
```python
# Audit catalog products for cross-brand or cross-category image collisions
from collections import defaultdict

def find_image_collisions(products: list[dict]) -> list[str]:
    brands_by_img: dict[str, set[str]] = defaultdict(set)
    cats_by_img: dict[str, set[str]] = defaultdict(set)
    for item in products:
        img = item["image"]
        brands_by_img[img].add(item["brand"])
        cats_by_img[img].add(item["category"])
    errors: list[str] = []
    for img, brands in brands_by_img.items():
        if len(brands) > 1:
            errors.append(f"{img}: shared across brands {sorted(brands)}")
    for img, cats in cats_by_img.items():
        if len(cats) > 1:
            errors.append(f"{img}: shared across categories {sorted(cats)}")
    return errors
```

```javascript
// Synchronize SQLite product images with canonical products-data.js on startup
const updateImgStmt = db.prepare('UPDATE products SET image = ? WHERE id = ?');
for (const item of canonicalProducts) {
  updateImgStmt.run(item.image, item.id);
}
```

## Пошаговое руководство
1. Проверьте все файлы в папке uploads/catalog/ на разрешение (800x800, 1:1) и отбракуйте узкие обрезки или фото задних крышек.
2. Запустите функцию find_image_collisions() по данным products-data.js для выявления всех межбрендовых и межкатегорийных пересечений.
3. Назначьте выделенные студийные рендеры каждому бренду и серии (велокомпьютеры Edge, эхолоты Striker и Deeper, навигаторы GPSMAP/Montana/eTrex, ошейники Alpha, часы по брендам и аксессуары).
4. Синхронно скопируйте обновленные файлы в обе директории: uploads/catalog/ и public/uploads/catalog/.
5. Убедитесь, что при старте server.js таблица products в SQLite автоматически обновляет поле image из products-data.js.
6. Запустите скрипт node sync-pages.js для обновления статической витрины GitHub Pages и архивов выгрузки CMS.
7. Проверьте переключение ракурсов #product-main-img в модалке и прогоните автотесты целостности каталога.

## Валидация
1. Функция find_image_collisions() возвращает пустой список (0 межбрендовых и 0 межкатегорийных коллизий)
2. Каждый файл из products-data.js физически присутствует в uploads/catalog/ и public/uploads/catalog/ в разрешении 800x800
3. Данные в таблице products базы SQLite на 100% совпадают с эталонным маппингом в products-data.js
4. Клик по миниатюрам ракурсов в карточке товара корректно обновляет главный рендер #product-main-img

## Устранение неполадок
- Падает тест на совпадение количества файлов в папках — копируйте каждое новое фото одновременно в uploads/catalog/ и public/uploads/catalog/.
- API продолжает отдавать старую картинку после правки products-data.js — обновите закэшированные строки в базе SQLite watchop.db.
- Ошибка при клике по миниатюре ракурса в карточке товара — проверьте наличие атрибута id="product-main-img" у главного тега <img>.
- Широкое фото кабеля или навигатора обрезается по краям — размещайте рендер на квадратном холсте 800x800 со стилем object-contain.
