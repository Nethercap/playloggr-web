"""Genera la calculadora publica "¿En que año terminas tu backlog?" en los 3
idiomas, desde una sola plantilla:

    calculadora/index.html            (es)
    en/backlog-calculator/index.html  (en)
    pt/calculadora/index.html         (pt)

Uso:  python tools/calculadora/build.py   (desde la raiz del repo web)

Los datos salen de GET /api/v1/public/backlog-calculator (backend). Todo lo
que viene de Steam se inserta con textContent, nunca como HTML.
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = "https://playloggr.com"
PATHS = {"es": "/calculadora/", "en": "/en/backlog-calculator/", "pt": "/pt/calculadora/"}
HOME = {"es": "/", "en": "/en/", "pt": "/pt/"}
OG = {"es": "/assets/og-cover.jpg?v=2", "en": "/assets/og-cover-en.jpg?v=2", "pt": "/assets/og-cover-pt.jpg?v=2"}

L = {
    "es": {
        "title": "¿En qué año terminás tu backlog de Steam? · Calculadora gratis | Playloggr",
        "desc": "Pegá tu perfil de Steam y descubrí cuántos juegos tenés sin empezar, cuántas horas son y en qué año los terminarías. Gratis y sin cuenta.",
        "h1": "¿En qué año terminás tu backlog?",
        "sub": "Pegá tu perfil de Steam y te decimos cuántos juegos tenés sin empezar y cuánto te falta. Gratis, sin cuenta.",
        "label": "Tu perfil de Steam",
        "ph": "Link de tu perfil, SteamID o nombre personalizado",
        "hpw": "Horas por semana que jugás",
        "go": "Calcular",
        "loading": "Contando tus juegos…",
        "help": "En Steam: tu perfil → clic derecho → Copiar URL. Tus detalles de juegos tienen que ser públicos.",
        "privacy": "No guardamos tu perfil ni tus juegos.",
        "finish": "Terminás tu backlog en",
        "unplayed": "juegos sin empezar",
        "of": "de {n}",
        "hours": "horas para terminarlos",
        "years": "años a {h} h por semana",
        "weeks": "semanas a {h} h por semana",
        "short": "Para arrancar ya",
        "long": "Los más largos",
        "note": "Tiempos de IGDB (modo normal, tope de 100 h por juego). Para {n} juegos sin dato usamos la mediana: {h} h.",
        "share": "Compartir resultado",
        "copied": "¡Copiado! Pegalo donde quieras.",
        "shareText": "Tengo {n} juegos de Steam sin empezar: a {h} h por semana termino mi backlog en {y} 💀 ¿Y vos?",
        "ctaTitle": "Guardá tu backlog y andá tachando",
        "ctaBody": "Playloggr junta Steam, PlayStation, Xbox, GOG y Epic en una sola lista, con horas, logros y un plan de juego. Gratis.",
        "ctaBtn": "Crear cuenta gratis",
        "ctaPlay": "App para Android",
        "errNotFound": "No encontramos ese perfil. Probá con el link completo de tu perfil de Steam.",
        "errPrivate": "Tu perfil es privado o no tiene juegos. En Steam: Editar perfil → Privacidad → Detalles del juego: Público.",
        "errRate": "Muchos intentos seguidos. Esperá un minuto y probá de nuevo.",
        "errOther": "Steam no respondió. Probá de nuevo en un rato.",
        "h": "h",
        "footer": "Hecho por Playloggr",
        "home": "Inicio",
        "langName": "Español",
    },
    "en": {
        "title": "When will you finish your Steam backlog? · Free calculator | Playloggr",
        "desc": "Paste your Steam profile and find out how many games you haven't started, how many hours that is and what year you'd finish. Free, no account.",
        "h1": "What year will you finish your backlog?",
        "sub": "Paste your Steam profile and we'll tell you how many games you haven't started and how long they'll take. Free, no account.",
        "label": "Your Steam profile",
        "ph": "Profile link, SteamID or custom URL name",
        "hpw": "Hours you play per week",
        "go": "Calculate",
        "loading": "Counting your games…",
        "help": "On Steam: your profile → right click → Copy Page URL. Your game details must be public.",
        "privacy": "We don't store your profile or your games.",
        "finish": "You'll finish your backlog in",
        "unplayed": "unplayed games",
        "of": "out of {n}",
        "hours": "hours to beat them",
        "years": "years at {h} h a week",
        "weeks": "weeks at {h} h a week",
        "short": "Start with these",
        "long": "The longest ones",
        "note": "Times from IGDB (normal mode, capped at 100 h per game). For {n} games without data we use the median: {h} h.",
        "share": "Share result",
        "copied": "Copied! Paste it anywhere.",
        "shareText": "I have {n} unplayed Steam games: at {h} h a week I'll finish my backlog in {y} 💀 What about you?",
        "ctaTitle": "Save your backlog and start checking games off",
        "ctaBody": "Playloggr puts Steam, PlayStation, Xbox, GOG and Epic in one list, with hours, achievements and a game plan. Free.",
        "ctaBtn": "Create a free account",
        "ctaPlay": "Android app",
        "errNotFound": "We couldn't find that profile. Try the full link to your Steam profile.",
        "errPrivate": "Your profile is private or has no games. On Steam: Edit Profile → Privacy Settings → Game details: Public.",
        "errRate": "Too many tries in a row. Wait a minute and try again.",
        "errOther": "Steam didn't respond. Please try again in a bit.",
        "h": "h",
        "footer": "Made by Playloggr",
        "home": "Home",
        "langName": "English",
    },
    "pt": {
        "title": "Em que ano você termina seu backlog da Steam? · Calculadora grátis | Playloggr",
        "desc": "Cole seu perfil da Steam e descubra quantos jogos você ainda não começou, quantas horas são e em que ano terminaria. Grátis e sem conta.",
        "h1": "Em que ano você termina seu backlog?",
        "sub": "Cole seu perfil da Steam e a gente te diz quantos jogos você não começou e quanto falta. Grátis, sem conta.",
        "label": "Seu perfil da Steam",
        "ph": "Link do perfil, SteamID ou nome personalizado",
        "hpw": "Horas por semana que você joga",
        "go": "Calcular",
        "loading": "Contando seus jogos…",
        "help": "Na Steam: seu perfil → botão direito → Copiar URL. Os detalhes de jogos precisam ser públicos.",
        "privacy": "Não guardamos seu perfil nem seus jogos.",
        "finish": "Você termina seu backlog em",
        "unplayed": "jogos não começados",
        "of": "de {n}",
        "hours": "horas para zerar",
        "years": "anos a {h} h por semana",
        "weeks": "semanas a {h} h por semana",
        "short": "Para começar já",
        "long": "Os mais longos",
        "note": "Tempos do IGDB (modo normal, limite de 100 h por jogo). Para {n} jogos sem dado usamos a mediana: {h} h.",
        "share": "Compartilhar resultado",
        "copied": "Copiado! Cole onde quiser.",
        "shareText": "Tenho {n} jogos da Steam que nem comecei: a {h} h por semana termino meu backlog em {y} 💀 E você?",
        "ctaTitle": "Salve seu backlog e vá riscando",
        "ctaBody": "O Playloggr junta Steam, PlayStation, Xbox, GOG e Epic em uma só lista, com horas, conquistas e um plano de jogo. Grátis.",
        "ctaBtn": "Criar conta grátis",
        "ctaPlay": "App para Android",
        "errNotFound": "Não encontramos esse perfil. Tente o link completo do seu perfil da Steam.",
        "errPrivate": "Seu perfil é privado ou não tem jogos. Na Steam: Editar perfil → Privacidade → Detalhes de jogos: Público.",
        "errRate": "Muitas tentativas seguidas. Espere um minuto e tente de novo.",
        "errOther": "A Steam não respondeu. Tente de novo daqui a pouco.",
        "h": "h",
        "footer": "Feito pelo Playloggr",
        "home": "Início",
        "langName": "Português",
    },
}

TEMPLATE = r"""<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>__TITLE__</title>
<meta name="description" content="__DESC__" />
<link rel="canonical" href="__CANONICAL__" />
__HREFLANG__
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<meta property="og:type" content="website" />
<meta property="og:title" content="__H1__" />
<meta property="og:description" content="__DESC__" />
<meta property="og:url" content="__CANONICAL__" />
<meta property="og:image" content="__OG__" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#132420" />
<script type="application/ld+json">__LDJSON__</script>
<style>
  :root {
    --bg: #111111; --bg2: #1a1a1a; --bg3: #1f1f1f; --border: #2a2a2a;
    --text: #f0f0f0; --text2: #a3a3a3; --green: #1D9E75; --red: #E24B4A;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: var(--bg); color: var(--text); line-height: 1.5; }
  a { color: inherit; }
  .wrap { max-width: 720px; margin: 0 auto; padding: 0 16px; }
  nav { border-bottom: 1px solid var(--border); }
  .nav-inner { display: flex; align-items: center; justify-content: space-between; height: 56px; }
  .logo { font-weight: 800; text-decoration: none; color: var(--green); font-size: 17px; }
  .nav-cta { font-size: 13px; font-weight: 700; text-decoration: none; background: var(--green); color: #fff;
             padding: 7px 12px; border-radius: 8px; }
  header { padding: 44px 0 20px; text-align: center; }
  h1 { font-size: clamp(26px, 6vw, 38px); line-height: 1.15; font-weight: 800; letter-spacing: -0.02em; }
  .sub { color: var(--text2); margin-top: 10px; font-size: 16px; }
  form { background: var(--bg2); border: 1px solid var(--border); border-radius: 14px; padding: 18px; margin-top: 8px; }
  label { display: block; font-size: 13px; font-weight: 700; margin-bottom: 6px; }
  .row { display: flex; gap: 8px; flex-wrap: wrap; }
  input[type=text] { flex: 1 1 260px; min-width: 0; background: var(--bg); color: var(--text); border: 1px solid var(--border);
                     border-radius: 10px; padding: 12px; font-size: 15px; }
  input[type=text]:focus-visible, button:focus-visible, a:focus-visible, input[type=range]:focus-visible { outline: 2px solid var(--green); outline-offset: 2px; }
  button { background: var(--green); color: #fff; border: 0; border-radius: 10px; padding: 12px 18px; font-size: 15px;
           font-weight: 700; cursor: pointer; }
  button:disabled { opacity: .6; cursor: wait; }
  .hpw { margin-top: 14px; }
  .hpw-row { display: flex; align-items: center; gap: 12px; }
  input[type=range] { flex: 1; accent-color: var(--green); }
  .hpw-val { font-weight: 800; min-width: 52px; text-align: right; }
  .help { font-size: 12.5px; color: var(--text2); margin-top: 10px; }
  .msg { margin-top: 14px; padding: 12px 14px; border-radius: 10px; font-size: 14px; display: none; }
  .msg.err { display: block; background: rgba(226,75,74,.12); border: 1px solid rgba(226,75,74,.4); }
  .msg.load { display: block; color: var(--text2); }
  #result { display: none; margin-top: 22px; }
  .card { background: var(--bg2); border: 1px solid var(--border); border-radius: 14px; padding: 20px; }
  .player { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; color: var(--text2); font-size: 14px; }
  .player img { width: 36px; height: 36px; border-radius: 50%; }
  .finish-lbl { color: var(--text2); font-size: 15px; }
  .finish-year { font-size: clamp(56px, 16vw, 88px); font-weight: 900; color: var(--green); line-height: 1; margin: 4px 0 12px; }
  .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
  .stat { background: var(--bg3); border-radius: 10px; padding: 12px; }
  .stat b { display: block; font-size: 22px; }
  .stat span { font-size: 12px; color: var(--text2); }
  @media (max-width: 480px) { .stats { grid-template-columns: 1fr; } }
  .lists { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 14px; }
  @media (max-width: 560px) { .lists { grid-template-columns: 1fr; } }
  .lists h2 { font-size: 14px; margin-bottom: 8px; }
  .lists ol { list-style: none; display: grid; gap: 6px; }
  .lists li { display: flex; justify-content: space-between; gap: 10px; font-size: 14px; background: var(--bg3);
              border-radius: 8px; padding: 8px 10px; }
  .lists li span:first-child { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .lists li span:last-child { color: var(--text2); flex-shrink: 0; }
  .note { font-size: 12px; color: var(--text2); margin-top: 12px; }
  .share { margin-top: 14px; width: 100%; }
  .copied { font-size: 13px; color: var(--green); text-align: center; margin-top: 6px; min-height: 18px; }
  .cta { margin-top: 18px; text-align: center; border: 1px solid var(--green); border-radius: 14px; padding: 20px;
         background: rgba(29,158,117,.08); }
  .cta h2 { font-size: 19px; }
  .cta p { color: var(--text2); font-size: 14px; margin: 6px 0 14px; }
  .cta-row { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
  .btn { display: inline-block; text-decoration: none; font-weight: 700; padding: 11px 16px; border-radius: 10px; font-size: 14px; }
  .btn-main { background: var(--green); color: #fff; }
  .btn-alt { border: 1px solid var(--border); }
  footer { margin: 40px 0 24px; text-align: center; font-size: 12.5px; color: var(--text2); }
  footer a { margin: 0 6px; }
</style>
</head>
<body>
<nav><div class="wrap nav-inner">
  <a class="logo" href="__HOME__">Playloggr</a>
  <a class="nav-cta" href="__CTA_URL__">__CTA_BTN__</a>
</div></nav>

<main class="wrap">
  <header>
    <h1>__H1__</h1>
    <p class="sub">__SUB__</p>
  </header>

  <form id="calc-form" novalidate>
    <label for="steam">__LABEL__</label>
    <div class="row">
      <input type="text" id="steam" name="steam" placeholder="__PH__" autocomplete="off" autocapitalize="off" spellcheck="false" required />
      <button type="submit" id="go">__GO__</button>
    </div>
    <div class="hpw">
      <label for="hpw">__HPW__</label>
      <div class="hpw-row">
        <input type="range" id="hpw" min="1" max="40" step="1" value="5" />
        <output class="hpw-val" id="hpw-val" for="hpw">5 __H_UNIT__</output>
      </div>
    </div>
    <p class="help">__HELP__ __PRIVACY__</p>
    <div class="msg" id="msg" role="status" aria-live="polite"></div>
  </form>

  <section id="result" aria-live="polite">
    <div class="card">
      <div class="player" id="player"></div>
      <div class="finish-lbl">__FINISH__</div>
      <div class="finish-year" id="year"></div>
      <div class="stats">
        <div class="stat"><b id="s-unplayed"></b><span>__UNPLAYED__ <span id="s-of"></span></span></div>
        <div class="stat"><b id="s-hours"></b><span>__HOURS__</span></div>
        <div class="stat"><b id="s-time"></b><span id="s-time-lbl"></span></div>
      </div>
      <div class="lists">
        <div><h2>__SHORT__</h2><ol id="l-short"></ol></div>
        <div><h2>__LONG__</h2><ol id="l-long"></ol></div>
      </div>
      <p class="note" id="note"></p>
      <button type="button" class="share" id="share">__SHARE__</button>
      <div class="copied" id="copied"></div>
    </div>

    <div class="cta">
      <h2>__CTA_TITLE__</h2>
      <p>__CTA_BODY__</p>
      <div class="cta-row">
        <a class="btn btn-main" href="__CTA_URL__">__CTA_BTN__</a>
        <a class="btn btn-alt" href="https://play.google.com/store/apps/details?id=com.playloggr.app&amp;referrer=utm_source%3Dcalculadora%26utm_medium%3Dtool" target="_blank" rel="noopener">__CTA_PLAY__</a>
      </div>
    </div>
  </section>
</main>

<footer class="wrap">
  __FOOTER__ · <a href="__HOME__">__HOME_LBL__</a> · __LANG_LINKS__
</footer>

<script>
(function () {
  var API = 'https://api.playloggr.com/api/v1/public/backlog-calculator';
  var T = __STRINGS__;
  var PAGE = '__CANONICAL__';
  var $ = function (id) { return document.getElementById(id); };
  var last = null;

  function fmt(s, vars) { return s.replace(/\{(\w+)\}/g, function (_, k) { return vars[k]; }); }
  var LANG = document.documentElement.lang;
  function num(n) { return Math.round(n).toLocaleString(LANG); }
  function dec(n) { return Number(n).toLocaleString(LANG, { minimumFractionDigits: 1, maximumFractionDigits: 1 }); }
  function hpw() { return parseInt($('hpw').value, 10) || 5; }

  function finish(hours, perWeek) {
    var weeks = Math.min(hours / perWeek, 52 * 500);
    var d = new Date();
    d.setDate(d.getDate() + Math.round(weeks * 7));
    return { weeks: weeks, years: weeks / 52.18, year: d.getFullYear() };
  }

  function msg(text, kind) {
    var m = $('msg');
    m.textContent = text || '';
    m.className = 'msg' + (kind ? ' ' + kind : '');
  }

  function fillList(ol, items) {
    ol.textContent = '';
    items.forEach(function (g) {
      var li = document.createElement('li');
      var a = document.createElement('span'); a.textContent = g.name;
      var b = document.createElement('span'); b.textContent = num(g.hours) + ' ' + T.h;
      li.appendChild(a); li.appendChild(b); ol.appendChild(li);
    });
  }

  function render() {
    if (!last) return;
    var f = finish(last.hours_total, hpw());
    var p = $('player'); p.textContent = '';
    if (last.player && last.player.name) {
      if (last.player.avatar) { var img = document.createElement('img'); img.src = last.player.avatar; img.alt = ''; p.appendChild(img); }
      var n = document.createElement('span'); n.textContent = last.player.name; p.appendChild(n);
    }
    $('year').textContent = f.year;
    $('s-unplayed').textContent = num(last.unplayed);
    $('s-of').textContent = fmt(T.of, { n: num(last.total_games) });
    $('s-hours').textContent = num(last.hours_total);
    var useYears = f.years >= 1;
    $('s-time').textContent = useYears ? dec(f.years) : num(f.weeks);
    $('s-time-lbl').textContent = fmt(useYears ? T.years : T.weeks, { h: hpw() });
    fillList($('l-short'), last.shortest || []);
    fillList($('l-long'), last.longest || []);
    var missing = last.unplayed - last.games_with_time;
    $('note').textContent = missing > 0 ? fmt(T.note, { n: num(missing), h: dec(last.fallback_hours) }) : '';
    $('result').style.display = 'block';
  }

  async function run(steam) {
    if (!steam) return;
    $('go').disabled = true;
    msg(T.loading, 'load');
    try {
      var r = await fetch(API + '?steam=' + encodeURIComponent(steam) + '&hpw=' + hpw());
      var d = await r.json().catch(function () { return {}; });
      if (!r.ok) {
        var text = r.status === 429 ? T.errRate
          : d.detail === 'not_found' ? T.errNotFound
          : d.detail === 'private_or_empty' ? T.errPrivate : T.errOther;
        $('result').style.display = 'none';
        msg(text, 'err');
        return;
      }
      last = d;
      msg('');
      render();
      try { history.replaceState(null, '', '?steam=' + encodeURIComponent(steam)); } catch (e) {}
      $('result').scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) {
      msg(T.errOther, 'err');
    } finally {
      $('go').disabled = false;
    }
  }

  $('calc-form').addEventListener('submit', function (e) { e.preventDefault(); run($('steam').value.trim()); });
  $('hpw').addEventListener('input', function () { $('hpw-val').textContent = hpw() + ' ' + T.h; render(); });
  $('share').addEventListener('click', async function () {
    if (!last) return;
    var text = fmt(T.shareText, { n: num(last.unplayed), h: hpw(), y: finish(last.hours_total, hpw()).year });
    if (navigator.share) {
      try { await navigator.share({ text: text, url: PAGE }); return; } catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(text + ' ' + PAGE); $('copied').textContent = T.copied; } catch (e) {}
  });

  var q = new URLSearchParams(location.search);
  if (q.get('h')) { $('hpw').value = q.get('h'); $('hpw-val').textContent = hpw() + ' ' + T.h; }
  if (q.get('steam')) { $('steam').value = q.get('steam'); run(q.get('steam')); }
})();
</script>
</body>
</html>
"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build(lang):
    s = L[lang]
    canonical = SITE + PATHS[lang]
    hreflang = "\n".join(
        f'<link rel="alternate" hreflang="{k}" href="{SITE + v}" />' for k, v in PATHS.items()
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{SITE + PATHS["es"]}" />'
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "WebApplication", "name": s["h1"],
        "url": canonical, "applicationCategory": "GameApplication", "operatingSystem": "Web",
        "inLanguage": lang, "description": s["desc"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "publisher": {"@type": "Organization", "name": "Playloggr", "url": SITE},
    }, ensure_ascii=False)
    cta_url = "/app/?register=1&amp;utm_source=calculadora&amp;utm_medium=tool&amp;utm_campaign=backlog_calc"
    lang_links = " · ".join(
        f'<a href="{PATHS[k]}" hreflang="{k}">{L[k]["langName"]}</a>' for k in ("es", "en", "pt") if k != lang
    )
    strings = {k: s[k] for k in ("loading", "of", "years", "weeks", "note", "copied", "shareText",
                                 "errNotFound", "errPrivate", "errRate", "errOther", "h")}
    out = TEMPLATE
    repl = {
        "__LANG__": lang, "__TITLE__": esc(s["title"]), "__DESC__": esc(s["desc"]),
        "__CANONICAL__": canonical, "__HREFLANG__": hreflang, "__OG__": SITE + OG[lang],
        "__LDJSON__": ld, "__HOME__": HOME[lang], "__HOME_LBL__": esc(s["home"]),
        "__CTA_URL__": cta_url, "__CTA_BTN__": esc(s["ctaBtn"]), "__CTA_PLAY__": esc(s["ctaPlay"]),
        "__CTA_TITLE__": esc(s["ctaTitle"]), "__CTA_BODY__": esc(s["ctaBody"]),
        "__H1__": esc(s["h1"]), "__SUB__": esc(s["sub"]), "__LABEL__": esc(s["label"]), "__PH__": esc(s["ph"]),
        "__HPW__": esc(s["hpw"]), "__H_UNIT__": esc(s["h"]), "__GO__": esc(s["go"]), "__HELP__": esc(s["help"]),
        "__PRIVACY__": esc(s["privacy"]), "__FINISH__": esc(s["finish"]), "__UNPLAYED__": esc(s["unplayed"]),
        "__HOURS__": esc(s["hours"]), "__SHORT__": esc(s["short"]), "__LONG__": esc(s["long"]),
        "__SHARE__": esc(s["share"]), "__FOOTER__": esc(s["footer"]), "__LANG_LINKS__": lang_links,
        "__STRINGS__": json.dumps(strings, ensure_ascii=False),
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    assert "__" not in out.replace("__proto__", ""), [x for x in repl if x in out]
    dest = os.path.join(ROOT, PATHS[lang].strip("/").replace("/", os.sep), "index.html")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("ok", dest)


if __name__ == "__main__":
    for lang in ("es", "en", "pt"):
        build(lang)
