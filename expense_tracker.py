import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

if 'expences' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

def add_expense(date, category, amount, description):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)

def load_expenses():
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        st.session_state.expenses = pd.read_csv(uploaded_file, parse_dates=['Date'])
        st.success("Expenses loaded successfully!")

def download_expenses():
    if not st.session_state.expenses.empty:

        csv = st.session_state.expenses.to_csv(index=False)
        st.download_button(label="Download Expenses CSV", data=csv, file_name="expenses.csv", mime="text/csv")
    
    else:
        st.warning("No expenses available to download.")

def visualize_expenses():
    if not st.session_state.expenses.empty:
        fig, ax = plt.subplots()
        sns.barplot(x='Category', y='Amount', data=st.session_state.expenses, estimator=sum, ci=None, ax=ax)
        plt.xticks(rotation=45)
        plt.title('Total Expenses by Category')
        plt.ylabel('Total Amount')
        plt.xlabel('Category')
        st.pyplot(fig)

    else:
        st.warning("No expenses to visualize. Please add some expenses first.")



st.title("Devanshi's Expense Tracker")
with st.sidebar:
    st.header("Add New Expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Clothing", "Groceries","Other"])
    amount = st.number_input("Amount", min_value=0.0, step=10.0, format="%.2f")
    description = st.text_input("Description")

    if st.button("Add Expense"):
        add_expense(date, category, amount, description)
        st.success("Expense added successfully!")

    st.header("File Operations")
    if st.button("Download Expenses"):
        download_expenses()
    if st.button("Load Expenses"):
        load_expenses()
st.header("Expense")
st.write(st.session_state.expenses)

st.header("Expense visualization summary")
if st.button("Visualize Expenses"):
    visualize_expenses()    

