import pandas as pd
from sentiment_analyzer import SentimentAnalyzer

def main():
   
    analyzer = SentimentAnalyzer()
    
   
  
    data = analyzer.load_data("Twitter_Data.csv")
    
    # عرض معلومات عن البيانات
   
    print(data.info())
   
    print(data['category'].value_counts())
    
    # تجهيز البيانات للتدريب
   
    X_train, X_test, y_train, y_test = analyzer.prepare_data("clean_text", "category")
    
   
  
    analyzer.train(X_train, y_train)
    
    # تقييم 
    
    accuracy, report = analyzer.evaluate(X_test, y_test)
  
   
    print(report)
    
    # اختبار النموذج على نصوص جديدة
   
    while True:
        text = input("\nأدخل نصاً للتحليل (اضغط Enter للخروج): ")
        if not text:
            break
        sentiment = analyzer.predict(text)
        print(f"المشاعر المتوقعة: {sentiment}")

if __name__ == "__main__":
    main()
