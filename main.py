import streamlit as st
import json
import os

# Define the file path for the library JSON file
LIBRARY_FILE = "library.json"

# Load Library Function
def load_library():
    """Load library from JSON file safely."""
    if not os.path.exists(LIBRARY_FILE):
        return []  # If file doesn't exist, return empty list

    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        st.error("⚠️ Error: library.json is corrupted or empty. Please check the file.")
        return []  # Return an empty list to prevent crashes
    except FileNotFoundError:
        return []

# Save Library Function
def save_library(library):
    """Save the library data back to the JSON file."""
    with open(LIBRARY_FILE, "w", encoding="utf-8") as file:
        json.dump(library, file, indent=4)

# Initialize Library
library = load_library()

# Custom CSS Styling
st.markdown(
    """
    <style>
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
            save_library(library)  # Pass library explicitly
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
            save_library(library)  # Pass library explicitly
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
    save_library(library)
    st.success("💾 Library saved successfully! 🎉")
