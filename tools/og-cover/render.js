// Regenera assets/og-cover.jpg, og-cover-en.jpg y og-cover-pt.jpg (1200x630).
// Uso (desde la raiz del repo web, con Node):
//   npm i -D playwright   (o global)   y   npx playwright install chromium
//   node tools/og-cover/render.js
// Textos: editar el objeto L en og.html. Captura de fondo: assets/screenshots/biblioteca.png
// JPG calidad ~84 para quedar < 100 KB (WhatsApp no muestra previews > ~300 KB).
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  const html = 'file://' + path.join(__dirname, 'og.html');
  for (const [lang, out] of [['es', 'og-cover.jpg'], ['en', 'og-cover-en.jpg'], ['pt', 'og-cover-pt.jpg']]) {
    await p.goto(html + '#' + lang); await p.reload(); await p.waitForTimeout(800);
    await p.screenshot({ path: path.join(__dirname, '../../assets', out), type: 'jpeg', quality: 84 });
    console.log('ok', out);
  }
  await b.close();
})();
