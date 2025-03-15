import pytest
import pytest_asyncio
import asyncio
import os
from playwright.async_api import async_playwright, Page

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def page(request):
    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=False,  # False: popup browser
        slow_mo=0,
        args=['--disable-http2']  # Disable HTTP/2 when using VPN!!!
    )
    context = await browser.new_context(
        #viewport={"width": 1920, "height": 1080}
    )
    os.makedirs("traces", exist_ok=True)

    test_name = request.node.name
    await context.tracing.start(screenshots=True, snapshots=True)
    
    page = await context.new_page()
    
    await page.goto("https://staging2.ca.powersports.honda.com/help-me-choose", timeout=300000, wait_until='networkidle')
    
    yield page

    # Lưu trace với tên file dựa trên tên test
    trace_path = f"traces/{test_name}.zip"
    await context.tracing.stop(path=trace_path)
    print(f"Trace saved to: {trace_path}")
    
    await page.close()
    await context.close()
    await browser.close()
    await playwright.stop()