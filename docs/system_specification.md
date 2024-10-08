# אפיון מערכת - מיני רשת חברתית

## תיאור כללי
מערכת רשת חברתית מינימלית המאפשרת למשתמשים להתחבר, לפרסם פוסטים, לצפות בפיד, לתת לייקים לפוסטים, להגיב לפוסטים ולצפות בפרופילים אישיים.

## תכונות עיקריות
1. כניסה פשוטה למערכת ללא צורך בסיסמה
2. יצירת פוסטים חדשים
3. צפייה בפיד של כל הפוסטים
4. מתן לייק לפוסטים
5. הוספת תגובות לפוסטים
6. צפייה בפרופיל אישי עם סטטיסטיקות ופוסטים של המשתמש
7. עיצוב מודרני ונקי באמצעות Tailwind CSS

## מודל נתונים
1. משתמש:
   - מזהה
   - שם

2. פוסט:
   - מזהה
   - תוכן
   - זמן יצירה
   - מזהה משתמש (יוצר הפוסט)
   - מספר לייקים

3. לייק:
   - מזהה
   - מזהה פוסט
   - מזהה משתמש (נותן הלייק)

4. תגובה:
   - מזהה
   - תוכן
   - זמן יצירה
   - מזהה פוסט
   - מזהה משתמש (כותב התגובה)

## User Stories
1. כמשתמש, אני רוצה להיכנס למערכת על ידי הזנת שמי או בחירתו מרשימה קיימת
2. כמשתמש, אני רוצה לראות את כל הפוסטים בפיד הראשי
3. כמשתמש, אני רוצה ליצור פוסט חדש
4. כמשתמש, אני רוצה לראות מי יצר כל פוסט
5. כמשתמש, אני רוצה לתת לייק לפוסט
6. כמשתמש, אני רוצה לראות כמה לייקים יש לכל פוסט
7. כמשתמש, אני רוצה לבטל לייק שנתתי לפוסט
8. כמשתמש, אני רוצה להגיב לפוסטים
9. כמשתמש, אני רוצה לראות את התגובות של כל פוסט
10. כמשתמש, אני רוצה לראות את פרופילי אישי של המשתמשים
11. כמשתמש, אני רוצה לראות את סטטיסטיקות הפרופיל שלי
12. כמשתמש, אני רוצה לראות את הפוסטים שלי בפרופיל אישי

## טכנולוגיות
- Flask
- SQLite
- Tailwind CSS