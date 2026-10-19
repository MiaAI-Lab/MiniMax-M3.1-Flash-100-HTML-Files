"""Capture actual study screenshots. Install: pip install playwright; playwright install chromium."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]

async def main():
    output = ROOT / 'thumbs'
    output.mkdir(exist_ok=True)
    files = sorted(ROOT.glob('[0-9][0-9][0-9]-*.html'))
    assert len(files) == 100
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=['--no-sandbox'])
        semaphore = asyncio.Semaphore(3)
        async def capture(file):
            async with semaphore:
                page = await browser.new_page(viewport={'width':1440,'height':900}, device_scale_factor=1)
                try:
                    await page.goto(file.as_uri(), wait_until='load')
                    await page.wait_for_timeout(2200)
                    await page.screenshot(path=str(output / (file.stem + '.jpg')), type='jpeg', quality=82, full_page=False, timeout=60000)
                    print(f'Captured {file.name}', flush=True)
                finally:
                    await page.close()
        try:
            await asyncio.gather(*(capture(file) for file in files))
        finally:
            await browser.close()
    assert all((output / (file.stem + '.jpg')).stat().st_size > 1000 for file in files)
    print('Verified 100 screenshots')

if __name__ == '__main__':
    asyncio.run(main())
