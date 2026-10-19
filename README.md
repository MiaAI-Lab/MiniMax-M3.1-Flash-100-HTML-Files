# MiniMax-M3.1-Flash 100 HTML Files

100 self-contained HTML studies, with a searchable gallery, screenshot previews, and each study’s complete original generation prompt. The gallery follows the layout of https://miaai-lab.github.io/Fable-5.1-100-HTML-Files/.

Open `index.html` locally. When screenshots are absent, the gallery shows sandboxed live previews. Published screenshots are actual 1440 × 900 browser captures.

Rebuild the gallery:

```sh
python scripts/build_gallery.py
```

Generate all 100 screenshots locally (requires a working Chromium browser):

```sh
pip install playwright
python -m playwright install chromium
python scripts/capture_screenshots.py
```

To push to the requested repository and enable GitHub Pages, run with authenticated GitHub CLI access and repository administration rights:

```sh
bash scripts/publish.sh
```

The script preserves remote history in a temporary checkout, uploads the gallery, all 100 studies and prompt files, and configures Pages to use GitHub Actions. On every push to `main`, the workflow rebuilds the gallery, captures every study, and deploys the result to Pages. Deployment success must be confirmed in the repository’s Actions tab.

Expected URL after deployment: https://miaai-lab.github.io/MiniMax-M3.1-Flash-100-HTML-Files/
