import streamlit as st
import json
import requests
from datetime import date


st.set_page_config(page_title="Repos Explorer App")
st.subheader('Repos Explorer App :sunglasses:', divider='rainbow')

col1, col2 = st.columns([3,5])

with col1:
    # taking input
    top_results = st.radio(
        "How many repos do you want to see? 10 or 50 or 100?",
        ["10", "50", "100"],
        captions = ["The top 10 Repos", "The top 50 Repos", "The top 100 Repos"])

    st.write("You selected:", top_results)

    on = st.toggle('Activate Language filter')


    if on:
        programming_language = st.radio(
        "Which language do you want to choose?",
        ["javascript", "python", "go", "java", "kotlin", "php"],
        index=None)

        st.write("You selected:", programming_language)
    else:
        programming_language = None

    on = st.toggle('Activate date filter')

    if on:
        created = st.date_input("From which date do you want to see the repos onwards ", date(2019, 1, 10))
        st.write('From the given date:', created)
    else:
        created = None

    sort = st.radio(
    "Which sort criterion do you want to choose?",
    ["stars", "forks", "help-wanted-issues", "updated"])

    st.write("You selected:", sort)

    order = st.radio(
    "Which order do you want to choose?",
    ["desc", "asc"],
    index=None)

    st.write("You selected:", order)

    inputs = {"top_results": top_results, "programming_language": programming_language, "created": created, "sort": sort, "order": order}

    if st.button('Search!'):
        res = requests.post(url = "http://backend:8000/search", data = json.dumps(inputs, default=str))
    else:
        res = None

with col2:
   if res is not None:
        if(res.status_code == 200):
            st.write(res.json())
        else:
            st.write("Choose at least one filter!")








    