import streamlit as st
import random

# --- App title ---
st.set_page_config(page_title="Digital Closet", layout="wide")

# --- Global theming (single CSS block) ---
st.markdown(
    """
<style>
/* Main background + text */
.stApp { background:#FAF8F5; color:#2E2E2E; }

/* Header (top bar) gradient: longer light segment */
header[data-testid="stHeader"]{
  background:linear-gradient(90deg,#f6e6fb 0%,#f6e6fb 65%,#b392ac 85%,#6b4c98 100%) !important;
  border-bottom:0px solid #d1b3c4; height:50px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
  background:#f6e6fb; color:#6B4C98; text-align:center;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] p{
  color:#6B4C98 !important; text-align:center !important;
}

/* Buttons (sidebar + main) — mauve bg, CREAM text */
.stButton > button:first-child{
  background:#B392AC !important; border:none !important; border-radius:8px !important;
  width:100%; padding:0.6em 1em; margin:6px 0;
}
.stButton > button:first-child *{ color:#FAF8F5 !important; fill:#FAF8F5 !important; }
.stButton > button:hover{ background:#735D78 !important; }
.stButton > button:hover *{ color:#FAF8F5 !important; fill:#FAF8F5 !important; }

/* Make center container transparent so cream shows through */
.main .block-container{ background:transparent !important; }

/* Headings in main area */
h1,h2,h3,h4,h5{ color:#6B4C98; }


/* File uploader styling (optional) */
.stFileUploader{ background:#FFF1FA; border:1px solid #E0BEEB; border-radius:10px; padding:12px; }
</style>
""",
    unsafe_allow_html=True,
)


# --- Buttons on Outfit Builder and Saved Outfits page ---
st.markdown(
    """
<style>
/* Recolor Streamlit alerts (incl. st.info) to lilac with readable text */
.stAlert, div[role="alert"], div[data-baseweb="notification"] {
  background:#F7E9FD !important;
  border:1px solid #D1B3C4 !important;
  border-radius:10px !important;
  color:#6B4C98 !important;
}
.stAlert *, div[role="alert"] *, div[data-baseweb="notification"] * {
  color:#6B4C98 !important;
  fill:#6B4C98 !important;
}
</style>
""",
    unsafe_allow_html=True,
)


# --- Sidebar ---
st.sidebar.image("logo.png")
st.sidebar.title("StyleSynth")
st.sidebar.write("Your digital stylist")

if "page" not in st.session_state:
    st.session_state.page = "My Wardrobe"

# --- Sidebar buttons ---
if st.sidebar.button("My Wardrobe"):
    st.session_state.page = "My Wardrobe"
if st.sidebar.button("Outfit Builder"):
    st.session_state.page = "Outfit Builder"
if st.sidebar.button("Saved Outfits"):
    st.session_state.page = "Saved Outfits"

page = st.session_state.page

# --- Initialize session state ---
st.session_state.setdefault("uploaded_items", [])
st.session_state.setdefault("show_uploader", False)
st.session_state.setdefault("saved_outfits", [])

# --- My Wardrobe Page ---
if page == "My Wardrobe":
    st.subheader("My Wardrobe")
    st.write(f"{len(st.session_state.uploaded_items)} items")

    col_add = st.columns([5, 1])[1]
    with col_add:
        if st.button("+ Add New Item"):
            st.session_state.show_uploader = True

    if len(st.session_state.uploaded_items) == 0 and not st.session_state.show_uploader:
        st.markdown(
            """
            <div style='text-align:center; margin-top:60px;'>
                <svg width="100" height="100" fill="none" stroke="gray" stroke-width="2">
                    <rect x="30" y="30" width="40" height="40"/>
                    <path d="M50 30 L50 70" stroke="gray"/>
                </svg>
                <h2>Your Wardrobe is empty</h2>
                <p>Start building your digital closet by uploading.</p>
            </div>""",
            unsafe_allow_html=True,
        )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            "<h2 style='text-align:center; color:#B392AC;'>Add First Item Above!</h2>",
            unsafe_allow_html=True,
        )

    if st.session_state.show_uploader:
        st.markdown("---")
        st.markdown("### Add New Item")
        st.caption("Upload a photo and we'll help you catalog it")

        uploaded_file = st.file_uploader(
            "Upload a clothing item", type=["png", "jpg", "jpeg", "webp"]
        )

        if uploaded_file:
            st.image(uploaded_file, width=300)
            st.markdown("### Item Details")

            category = st.selectbox(
                "Category *", ["Casual", "Dinner", "Formal", "Party", "Everyday"]
            )
            season = st.selectbox("Season *", ["Spring", "Summer", "Fall", "Winter"])
            subcategory = st.text_input("Subcategory", placeholder="e.g., tank top")
            brand = st.text_input("Brand", placeholder="e.g., Christopher Esber")
            colors = st.text_input(
                "Colors (comma-separated)", placeholder="e.g., brown, beige"
            )
            occasions = st.multiselect(
                "Occasions",
                ["Casual", "Formal", "Business", "Athletic", "Party", "Everyday"],
            )
            seasons = st.multiselect(
                "Seasons", ["Spring", "Summer", "Fall", "Winter", "All-Season"]
            )
            notes = st.text_area(
                "Notes", placeholder="Add any personal notes about this item"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Add to Wardrobe"):
                    st.session_state.uploaded_items.append(
                        {
                            "file": uploaded_file,
                            "category": category,
                            "season": season,
                            "subcategory": subcategory,
                            "brand": brand,
                            "colors": [
                                c.strip() for c in colors.split(",") if c.strip()
                            ],
                            "occasions": occasions,
                            "seasons": seasons,
                            "notes": notes,
                        }
                    )
                    st.session_state.show_uploader = False
                    st.success(f"Added '{brand or 'New Item'}' to your wardrobe!")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.show_uploader = False
                    st.rerun()

    elif len(st.session_state.uploaded_items) > 0:
        st.markdown("### Your Items")
        cols = st.columns(4)
        for i, item in enumerate(st.session_state.uploaded_items):
            with cols[i % 4]:
                st.image(item["file"], use_container_width=True)
                st.markdown(
                    f"""
                    <div style="background:#f5f5f5; padding:10px; border-radius:10px; text-align:center;
                                box-shadow:2px 2px 5px rgba(0,0,0,0.1); font-family:Arial, sans-serif;">
                        <p style="margin:5px;"><strong>Brand:</strong> {item.get('brand','Unknown')}</p>
                        <p style="margin:5px;"><strong>Category:</strong> {item.get('category','Unknown')}</p>
                        <p style="margin:5px;"><strong>Subcategory:</strong> {item.get('subcategory','Unknown')}</p>
                    </div>""",
                    unsafe_allow_html=True,
                )

# --- Outfit Builder Page ---
elif page == "Outfit Builder":
    st.subheader("Outfit Builder")
    st.write("Mix and match your wardrobe items here.")

    if len(st.session_state.uploaded_items) == 0:
        st.info("Upload some items in 'My Wardrobe' first!")
    else:
        st.markdown("#### Select Items to Build an Outfit")

        occasion_options = ["Casual", "Dinner", "Formal", "Party", "Everyday"]
        season_options = ["Spring", "Summer", "Fall", "Winter"]

        col1, col2 = st.columns(2)
        with col1:
            occasion_choice = st.selectbox(
                "Occasion:", options=occasion_options, key="occasion"
            )
        with col2:
            season_choice = st.selectbox(
                "Season:", options=season_options, key="season"
            )

        if st.button("Generate outfits"):
            st.session_state.current_outfit = random.sample(
                st.session_state.uploaded_items,
                min(2, len(st.session_state.uploaded_items)),
            )

        if st.session_state.get("current_outfit"):
            st.markdown("### Your Generated Outfit")
            cols = st.columns(len(st.session_state.current_outfit))
            for i, item in enumerate(st.session_state.current_outfit):
                with cols[i]:
                    st.image(item["file"], use_container_width=True)
                    st.caption(
                        f"{item.get('brand','Unknown Brand')} — {item.get('subcategory','')}"
                    )

            if st.button("💾 Save This Outfit"):
                st.session_state.saved_outfits.append(
                    {
                        "occasion": occasion_choice,
                        "season": season_choice,
                        "items": st.session_state.current_outfit,
                    }
                )
                st.success("Outfit saved to your collection!")

# --- Saved Outfits Page ---
elif page == "Saved Outfits":
    st.subheader("Saved Outfits")
    if len(st.session_state.saved_outfits) == 0:
        st.info("You haven't saved any outfits yet.")
    else:
        for i, outfit in enumerate(st.session_state.saved_outfits):
            st.markdown(f"### 👗 Outfit {i+1}")
            st.write(
                f"**Occasion:** {outfit['occasion']} | **Season:** {outfit['season']}"
            )
            cols = st.columns(len(outfit["items"]))
            for j, item in enumerate(outfit["items"]):
                with cols[j]:
                    st.image(item["file"], use_container_width=True)
                    st.caption(
                        f"{item.get('brand','Unknown Brand')} — {item.get('subcategory','')}"
                    )
            st.markdown("---")
