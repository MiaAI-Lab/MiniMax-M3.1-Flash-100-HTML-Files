"""Rebuild the static gallery from the original study prompt files."""
from pathlib import Path
import re
from html import escape

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'MiniMax-M3.1-Flash 100 HTML Files'

def section(text, name):
    match = re.search(r'^' + re.escape(name) + r':\s*\n?(.*?)(?=\n[A-Z][A-Z /-]+:|\Z)', text, re.M | re.S)
    if not match:
        raise ValueError(f'Missing {name} section')
    return match.group(1).strip()

cards = []
files = sorted(ROOT.glob('[0-9][0-9][0-9]-*.html'))
assert len(files) == 100, f'Expected 100 studies, found {len(files)}'
for file in files:
    source = file.with_suffix('.txt')
    text = source.read_text()
    title, prompt, description = (section(text, key) for key in ['TITLE', 'PROMPT', 'DESCRIPTION'])
    num = file.name[:3]
    title, prompt, description = map(escape, [title, prompt, description])
    href = escape(file.name, quote=True)
    cards.append(f'''<article class="card" id="study-{num}">
  <a class="thumb" href="{href}" target="_blank" rel="noopener" aria-label="Open {title}">
    <img src="thumbs/{file.stem}.jpg" width="1440" height="900" alt="{title} screenshot" loading="lazy" decoding="async">
  </a>
  <div class="card-top">
    <div class="num">{num}</div>
    <div class="main"><h2 class="title"><a href="{href}" target="_blank" rel="noopener">{title}</a></h2><p class="desc">{description}</p></div>
    <div class="actions"><a class="btn btn-open" href="{href}" target="_blank" rel="noopener">Open ↗</a><button class="btn btn-prompt" type="button" aria-expanded="false" aria-controls="prompt-{num}">☰ Prompt</button></div>
  </div>
  <div class="prompt-panel" id="prompt-{num}" hidden><h3 class="prompt-label">Original prompt</h3><div class="prompt-text">{prompt}</div><div class="file-name"><a href="{source.name}">{source.name}</a></div></div>
</article>''')

head = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MiniMax-M3.1-Flash 100 HTML Files</title>
<meta name="description" content="100 self-contained HTML studies generated with MiniMax-M3.1-Flash. Browse screenshots, open each experiment, and read its original prompt.">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>
:root{--bg:#f7f6f2;--card:#fff;--line:#e6e1d6;--strong:#cfc6b4;--ink:#211d17;--muted:#665e50;--dim:#9a917f;--accent:#6d28d9;--green:#0e7a5f}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}body{font-family:"Segoe UI",system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--ink);line-height:1.5;min-height:100vh}body:before{content:"";position:fixed;inset:0;pointer-events:none;background:radial-gradient(ellipse 80% 50% at 10% -10%,#6d28d91a,transparent 50%),radial-gradient(ellipse 60% 40% at 90% 0%,#4338ca14,transparent 45%),radial-gradient(ellipse 50% 30% at 50% 100%,#0e7a5f14,transparent 40%)}
.wrap{position:relative;max-width:960px;margin:auto;padding:48px 20px 80px}header{margin-bottom:36px}.eyebrow{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--accent);margin-bottom:12px;font-weight:600}h1{font-size:clamp(28px,5vw,42px);font-weight:800;letter-spacing:-.03em;line-height:1.12;margin-bottom:12px;overflow-wrap:anywhere}h1 span{background:linear-gradient(120deg,#7c3aed,#4f46e5,#0d9488);background-clip:text;color:transparent}.lede{color:var(--muted);font-size:16px;max-width:58ch}
.toolbar{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin:28px 0 8px;position:sticky;top:0;z-index:10;padding:14px 0;background:linear-gradient(180deg,#f7f6f2f5 65%,#f7f6f200);backdrop-filter:blur(8px)}.search{flex:1;min-width:220px;position:relative}.search input{width:100%;background:white;border:1px solid var(--strong);border-radius:10px;padding:12px 14px 12px 40px;font:14px inherit;color:var(--ink);font-family:inherit;font-size:14px}.search input::placeholder{color:var(--dim)}.search svg{position:absolute;left:13px;top:50%;transform:translateY(-50%);width:16px;height:16px;color:var(--dim);pointer-events:none}.count{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);white-space:nowrap}.count b{color:var(--accent)}
.list{display:flex;flex-direction:column;gap:12px;margin-top:8px}.card{background:white;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 1px 2px #1e14320d,0 8px 24px -12px #1e14321f;transition:border-color .2s,box-shadow .2s,transform .15s}.card:hover{border-color:#c9c0ae;transform:translateY(-1px);box-shadow:0 2px 6px #1e14320f,0 16px 34px -16px #1e143233}.thumb{display:block;overflow:hidden;aspect-ratio:8/5;background:#111;position:relative}.thumb img{display:block;width:100%;height:auto;transition:transform .25s}.card:hover .thumb img{transform:scale(1.015)}.live-preview{position:absolute;top:0;left:0;width:1440px;height:900px;border:0;pointer-events:none;transform-origin:top left}.card-top{display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:start;padding:18px 18px 14px}.num{font:12px ui-monospace,monospace;letter-spacing:.06em;color:#5b21b6;background:#6d28d91a;border:1px solid #6d28d938;border-radius:8px;padding:6px 9px;min-width:48px;text-align:center}.main{min-width:0}.title{font-size:17px;font-weight:650;letter-spacing:-.02em;margin-bottom:4px}.title a{color:inherit;text-decoration:none}.title a:hover{color:var(--accent)}.desc{font-size:13.5px;color:var(--muted);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}.actions{display:flex;flex-direction:column;gap:8px}.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:9px 14px;border-radius:9px;font:600 12px inherit;font-family:inherit;font-size:12px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;border:1px solid transparent;cursor:pointer;white-space:nowrap;transition:background .15s,color .15s}.btn-open{background:linear-gradient(135deg,#7c3aed24,#4f46e51f);color:#5b21b6;border-color:#7c3aed59}.btn-open:hover{background:linear-gradient(135deg,#7c3aed,#4f46e5);color:white}.btn-prompt{background:transparent;color:var(--muted);border-color:var(--strong)}.btn-prompt:hover{background:#fbfaf7}.btn-prompt[aria-expanded=true]{color:var(--green);border-color:#0e7a5f66;background:#0e7a5f14}.prompt-panel{border-top:1px solid var(--line);padding:16px 18px 18px;background:#f4f1ea}.prompt-label{font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--green);margin-bottom:10px;font-weight:600}.prompt-text{font-size:13.5px;color:#47402f;line-height:1.65;white-space:pre-wrap;overflow-wrap:anywhere}.file-name{margin-top:12px;font:11px ui-monospace,monospace;color:var(--muted)}.file-name a{color:inherit}.empty{text-align:center;padding:60px 20px;color:var(--muted);border:1px dashed var(--strong);border-radius:14px;background:#ffffff99}footer{margin-top:48px;padding-top:20px;border-top:1px solid var(--strong);font-size:12px;color:var(--muted);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}footer a{color:var(--accent)}[hidden]{display:none!important}:focus-visible{outline:3px solid #7c3aed;outline-offset:3px}
@media(max-width:640px){.card-top{grid-template-columns:auto 1fr}.actions{grid-column:1/-1;flex-direction:row}.btn{flex:1}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*:before,*:after{transition:none!important;animation:none!important}}
</style>
</head>
<body><main class="wrap">
<header><div class="eyebrow">Collection · 100 studies</div><h1>MiniMax-M3.1-Flash <span>100 HTML</span> Files</h1><p class="lede">One hundred self-contained visual studies — generative art, physics, typography, interfaces and scenes — generated with MiniMax-M3.1-Flash. Open any piece in a new tab, or expand a card to read the original generation prompt.</p></header>
<div class="toolbar"><div class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><input type="search" id="q" aria-label="Search by name, number, or prompt" placeholder="Search by name, number, or prompt…" autocomplete="off" spellcheck="false"></div><div class="count" id="count" role="status" aria-live="polite"><b>100</b> studies</div></div>
<div class="list" id="list">
'''
tail = '''</div>
<p class="empty" id="empty" hidden>No studies match your search. Try another name, number, or keyword.</p>
<noscript><p>All studies and their screenshots are listed above. Enable JavaScript for search and the Prompt buttons. Original prompts are also available in the matching .txt files.</p></noscript>
<footer><span>MiniMax-M3.1-Flash · 100 self-contained HTML studies</span><a href="https://github.com/MiaAI-Lab/MiniMax-M3.1-Flash-100-HTML-Files">View on GitHub ↗</a></footer>
</main>
<script>
const cards = [...document.querySelectorAll('.card')];
const searchText = cards.map(card => card.textContent.toLowerCase());
document.querySelector('#q').addEventListener('input', event => {
  const words = event.target.value.toLowerCase().trim().split(/\\s+/);
  let visible = 0;
  cards.forEach((card, i) => {card.hidden = !words.every(word => searchText[i].includes(word)); if (!card.hidden) visible++;});
  document.querySelector('#count').innerHTML = `<b>${visible}</b> ${visible === 1 ? 'study' : 'studies'}`;
  document.querySelector('#empty').hidden = visible !== 0;
});
document.querySelector('#list').addEventListener('click', event => {
  const button = event.target.closest('.btn-prompt');
  if (!button) return;
  const expanded = button.getAttribute('aria-expanded') !== 'true';
  button.setAttribute('aria-expanded', String(expanded));
  document.getElementById(button.getAttribute('aria-controls')).hidden = !expanded;
});
// A local checkout can show live studies until real screenshots are captured.
const resize = new ResizeObserver(entries => entries.forEach(({target, contentRect}) => {
  const frame = target.querySelector('iframe');
  if (frame) frame.style.transform = `scale(${contentRect.width / 1440})`;
}));
for (const img of document.querySelectorAll('.thumb img')) {
  const fallback = () => {
    if (img.parentElement.querySelector('iframe')) return;
    const link = img.parentElement;
    const frame = document.createElement('iframe');
    frame.className = 'live-preview';
    frame.title = img.alt.replace(' screenshot', ' live preview');
    frame.loading = 'lazy';
    frame.tabIndex = -1;
    frame.setAttribute('sandbox', 'allow-scripts');
    frame.setAttribute('aria-hidden', 'true');
    frame.src = link.getAttribute('href');
    img.hidden = true;
    link.append(frame);
    resize.observe(link);
  };
  img.addEventListener('error', fallback, {once:true});
  if (img.complete && img.naturalWidth === 0) fallback();
}
</script>
</body></html>
'''
(ROOT / 'index.html').write_text(head + '\n'.join(cards) + tail)
print(f'Built index.html with {len(cards)} studies and complete original prompts')
