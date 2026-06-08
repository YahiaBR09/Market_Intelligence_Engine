from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import re
import time

# نفس قائمة الكلمات الدلالية لضمان تطابق تصنيفات التقرير النهائي
keywords = ["Spanners", "Sockets", "Pliers", "Screwbrivers"] # تم تصحيح الكتابة لتطابق محرك بحث العميل
filename = "vinod_real_prices.csv"

print("🚀 جاري تشغيل منظومة الكشط الشاملة للأقسام المتعددة بمضاد الإعلانات الحركي...")

# إنشاء الملف وكتابة الهيدر الأساسي مرة واحدة فقط في البداية
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Our Product Name', 'Our Price', 'Our SKU'])

total_scraped_all = 0
scraped_skus = set() # للحفاظ على عزل التكرار الشامل عبر كافة الأقسام

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # يمكنك تحويلها لـ False إذا رغبت في المراقبة بالعين
    page = browser.new_page()
    
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    for keyword in keywords:
        print(f"\n🎯 ==================== جاري بدء قشط صنف العميل: [{keyword}] ====================")
        url = f"https://www.customerweb.com.fj/search?q={keyword}"
        
        print(f"🌐 جاري فتح الصفحة الأولى للصنف...")
        try:
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_selector("h3", timeout=15000)
        except Exception:
            print(f"❌ تعذر تحميل نتائج هذا الصنف أو لا توجد منتجات له، ننتقل للصنف التالي.")
            continue
            
        # مضاد الإعلانات والمنبثقات لكل قسم جديد
        try:
            popup_close_selectors = [
                "button[aria-label='Close']", "button:has-text('Close')", 
                ".modal-close", "button:has-text('Dismiss')"
            ]
            for selector in popup_close_selectors:
                locator = page.locator(selector).first
                if locator.is_visible():
                    print("🛡️ تم كشف إعلان منبثق وإغلاقه بنجاح...")
                    locator.click()
                    time.sleep(1)
        except Exception:
            pass

        current_page = 1
        
        # فتح الملف بوضع الإضافة 'a' لحماية وحفظ المنتجات السابقة
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            while True:
                print(f"📸 جاري استخراج منتجات [{keyword}] - (صفحة {current_page})...")
                
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                product_cards = soup.find_all('div', role='link')
                
                page_new_items = 0
                for card in product_cards:
                    title_el = card.find('h3')
                    if not title_el:
                        continue
                    title = title_el.text.strip()
                    
                    price = "0.00"
                    price_container = card.find('div', class_=re.compile(r'font-sriracha|bg-gray-50'))
                    if price_container:
                        price_spans = price_container.find_all('span')
                        if len(price_spans) >= 2:
                            raw_price = price_spans[1].text.strip()
                            price = re.sub(r'[^\d.]', '', raw_price)
                        else:
                            price = re.sub(r'[^\d.]', '', price_container.text)
                    
                    sku = "N/A"
                    img_el = card.find('img')
                    if img_el and img_el.get('srcset'):
                        sku_match = re.search(r'(A\d+)', img_el.get('srcset'))
                        if sku_match:
                            sku = sku_match.group(1)
                    elif img_el and img_el.get('alt'):
                        sku_match = re.search(r'(A\d+)', img_el.get('alt'))
                        if sku_match:
                            sku = sku_match.group(1)
                    
                    identifier = sku if sku != "N/A" else title
                    if identifier not in scraped_skus:
                        scraped_skus.add(identifier)
                        writer.writerow([title, price, sku])
                        page_new_items += 1
                        total_scraped_all += 1
                
                print(f"📊 تم تسجيل {page_new_items} منتج فريد من الصفحة الحالية.")
                
                # البحث عن زر التنقل والتنقل الحركي الآمن
                next_button = page.locator("button:has-text('Next')").first
                if not next_button.is_visible():
                    next_button = page.locator("button[aria-label='Next page']").first
                
                if next_button and next_button.is_visible() and next_button.is_enabled():
                    old_page_content = page.content()
                    print("🖱️ جاري الانتقال الحركي للصفحة التالية عبر Force Click...")
                    next_button.click(force=True)
                    time.sleep(3)
                    
                    if page.content() == old_page_content:
                        print("🏁 المحتوى متطابق بعد الضغط. ننتقل للصنف القادم.")
                        break
                    current_page += 1
                else:
                    print(f"🏁 انتهت صفحات الصنف [{keyword}].")
                    break
                    
    browser.close()

print(f"\n🎉 تم اكتمال الكشط الشامل والأوتوماتيكي لجميع الأصناف بنجاح تام!")
print(f"📊 إجمالي المنتجات الحقيقية المستخرجة لملف العميل: {total_scraped_all} منتج محفوظ في {filename}")
