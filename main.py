import streamlit as st
import pandas as pd

from scanner import scan
from output import count_tokens, format_token, build_symbol_table

SAMPLE = '''# Who passed, and how hard did they study?
analysis Grades
  load students from "students.csv" with (name text, score number, hours number)
  let total = count(students)
  keep students where score >= 60
  let passed = count(students)
  let avg = mean(students.score)
  show "Passed: " + passed + " of " + total
  show "Average score of passing students: " + avg
  if avg > 80 then
    show "Great class!"
  otherwise
    show "Room to improve."
  done
  sort students by score desc
  show students
  plot bar students score by name
end
'''

st.set_page_config(page_title="Sift Compiler", layout="wide")

st.title("Sift Compiler - Phase 1: Scanner")

code = st.text_area(
    "Write your Sift program",
    value=SAMPLE,
    height=350
)

if st.button("Run"):
    st.session_state["result"] = scan(code)

if "result" in st.session_state:
    tokens, errors = st.session_state["result"]

    tab_tokens, tab_problems = st.tabs(["Tokens", "Problems"])

    with tab_tokens:
        st.write(f"**Total tokens: {count_tokens(tokens)}**")

        rows = [(format_token(t), t[0], t[1], t[2]) for t in tokens]

        st.dataframe(
            pd.DataFrame(
                rows,
                columns=["Token", "Type", "Line", "Lexeme"]
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Symbol table")

        symbols = build_symbol_table(tokens)

        st.dataframe(
            pd.DataFrame(
                list(symbols.items()),
                columns=["Identifier", "First line"]
            ),
            use_container_width=True,
            hide_index=True,
        )

    with tab_problems:
        if errors:
            st.write(f"**Total lexical errors: {len(errors)}**")

            for line, message, lexeme in errors:
                st.error(f"Line {line}: {message}: {lexeme}")
        else:
            st.success("No lexical errors")
   
   
