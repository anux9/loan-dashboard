import streamlit as st
import pandas as pd

# قراءة البيانات
df = pd.read_csv("loan_clean.csv")

# عنوان التطبيق
st.title("Loan Dashboard")
st.write("Interactive dashboard for loan data analysis")

# عرض البيانات
st.write(df.head())

# فلتر المنطقة
areas = df["Property_Area"].unique()

selected_area = st.sidebar.multiselect(
    "Choose Property Area",
    areas )

# فلتر التعليم
education = df["Education"].unique()

selected_education = st.sidebar.radio(
    "Education",
    education )

# فلتر الدخل
max_income = st.sidebar.slider(
    "Maximum Applicant Income",
    0,
    int(df["ApplicantIncome"].max()),
    int(df["ApplicantIncome"].max()) )

# تطبيق الفلاتر
filtered_df = df.copy()

if len(selected_area) > 0:
    filtered_df = filtered_df[filtered_df["Property_Area"].isin(selected_area)]

filtered_df = filtered_df[filtered_df["Education"] == selected_education]

filtered_df = filtered_df[filtered_df["ApplicantIncome"] <= max_income]

st.write("Filtered Data")
st.write(filtered_df.head())

# الأرقام الرئيسية
if len(filtered_df) > 0:

    total_loans = len(filtered_df)

    approval_rate = (filtered_df["Loan_Status"] == 1).mean() * 100

    average_loan = filtered_df["LoanAmount"].median()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Applications", total_loans)
    col2.metric("Approval Rate", f"{approval_rate:.1f}%")
    col3.metric("Median Loan Amount", f"{average_loan:.1f}")

    # الرسوم البيانية
import seaborn as sns
import matplotlib.pyplot as plt

# رسم يوضح عدد طلبات القروض في كل منطقة
# يساعدنا على معرفة المنطقة التي لديها أكبر عدد من الطلبات

col1, col2 = st.columns(2)

with col1:
    st.subheader("Applications by Area")

    fig, ax = plt.subplots()

    sns.countplot(data=filtered_df, x="Property_Area", ax=ax)

    st.pyplot(fig)

# نلاحظ من الرسم أن منطقة Semiurban  لديها أكبر عدد من الطلبات


# رسم يوضح نسبة الموافقة على القروض في كل منطقة
# يساعدنا على مقارنة المناطق ومعرفة أي منطقة لديها نسبة موافقة أعلى

with col2:
    st.subheader("Approval Rate by Area")

    fig, ax = plt.subplots()

    sns.barplot(
        data=filtered_df,
        x="Property_Area",
        y="Loan_Status",
        ax=ax
    )

    st.pyplot(fig)

# بما أن الموافقة ممثلة بالرقم 1 والرفض بالرقم 0،
# فإن الرسم يوضح متوسط الموافقة في كل منطقة

# وش الفرق بين الرسمتين؟
# - الرسم الأول countplot: يحسب عدد الطلبات في كل منطقة
# - الرسم الثاني barplot: يقارن متوسط نسبة الموافقة بين المناطق

# selectbox

# السماح للمستخدم باختيار عمود رقمي لعرض توزيعه
numeric_columns = filtered_df.select_dtypes(include="number").columns

selected_column = st.selectbox(
    "Choose a numerical column",
    numeric_columns
)

# رسم توزيع العمود الذي اختاره المستخدم
fig, ax = plt.subplots()

sns.histplot(data=filtered_df, x=selected_column, ax=ax)

st.pyplot(fig)

# جدول البيانات (Expander)

# عرض البيانات المفلترة داخل قسم قابل للفتح
with st.expander("Show Filtered Data"):
    st.write(filtered_df)

    # حالة خاصة: لو الفلاتر لم تعطي نتائج

    # التأكد من وجود بيانات بعد تطبيق الفلاتر
if len(filtered_df) == 0:
    st.warning("No data found. Please change the filters.")
    st.stop()