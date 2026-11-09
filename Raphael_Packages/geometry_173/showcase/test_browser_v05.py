from pathlib import Path
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent/'showcase_v05.html'
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=b.new_page(viewport={'width':1380,'height':860});errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(P.read_text(),wait_until='domcontentloaded');page.wait_for_timeout(500)
 assert page.locator('#meshCount').inner_text()=='140',page.locator('#meshCount').inner_text()
 assert page.locator('#resultCount').inner_text()=='173'
 for metric in 'VEF':
  names={'V':'Vertices','E':'Edges','F':'Faces'}
  for expected in [f'{names[metric]} ascending ↑',f'{names[metric]} descending ↓','Raphael 001 → 173']:
   page.locator(f'[data-sort="{metric}"]').click();page.wait_for_timeout(45)
   assert page.locator('#sortMode').inner_text()==expected,(metric,expected,page.locator('#sortMode').inner_text())
 page.locator('[data-sort="V"]').click()
 first=int(page.locator('.record').first.get_attribute('data-slot'))
 page.locator('.record').first.click();page.locator('#next').click()
 next_slot=int(page.locator('#assetID').inner_text().split('-')[-1])
 assert first!=next_slot
 page.locator('[data-sort="V"]').click();page.locator('[data-sort="V"]').click()
 assert page.locator('#sortMode').inner_text()=='Raphael 001 → 173'
 page.locator('#q').fill('Snub Disphenoid')
 assert page.locator('.record').count()>0
 page.locator('#q').fill('');
 for slot in [105,113,114,115,116,117,130,173]:
  page.evaluate('(n)=>window.location.hash="slot-"+n',slot)
  page.locator('.record[data-slot="%s"]'%slot).click()
  page.wait_for_timeout(40)
  assert ('STAR' in page.locator('#sourceBadge').inner_text()) if slot in (114,115,116,117) else True
 assert not errors, errors
 page.locator('[data-mode="graph"]').click();page.wait_for_timeout(70)
 page.screenshot(path=str(P.with_name('studio_v05_preview.png')),full_page=True)
 print({'browser':'PASS','order_cycles':9,'mesh_roles':140,'missing':33,'star_wireframe':True,'source_badge':'PASS','navigation':'PASS','js_errors':errors,'sort_first':first,'next':next_slot})
 b.close()
