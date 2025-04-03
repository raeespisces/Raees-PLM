import streamlit as st
import json

# Load & Save Library
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)

# Initialize Library
library = load_library()

# Custom CSS Styling
st.markdown(
    """
    <style>
    /* Customizing title */
    .main-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: white;
        background: linear-gradient(to right, #ff6a00, #ee0979);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f7f9fc;
        border-right: 3px solid #e3e4e8;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(to right, #ff6a00, #ee0979);
        color: white;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px;
        border: none;
    }
    
    .stButton button:hover {
        background: linear-gradient(to right, #ee0979, #ff6a00);
    }

    /* Table Styling */
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 10px;
        border: 1px solid #ddd;
    }
    th {
        background: #ff6a00;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">📚 Personal Library Manager</h1>', unsafe_allow_html=True)

menu = st.sidebar.radio("📌 Select an option", ["📖 View Library", "➕ Add Book", "❌ Remove Book", "🔍 Search Book", "💾 Save and Exit"])

# View Library
if menu == "📖 View Library":
    st.sidebar.write("📚 Your Library")
    if library:
        st.table(library)
    else:
        st.write("⚠️ No books in your library. Add some books!")

# Add Book
elif menu == "➕ Add Book":
    st.sidebar.write("📥 Add a New Book")
    title = st.text_input("📌 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Year", min_value=1900, max_value=2025, step=1)
    genre = st.text_input("🎭 Genre")
    read_status = st.checkbox("✅ Mark as Read")

    if st.button("📚 Add Book"):
        if title and author and genre:
            library.append({"title": title, "author": author, "year": year, "genre": genre, "read_status": read_status})
            save_library()
            st.success("✅ Book added successfully!")
            st.rerun()
        else:
            st.warning("⚠️ Please fill in all fields.")

# Remove Book
elif menu == "❌ Remove Book":
    st.sidebar.write("🗑️ Remove a Book")
    book_titles = [book["title"] for book in library]

    if book_titles:
        selected_book = st.selectbox("📌 Select a book to remove", book_titles)
        if st.button("❌ Remove Book"):
            library = [book for book in library if book["title"] != selected_book]  # Updating the library correctly
            save_library()
            st.success("🗑️ Book removed successfully!")
            st.rerun()
    else:
        st.warning("⚠️ No books in your Library. Add some books!")

# Search Book
elif menu == "🔍 Search Book":
    st.sidebar.write("🔎 Search a Book")
    search_term = st.text_input("🔠 Enter a Title or Author Name")
    if st.button("🔍 Search"):
        results = [book for book in library if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]
        if results:
            st.table(results)
        else:
            st.warning("⚠️ No book found!")

# Save and Exit
elif menu == "💾 Save and Exit":
    save_library()
    st.success("💾 Library saved successfully! 🎉")
