---
name: catalog-photo-mapper
description: "Audits, maps, and synchronizes e-commerce product catalog images across brands, series, and categories with zero cross-brand collisions, 1:1 studio aspect ratios, SQLite/CMS sync, and automated integrity tests. Use when fixing mismatched or broken product imagery."
category: frontend
tags: [ecommerce, frontend, catalog, images, sqlite, testing, automation]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# E-Commerce Catalog Photo Mapper & Integrity Auditor

> Zero cross-brand image collisions, verified 1:1 studio product renders, automatic SQLite/static sync, and gallery integrity tests.

## Quick Start
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

## When to Use
- Product cards display mismatched brand photos (e.g., Suunto, Polar, or Coros items showing Garmin renders, or collars showing handhelds)
- Uploaded catalog images contain defective assets (upside-down devices, back-case sensors, narrow strap crops, or generic icons)
- Synchronizing updated image paths across products-data.js, uploads/catalog/, public/uploads/catalog/, SQLite (watchop.db), and CMS exports
- Ensuring product detail modal galleries (#product-main-img) switch angles and zoom cleanly on thumbnail selection

## Best Practices
- Enforce a strict invariant: two products from different brands or incompatible categories must never reference the same image filename.
- Standardize all catalog photos to square 1:1 studio front renders (800x800 WebP/PNG) so object-contain cards look uniform.
- Mirror every image update identically in both uploads/catalog/ and public/uploads/catalog/ so static build checks pass.
- Auto-migrate products.image in the local SQLite database from the canonical products-data.js map on server startup.
- Separate accessory imagery by exact product type (USB-C charging cables, 9H sapphire glass protectors, silicone cases).
- Assign id="product-main-img" to the primary image inside #product-photo-pane so thumbnail switching works deterministically.

## Dependencies
```bash
# Verify image dimensions with Python Pillow and run Node catalog tests
python3 -c "from PIL import Image; print(Image.__name__)"
node --test
```

## Examples
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

## Step-by-Step
1. Inspect all image files in uploads/catalog/ for aspect ratio (800x800 1:1) and flag non-square or back-facing images.
2. Run find_image_collisions() against products-data.js to list every cross-brand or cross-category collision.
3. Assign dedicated front-facing studio images for each brand and series (Edge bike computers, Striker/Deeper sonar, GPSMAP/Montana/eTrex, Alpha collars, multi-brand watches, cables, glass, cases).
4. Copy updated image files to both uploads/catalog/ and public/uploads/catalog/.
5. Ensure server.js synchronizes SQLite products.image rows from products-data.js at startup.
6. Run node sync-pages.js to propagate the updated catalog map to static GitHub Pages and CMS export bundles.
7. Verify #product-main-img angle switching and run the Catalog Photo Integrity test suite.

## Validation
1. find_image_collisions() returns an empty list (0 cross-brand and 0 cross-category collisions)
2. Every image path in products-data.js exists in both uploads/catalog/ and public/uploads/catalog/ with 800x800 dimensions
3. SQLite query SELECT id, image FROM products matches products-data.js 100%
4. Clicking gallery angle thumbnails updates #product-main-img transform and visual state cleanly

## Troubleshooting
- Static build test fails on file count mismatch — copy every new or replaced image into both uploads/catalog/ and public/uploads/catalog/.
- API still returns old image paths after editing products-data.js — watchop.db cached old rows; run the startup SQLite image sync.
- Gallery thumbnail click throws TypeError — ensure the main <img> inside #product-photo-pane has id="product-main-img".
- Wide handheld or cable photo looks clipped — place the product centered on an 800x800 canvas and use object-contain.
