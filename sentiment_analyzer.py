import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

class SentimentAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = LogisticRegression()
        self.data = None
        
    def load_data(self, file_path):
        
        self.data = pd.read_csv(file_path)
        return self.data
    
    def prepare_data(self, text_column, label_column):
        """
        تجهيز البيانات
        """
        if self.data is None:
            raise ValueError("التحميل من load_data()")
            
        # معالجة ق م
        self.data = self.data.dropna(subset=[text_column, label_column])
        
        X = self.vectorizer.fit_transform(self.data[text_column])
        y = self.data[label_column]
        
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def train(self, X_train, y_train):
        """
       بداية تدريب 
        """
        self.model.fit(X_train, y_train)
    
    def evaluate(self, X_test, y_test):
        
        predictions = self.model.predict(X_test)
        return accuracy_score(y_test, predictions), classification_report(y_test, predictions)
    
    def predict(self, text):
        
        text_vectorized = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vectorized)[0]
        
        # تحويل  إلى وصف
        sentiment_map = {
            1.0: "إيجابي",
            0.0: "محايد",
            -1.0: "سلبي"
        }
        return sentiment_map.get(prediction, "غير معروف")


if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
   