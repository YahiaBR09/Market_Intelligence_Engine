import pandas as pd
import numpy as np

print("📊 جاري بدء عملية تحليل ومقارنة الأسعار...")

# 1. قراءة ملف البيانات الحقيقي الذي قشته أنت (Bunnings)
try:
    df_bunnings = pd.read_csv("web_competitor_prices.csv")
    print(f"✅ تم تحميل {len(df_bunnings)} منتج من ملف المنافس بنجاح.")
except FileNotFoundError:
    print("❌ خطأ: لم يتم العثور على ملف web_competitor_prices.csv! تأكد من تشغيل السكربت الأول أولاً.")
    exit()

# 2. محاكاة بيانات متجر العميل (Vinod Patel) للتجربة:
# سنأخذ نفس أسماء المنتجات ولكن سنغير أسعارها عشوائياً لنرى كيف سيكتشف السكربت الفروقات التجارية!
df_vinod = df_bunnings.copy()
df_vinod = df_vinod.rename(columns={'Price (FJD)': 'Our Price', 'SKU/ID': 'Our SKU'})
df_vinod = df_vinod.drop(columns=['Product URL'])

# تغيير الأسعار عشوائياً (بعضها أرخص وبعضها أغلى) لمحاكاة الواقع
np.random.seed(42)
df_vinod['Our Price'] = df_vinod['Our Price'].astype(float)
df_bunnings['Price (FJD)'] = df_bunnings['Price (FJD)'].astype(float)
df_vinod['Our Price'] = (df_vinod['Our Price'] * np.random.uniform(0.85, 1.15, len(df_vinod))).round(2)

# 3. عملية الدمج الذكي (Inner Join) بناءً على تطابق اسم المنتج
# هذا هو السحر الذي يبحث عنه العميل لمعرفة المنتجات المشتركة!
df_comparison = pd.merge(df_bunnings, df_vinod, on='Product Name', how='inner')

# 4. حساب الفروقات المالية
df_comparison['Price Difference (FJD)'] = (df_comparison['Our Price'] - df_comparison['Price (FJD)']).round(2)

# تحديد من هو الأرخص في خانة مخصصة كتقرير تسويقي للعميل
df_comparison['Status'] = np.where(
    df_comparison['Price Difference (FJD)'] > 0, 'Competitor is Cheaper',
    np.where(df_comparison['Price Difference (FJD)'] < 0, 'We are Cheaper', 'Equal Price')
)

# إعادة ترتيب الأعمدة بشكل مريح للعين والمدراء
df_comparison = df_comparison[[
    'Product Name', 'Our Price', 'Price (FJD)', 'Price Difference (FJD)', 'Status', 'Product URL'
]]
df_comparison = df_comparison.rename(columns={'Price (FJD)': 'Competitor Price'})

# 5. حفظ النتيجة النهائية في ملف Excel فخم (وليس CSV عادي) لأن العملاء والمدراء يعشقون الإكسيل
output_file = "Final_Price_Comparison_Report.xlsx"
df_comparison.to_excel(output_file, index=False)

print(f"\n🎉 مبروك! تم إنشاء تقرير مقارنة الأسعار الشامل وحفظه في: {output_file}")
print(f"📊 إجمالي المنتجات التي تم مطابقتها ومقارنتها: {len(df_comparison)} منتج.")

# عرض عينة صغيرة في التيرمنال لنرى النتيجة
print("\n👀 عينة من تقرير المقارنة الذكي:")
print(df_comparison[['Product Name', 'Our Price', 'Competitor Price', 'Price Difference (FJD)', 'Status']].head())
