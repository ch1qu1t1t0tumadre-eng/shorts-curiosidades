// Pegar con javascript_tool en la pestaña de Studio (cualquier página de studio.youtube.com del canal).
// Devuelve, para cada ID, la curva de retención (41 puntos de 0 % a 100 % del vídeo, en % de espectadores),
// "se quedaron viendo" (%) y vistas. Uso: await window.__curvas(['ID1','ID2'])
window.__curvas = async function (ids) {
  const sl = ms => new Promise(r => setTimeout(r, ms));
  const curve = function (doc, N) {
    const e = [...doc.querySelectorAll('*')].find(x => x.children.length == 0 && x.textContent.trim() == 'Retención de la audiencia');
    if (!e) return null;
    let c = e; for (let i = 0; i < 10; i++) { c = c.parentElement; if (c.querySelectorAll('path').length) break; }
    const p = c.querySelector('path'); if (!p) return null;
    const nums = p.getAttribute('d').match(/-?[\d.]+/g).map(Number); const pts = [];
    for (let i = 0; i + 1 < nums.length; i += 2) pts.push([nums[i], nums[i + 1]]);
    const ticks = [...c.querySelectorAll('*')].filter(x => x.children.length == 0 && /^\d+\s*%$/.test(x.textContent.trim()))
      .map(x => [parseFloat(x.textContent), x.getBoundingClientRect().top + x.getBoundingClientRect().height / 2]);
    const m = p.getScreenCTM(); const scr = pts.map(([x, y]) => [m.a * x + m.e, m.d * y + m.f]);
    const [t0, t1] = [ticks[0], ticks[ticks.length - 1]]; const toPct = y => t0[0] + (y - t0[1]) * (t1[0] - t0[0]) / (t1[1] - t0[1]);
    const x0 = scr[0][0], x1 = scr[scr.length - 1][0]; const out = [];
    for (let k = 0; k <= N; k++) { const xs = x0 + (x1 - x0) * k / N; const b = scr.reduce((a, q) => Math.abs(q[0] - xs) < Math.abs(a[0] - xs) ? q : a); out.push(Math.round(toPct(b[1]) * 10) / 10); }
    return out;
  };
  const res = {};
  for (const id of ids) {
    const f = document.createElement('iframe'); f.style.cssText = 'width:1300px;height:2200px;position:fixed;left:-3000px;top:0';
    f.src = '/video/' + id + '/analytics/tab-overview/period-default'; document.body.appendChild(f);
    let r = { curva: null };
    for (let i = 0; i < 25; i++) {
      await sl(800);
      try { const doc = f.contentDocument; const t = doc && doc.body ? doc.body.innerText : '';
        if (/Se quedaron viendo/.test(t)) { await sl(1500); const t2 = doc.body.innerText;
          r = { curva: curve(doc, 40), stayed: (t2.match(/([\d,]+)\s*%\s*\n+\s*Se quedaron viendo/) || [])[1],
                vistas: (t2.match(/Visualizaciones\s*\n+\s*([\d.,]+\s?K?)\s*\n/) || [])[1] }; break; } } catch (e) { r = { error: e.message }; break; }
    }
    res[id] = r; f.remove();
  }
  return res;
};
'ok'
