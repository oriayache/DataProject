import pandas as pd 
import os
import matplotlib.pyplot as plt
import io
import base64

dir_path = os.path.dirname(os.path.realpath(__file__))

def render_plot():
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    buffer = b''.join(img)
    b2 = base64.b64encode(buffer)
    plot_Climb = b2.decode('utf-8')
    plt.clf()
    return plot_Climb

# הפונקציה צובעת את כל הערכים שמעל הממוצע בירוק את כל הערכים שמתחת בצבע אדום
def color_negative_red_color_positive_green(val,avg):
    color = 'black'

    if val < avg:
        color = 'red'
   
    elif val > avg:
        color = 'green'

    return 'color: %s' % color


def create_html_page_for_src1():
    
    df = pd.read_csv(f'{dir_path}/Src/dead_sea_level.csv') # פותח את הטבלה מקובץ אקסל ומגדיר אותה כדאטה פריים. 


    df['מפלס'] = df['מפלס'].astype('float') # הופך את הטור מפלס לטור מסוג מספר ממשי
    avg = df['מפלס'].mean() # מחשב ממוצע של הטור
    
    df = df.head(20)
    s = df.style.applymap(lambda x: color_negative_red_color_positive_green(x,avg) ,subset=['מפלס'])
    Tables =s.hide_index().render()
    
    
    return Tables

def create_plot_for_compere():
    df1 = pd.read_csv(f'{dir_path}/Src/dead_sea_level.csv') # פותח את הטבלה מקובץ אקסל ומגדיר אותה כדאטה פריים.
    
    df2 = pd.read_csv(f'{dir_path}/Src/kinneret_level.csv') # פותח את הטבלה מקובץ אקסל ומגדיר אותה כדאטה פריים. 
    
    df2.rename(columns={'מפלס הכנרת במטרים': 'מפלס'}, inplace=True) # משנה את השם של אחד מן הטורים בטבלה לשם שקיים בטבלה השנייה

    df2['תאריך מדידה'] = pd.to_datetime(df2['תאריך מדידה'],errors='coerce') # משנה את התאריכים שמגיעים בסטרינג לדאטה טיים
    df1['תאריך מדידה'] = pd.to_datetime(df1['תאריך מדידה'],errors='coerce')
    
    df2['year'], df2['month'] = df2['תאריך מדידה'].dt.year, df2['תאריך מדידה'].dt.month # מפצל את התאריך לשתי טורים שונים אחת שנה אחד חודש
    df1['year'], df1['month'] = df1['תאריך מדידה'].dt.year, df1['תאריך מדידה'].dt.month
    
    df1.groupby("month")['מפלס'].mean().plot(kind='line',title="ים המלח"[::-1],colormap='jet', marker='.',markersize=10) # יוצר גרף לפי חודש ומפלס בשביל הגרף הראשון
    plot = render_plot()
    df2.groupby("month")['מפלס'].mean().plot(kind='line',title=str("הכנרת")[::-1],colormap='jet', marker='.',markersize=10)# יוצר גרף לפי חודש ומפלס בשביל הגרף השני
    return plot,render_plot()

    
    

def create_html_page_for_src2():
    
    df = pd.read_csv(f'{dir_path}/Src/kinneret_level.csv') # פותח את הטבלה מקובץ אקסל ומגדיר אותה כדאטה פריים. 

    
    df.rename(columns={'מפלס הכנרת במטרים': 'מפלס'}, inplace=True)

    df['מפלס'] = df['מפלס'].astype('float') # הופך את הטור מפלס לטור מסוג מספר ממשי
    avg = df['מפלס'].mean() # מחשב ממוצע של הטור
   
    df = df.head(20)

    
    s = df.style.applymap(lambda x: color_negative_red_color_positive_green(x,avg) ,subset=['מפלס'])
    Tables =s.hide_index().render()
    
    
    return Tables