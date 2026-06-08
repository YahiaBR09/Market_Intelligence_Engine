import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import random

# قائمة الكلمات الدلالية لجميع الأصناف المطابقة لموقع العميل
keywords = ["Spanners", "Sockets", "Pliers", "Screwdrivers"]
filename = "bunnings_competitor_prices.csv"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}

total_scraped_all = 0
# مصفوفة شاملة لمنع التكرار على مستوى الملف بالكامل وللتحقق من نهاية الصفحات
scraped_product_urls = set()

print(f"🔄 جاري بدء منظومة كشط الأقسام المتعددة للمنافس بآلية الانتقال الموالي الذكية...")

# إنشاء الملف وكتابة العناوين الرئيسية (Header) في البداية
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['SKU/ID', 'Product Name', 'Price (FJD)', 'Product URL'])

session = requests.Session()
session.headers.update(headers)

# حلقة التكرار الكبرى للمرور على الأصناف
for keyword in keywords:
    print(f"\n🎯 ==================== جاري بدء البحث عن الصنف: [{keyword}] ====================")
    page_number = 1
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        while True:
            page_url = f"https://comepetitorweb.com.fj/search?q={keyword}&page={page_number}"
            print(f"📄 جاري فحص الصفحة رقم [{page_number}] للصنف [{keyword}] عبر الرابط: {page_url}")
            
            try:
                response = session.get(page_url, timeout=15)
                
                if response.status_code == 429:
                    print("⚠️ السيرفر طلب التهدئة (429). سننتظر 12 ثانية...")
                    time.sleep(12)
                    response = session.get(page_url, timeout=15)
                
                if response.status_code != 200:
                    print(f"🏁 توقف استجابة الرابط. ننتقل للبحث الموالي [{keyword}].")
                    break
                    
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # استهداف كروت المنتجات
                product_elements = soup.find_all('li', class_='product-grid__item')
                if not product_elements:
                    product_elements = soup.find_all('div', class_=re.compile(r'product-card|grid-product'))
                
                if not product_elements or len(product_elements) == 0:
                    print(f"🏁 لا توجد عناصر في الصفحة. ننتقل للبحث الموالي.")
                    break
                
                page_new_items_count = 0
                
                # استخراج وفحص المنتجات داخل الصفحة الحالية
                for product in product_elements:
                    title_el = product.find(['h3', 'div', 'a'], class_=re.compile(r'title|name|product-card__title'))
                    if not title_el:
                        continue
                    title = title_el.text.strip()
                    
                    # --- 🛠️ حل مشكلة تكرار السعر (مثل 13.7613.76) ---
                    price_el = product.find(['span', 'div'], class_=re.compile(r'price|visually-hidden'))
                    if price_el:
                        raw_price = price_el.text.strip()
                        # تنظيف النص من أي رموز وابقاء الأرقام والنقاط فقط
                        clean_price = re.sub(r'[^\d.]', '', raw_price)
                        
                        # إذا كان السعر مكرراً (يحتوي على نقطتين عشريتين مثل 13.7613.76)
                        if clean_price.count('.') == 2:
                            # شق السعر من المنتصف لآخذ الجزء الأول الصحيح فقط
                            half_length = len(clean_price) // 2
                            price = clean_price[:half_length]
                        else:
                            price = clean_price
                    else:
                        price = "0.00"
                    
                    # روابط المنتجات والـ SKU
                    link_el = product.find('a')
                    if link_el and 'href' in link_el.attrs:
                        relative_url = link_el['href']
                        full_url = f"https://bunningspacific.com.fj{relative_url}"
                        sku = relative_url.split('/')[-1].split('?')[0]
                    else:
                        full_url = "N/A"
                        sku = "N/A"
                    
                    # التحقق الصارم من عدم التكرار
                    if full_url not in scraped_product_urls and full_url != "N/A":
                        scraped_product_urls.add(full_url)
                        writer.writerow([sku, title, price, full_url])
                        page_new_items_count += 1
                        total_scraped_all += 1
                
                print(f"📊 تم تسجيل {page_new_items_count} منتج جديد فريد من هذه الصفحة.")
                
                # 🛑 آلية التوقف الذكي والانتقال الموالي الحرة:
                # إذا كانت الصفحة تحتوي على منتجات، ولكن لم نسجل منها "أي منتج جديد" 
                # فهذا يعني قطعياً أننا وصلنا للنهاية والموقع يعيد عرض الصفحة الأخيرة، فننتقل فوراً للبحث الموالي!
                if page_new_items_count == 0:
                    print(f"🏁 وصلنا لآخر صفحة حقيقية (لم تظهر منتجات جديدة). الانتقال التلقائي للبحث الموالي...")
                    break
                
                page_number += 1
                # وقت راحة عشوائي طبيعي للبشر
                time.sleep(random.uniform(2, 3))
                
            except Exception as e:
                print(f"🚨 حدث خطأ أثناء معالجة الصنف {keyword} صفحة {page_number}: {e}")
                break
                
    print(f"⏳ استراحة قصيرة لتهدئة السيرفر قبل الانتقال للصنف الموالي...")
    time.sleep(4)

print(f"\n🎉 نجاح باهر ومكتمل للمشروع بالكامل!")
print(f"📊 إجمالي المنتجات الصافية والمستخرجة للمنافس من كافة الأصناف: {total_scraped_all} منتج بنجاح!")
