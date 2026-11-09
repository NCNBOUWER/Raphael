from playwright.sync_api import sync_playwright
from pathlib import Path
ROOT=Path(__file__).resolve().parent
URL=(ROOT/'showcase.html').as_uri()
with sync_playwright() as p:
 kwargs={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage','--disable-background-networking','--disable-extensions']}
 if Path('/usr/bin/chromium').exists():kwargs['executable_path']='/usr/bin/chromium'
 browser=p.chromium.launch(**kwargs)
 page=browser.new_page(viewport={'width':1440,'height':900},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((Path(__file__).resolve().parent/"showcase.html").read_text(),wait_until="domcontentloaded",timeout=10000)
 page.wait_for_timeout(400)
 print('title',page.title(),'head',page.locator('#assetName').inner_text(),'rows',page.locator('.record').count(),'meshCount',page.locator('#meshCount').inner_text())
 page.screenshot(path=str(ROOT/'studio-preview.png'),full_page=True,timeout=10000)
 page.locator('#q').fill('J78')
 print('filter_records',page.locator('.record').count(),'filtered_label',page.locator('.record').first.inner_text())
 page.locator('.record').first.click()
 print('picked_slot',page.locator('#assetID').inner_text())
 page.locator('#add').click()
 print('composite_status',page.locator('#basketStatus').inner_text())
 page.locator('[data-mode="graph"]').click()
 print('graph mode',page.locator('#sceneWrap').get_attribute('class'))
 print('errors',errors)
 assert not errors,errors
 assert '099' in page.locator('#assetID').inner_text()
 assert page.locator('#export').is_enabled()
 browser.close()
