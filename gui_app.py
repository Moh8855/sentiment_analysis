import tkinter as tk
from tkinter import ttk, scrolledtext
from sentiment_analyzer import SentimentAnalyzer
import threading
from tkinter import messagebox

class SentimentAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("محلل مشاعر التغريدات ")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
       
        self.analyzer = SentimentAnalyzer()
        self.setup_gui()
        
    def setup_gui(self):
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
       
        title_label = ttk.Label(
            main_frame, 
            text="محلل المشاعر ",
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=20)
        
        # الادخال
        text_label = ttk.Label(
            main_frame,
            text="أدخل النص المراد تحليله:",
            font=('Arial', 12)
        )
        text_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10,5))
        
        self.text_input = scrolledtext.ScrolledText(
            main_frame,
            width=60,
            height=8,
            font=('Arial', 12),
            wrap=tk.WORD
        )
        self.text_input.grid(row=2, column=0, columnspan=2, pady=(0,20))
        
        #  للنسخ واللصق
        self.text_input.bind('<Control-v>', self.paste_text)
        self.text_input.bind('<Control-V>', self.paste_text)
        self.text_input.bind('<Control-c>', self.copy_text)
        self.text_input.bind('<Control-C>', self.copy_text)
        self.text_input.bind('<Control-x>', self.cut_text)
        self.text_input.bind('<Control-X>', self.cut_text)
        
       
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        # زر ل
        paste_button = ttk.Button(
            button_frame,
            text="لصق النص",
            command=self.paste_text
        )
        paste_button.pack(side=tk.LEFT, padx=5)
        
        # زر ت
        self.analyze_button = ttk.Button(
            button_frame,
            text="تحليل النص",
            command=self.analyze_text,
            style='Accent.TButton'
        )
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        # النتيجة
        result_frame = ttk.LabelFrame(main_frame, text="نتيجة التحليل", padding="10")
        result_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        self.result_label = ttk.Label(
            result_frame,
            text="النتيجة ستظهر هنا",
            font=('Arial', 14)
        )
        self.result_label.grid(row=0, column=0, pady=10)
        
        # حالة التحميل
        self.status_label = ttk.Label(
            main_frame,
            text="",
            font=('Arial', 10)
        )
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5)
        
        
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 12))
    
    def paste_text(self, event=None):
        try:
            text = self.root.clipboard_get()
            self.text_input.delete('1.0', tk.END)  # Clear النص
            self.text_input.insert(tk.INSERT, text)
        except:
            pass
        return 'break'
    
    def copy_text(self, event=None):
        try:
            text = self.text_input.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
        except:
            pass
        return 'break'
    
    def cut_text(self, event=None):
        try:
            text = self.text_input.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.text_input.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except:
            pass
        return 'break'
    
    def load_model(self):
        try:
            self.status_label.config(text="جاري تحميل النموذج...")
            self.analyzer.load_data("Twitter_Data.csv")
            X_train, X_test, y_train, y_test = self.analyzer.prepare_data("clean_text", "category")
            self.analyzer.train(X_train, y_train)
            self.status_label.config(text="تم تحميل النموذج بنجاح!")
            self.analyze_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تحميل النموذج: {str(e)}")
            self.status_label.config(text="فشل تحميل النموذج")
    
    def analyze_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("تنبيه", "الرجاء إدخال نص للتحليل")
            return
        
        try:
            sentiment = self.analyzer.predict(text)
            
            # تعيين لون النتيجة حسب التصنيف
            color = {
                "إيجابي": "#28a745",
                "محايد": "#ffc107",
                "سلبي": "#dc3545"
            }.get(sentiment, "black")
            
            self.result_label.config(
                text=f"النص {sentiment}",
                foreground=color
            )
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التحليل: {str(e)}")

def main():
    root = tk.Tk()
    root.title("محلل المشاعر")
    
    
    root.configure(bg='#f0f0f0')
    try:
        root.tk.call('encoding', 'system', 'utf-8')
    except:
        pass
    
    app = SentimentAnalyzerGUI(root)
    
   
    loading_thread = threading.Thread(target=app.load_model)
    loading_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()
