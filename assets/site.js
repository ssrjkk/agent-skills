/* Agent Skills — shared frontend (single source of truth).
   Hand-edited in assets/site.js; build_docs.py copies it to docs/site.js.
   Page-specific code (search, tabs, roadmaps data) stays inline per page. */
  var I18N = {
    en: {skip:"Skip to catalog",nav_catalog:"Catalog",nav_roadmaps:"Roadmaps",nav_stats:"Stats",nav_how:"How it works",soon:"soon",back_top:"Back to top",copied:"Copied: ",copy:"copy",view_source:"view source",models:"Models:",quality:"Quality",blocks:"Code blocks",sections:"Sections",lines:"Lines",ru_tr:"RU translation",back_catalog:"← Back to catalog",back_roadmaps:"← All roadmaps",open_map:"Open full map →",rel_skills:"Related skills →",browse_domain:"Browse {d} skills →",src:"Source:",copied_btn:"✓ copied",hero_sub:"Curated bilingual skills for <strong>Claude Code, OpenCode, Cursor, Windsurf</strong> and every Agent Skills–compatible agent. Pick a skill → copy the path → ship.",how_t:"How it works",how_s:"— 3 steps, 30 seconds",f1t:"Find",f1d:"Search by task, domain or tag. Every card shows quality, blocks and RU badge.",f2t:"Copy",f2d:"One click copies the skill path or install command for your agent.",f3t:"Ship",f3d:"Paste SKILL.md into context. Validate with agent-skills validate.",inst_t:"Install in one line",inst_s:"— pick your agent",cat_t:"Catalog",cat_s:"— {total} skills, {ru} with RU",search_ph:"Search skills by name, domain, or tag…",sort_domain:"Sort: domain",sort_name:"Sort: name",sort_score:"Sort: quality (high→low)",sort_aria:"Sort skills",empty_t:"No skills match your search.",count_t:"{v} of {t} shown",rm_t:"IT Roadmaps",rm_s:"soon everywhere",rm_d:"Step-by-step maps for every IT direction — frontend to AI. Statuses are live, content drops next.",rm_b:"Open roadmaps →",foot_t:"Created by ssrjkk · {n} skills · {d} domains",keys:"<kbd>/</kbd> search · <kbd>1–5</kbd> tabs · <kbd>t</kbd> theme · <kbd>Esc</kbd> clear",browse:"Browse skills ↓",st_skills:"Skills",st_ru:"Russian",st_dom:"Domains",st_q:"Quality",stat_t:"Distribution by domain",stat_s:"— click a pill to filter ↓",tab_install:"Install",rm_hd:"One tab per IT direction. Each map lives on its own page and in its own source file (<code>roadmaps/&lt;slug&gt;.json</code>) — drop your maps there and they plug straight in."},
    ru: {skip:"К каталогу",nav_catalog:"Каталог",nav_roadmaps:"Роадмапы",nav_stats:"Статистика",nav_how:"Как это работает",soon:"скоро",back_top:"Наверх",copied:"Скопировано: ",copy:"копировать",view_source:"исходник",models:"Модели:",quality:"Качество",blocks:"Блоки кода",sections:"Разделы",lines:"Строк",ru_tr:"Перевод RU",back_catalog:"← Назад в каталог",back_roadmaps:"← Все роадмапы",open_map:"Открыть мапу →",rel_skills:"Смежные скиллы →",browse_domain:"Скиллы: {d} →",src:"Источник:",copied_btn:"✓ готово",hero_sub:"Двуязычные скиллы для <strong>Claude Code, OpenCode, Cursor, Windsurf</strong> и любого совместимого агента. Найди скилл → скопируй путь → ship.",how_t:"Как это работает",how_s:"— 3 шага, 30 секунд",f1t:"Найди",f1d:"Ищи по задаче, домену или тегу. На каждой карточке — качество, блоки и бейдж RU.",f2t:"Скопируй",f2d:"Один клик копирует путь к скиллу или команду установки для твоего агента.",f3t:"Зашипь",f3d:"Вставь SKILL.md в контекст. Проверь через agent-skills validate.",inst_t:"Установка в одну строку",inst_s:"— выбери свой агент",cat_t:"Каталог",cat_s:"— {total} скиллов, {ru} с RU",search_ph:"Ищи скиллы по имени, домену или тегу…",sort_domain:"Сорт: домен",sort_name:"Сорт: имя",sort_score:"Сорт: качество (сначала лучшие)",sort_aria:"Сортировка скиллов",empty_t:"Ничего не найдено.",count_t:"Показано {v} из {t}",rm_t:"IT-роадмапы",rm_s:"скоро везде",rm_d:"Пошаговые мапы по каждому IT-направлению — от фронтенда до AI. Статусы живые, контент скоро.",rm_b:"Открыть роадмапы →",foot_t:"Автор ssrjkk · {n} скиллов · {d} доменов",keys:"<kbd>/</kbd> поиск · <kbd>1–5</kbd> вкладки · <kbd>t</kbd> тема · <kbd>Esc</kbd> очистить",browse:"Смотреть скиллы ↓",st_skills:"Скиллы",st_ru:"На русском",st_dom:"Домены",st_q:"Качество",stat_t:"По доменам",stat_s:"— клик по пилюле фильтрует ↓",tab_install:"Установка",rm_hd:"Одна вкладка — одно направление. Каждая мапа живёт на своей странице и в своём файле (<code>roadmaps/&lt;slug&gt;.json</code>) — клади свои мапы туда, и они подхватятся сами."}
  };
  function lang() { try { return localStorage.getItem('lang') || ((navigator.language || 'en').slice(0, 2) === 'ru' ? 'ru' : 'en'); } catch (e) { return 'en'; } }
  function setLang(l) {
    try { localStorage.setItem('lang', l); } catch (e) {}
    document.documentElement.setAttribute('lang', l);
    var D = I18N[l] || I18N.en;
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      var k = el.getAttribute('data-i18n');
      if (D[k] === undefined) return;
      var v = D[k];
      ['total', 'ru', 'n', 'd', 'v', 't'].forEach(function(key) {
        if (el.dataset[key] !== undefined) v = v.split('{' + key + '}').join(el.dataset[key]);
      });
      if (el.hasAttribute('data-i18n-html')) el.innerHTML = v; else el.textContent = v;
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(function(el) {
      var v = (D[el.getAttribute('data-i18n-ph')] || '');
      if (v) el.setAttribute('placeholder', v);
    });
    document.querySelectorAll('[data-i18n-aria]').forEach(function(el) {
      var v = D[el.getAttribute('data-i18n-aria')];
      if (v) el.setAttribute('aria-label', v);
    });
    document.querySelectorAll('.lang-toggle').forEach(function(b) { b.textContent = l === 'ru' ? 'EN' : 'РУ'; });
    if (typeof applyFilter === 'function') { try { applyFilter(); } catch (e) {} }
  }
  function toggleLang() { setLang(lang() === 'ru' ? 'en' : 'ru'); }
  function copyText(text) {
    function legacyCopy() {
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        var ok = document.execCommand('copy');
        document.body.removeChild(ta);
        return ok;
      } catch (e) { return false; }
    }
    function done(ok) {
      // on failure show the raw path so the user can copy it manually
      showToast(ok ? (I18N[lang()] || I18N.en).copied + text : text);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() { done(true); }, function() { done(legacyCopy()); });
    } else {
      done(legacyCopy());
    }
  }
  function copyBtn(btn, text) {
    copyText(text);
    if (btn.dataset.busy) return;
    btn.dataset.busy = '1';
    var old = btn.textContent;
    btn.classList.add('copied');
    btn.textContent = (I18N[lang()] || I18N.en).copied_btn;
    setTimeout(function() { btn.classList.remove('copied'); btn.textContent = old; delete btn.dataset.busy; }, 1400);
  }
  function showSkillLang(l) {
    try { localStorage.setItem('skill-lang', l); } catch (e) {}
    document.querySelectorAll('[data-slang-body]').forEach(function(d) {
      d.hidden = d.getAttribute('data-slang-body') !== l;
    });
    document.querySelectorAll('.lang-tab').forEach(function(b) {
      b.classList.toggle('active', b.getAttribute('data-slang') === l);
    });
  }
  function showToast(msg) {
    var t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._timer);
    t._timer = setTimeout(function() { t.classList.remove('show'); }, 1800);
  }
  function toggleTheme() {
    var b = document.body;
    var next = b.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    b.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); sessionStorage.removeItem('theme'); } catch (e) {}
    var btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = next === 'dark' ? '🌙' : '☀️';
  }
  (function() {
    var saved = null;
    try { saved = localStorage.getItem('theme') || sessionStorage.getItem('theme'); } catch (e) {}
    setLang(lang());
    if (saved === 'light') {
      document.body.setAttribute('data-theme', 'light');
      var btn = document.querySelector('.theme-toggle');
      if (btn) btn.textContent = '☀️';
    }
    var bt = document.getElementById('back-top');
    if (bt) window.addEventListener('scroll', function() { bt.hidden = window.scrollY < 600; }, {passive: true});
    var sl = null;
    try { sl = localStorage.getItem('skill-lang') || localStorage.getItem('lang'); } catch (e) {}
    if ((sl === 'ru' || sl === 'en') && document.querySelector('[data-slang-body="ru"]')) showSkillLang(sl);
  })();
  // animated counters
  document.querySelectorAll('.stat-num[data-count]').forEach(function(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var start = null;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / 900, 1);
      el.textContent = Math.round(target * p);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = target;
    }
    requestAnimationFrame(step);
  });
  // terminal typing animation
  (function() {
    var el = document.getElementById('term-body');
    if (!el) return;
    var lines = [
      '<span class="ln">~$</span> <span class="cmd">pip install agent-skills-library</span>',
      '<span class="ok">&#10003; library ready · EN+RU</span>',
      '<span class="ln">~$</span> <span class="cmd">agent-skills search diagram</span>',
      '<span class="ok">&#10003; diagram-as-code · design-spec-md</span>',
      '<span class="ln">~$</span> <span class="cmd">agent-skills validate</span><span class="cursor"></span>',
    ];
    var idx = 0;
    el.innerHTML = '';
    function typeLine() {
      if (idx >= lines.length) { setTimeout(reset, 4000); return; }
      var line = document.createElement('div');
      line.classList.add('term-line');
      line.innerHTML = lines[idx];
      el.appendChild(line);
      idx++;
      setTimeout(typeLine, 700);
    }
    function reset() {
      el.innerHTML = '';
      idx = 0;
      setTimeout(typeLine, 1500);
    }
    setTimeout(typeLine, 400);
  })();
  // roadmaps strip preview
  (function() {
    var strip = document.getElementById('rm-strip');
    if (!strip || typeof RM_TRACKS === 'undefined') return;
    RM_TRACKS.slice(0, 8).forEach(function(t, i) {
      var a = document.createElement('a');
      a.href = 'roadmaps.html#' + t.slug;
      a.className = 'rm-chip';
      a.style.animationDelay = (i * 60) + 'ms';
      a.innerHTML = '<span class="rm-ico">' + t.icon + '</span>' + t.name + '<span class="soon-pill">soon</span>';
      strip.appendChild(a);
    });
    var more = document.createElement('a');
    more.href = 'roadmaps.html';
    more.className = 'rm-chip more';
    more.textContent = '+' + (RM_TRACKS.length - 8) + ' more →';
    strip.appendChild(more);
  })();
  // tabs hash routing + initial filter (index only; guarded elsewhere)
  if (typeof showTab === 'function' && document.querySelector('.tab-btn')) {
    var h = (location.hash || '').replace('#', '');
    if (h === 'dashboard') h = 'stats';
    showTab(['catalog', 'stats', 'how', 'install', 'roadmaps'].indexOf(h) >= 0 ? h : 'catalog');
    if (typeof applyFilter === 'function') applyFilter();
  }
  // reveal on scroll + stagger cards
  (function() {
    var io = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting) {
          e.target.classList.add('in');
          if (e.target.classList.contains('cards')) {
            Array.prototype.forEach.call(e.target.children, function(c, i) {
              c.style.transitionDelay = Math.min(i * 30, 600) + 'ms';
              c.classList.add('in');
            });
          }
          io.unobserve(e.target);
        }
      });
    }, {threshold: 0.08});
    document.querySelectorAll('.reveal, .cards').forEach(function(el) { io.observe(el); });
    document.querySelectorAll('.card').forEach(function(c) { c.classList.add('reveal'); });
  })();
