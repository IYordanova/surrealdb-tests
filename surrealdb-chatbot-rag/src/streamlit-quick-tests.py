# import pandas as pd
# st.write("Here's our first attempt at using data to create a table:")
# st.write(
#     pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
# )


# import numpy as np
# import pandas as pd
# import streamlit as st

# dataframe = pd.DataFrame(
#     np.random.randn(10, 20), columns=("col %d" % i for i in range(20))
# )

# st.dataframe(dataframe.style.highlight_max(axis=0))


# import numpy as np
# import pandas as pd
# import streamlit as st

# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
# )

# st.map(map_data)


# x = st.slider("x")  # 👈 this is a widget
# st.write(x, "squared is", x * x)


# import streamlit as st

# if "counter" not in st.session_state:
#     st.session_state.counter = 0

# st.session_state.counter += 1

# st.header(f"This page has run {st.session_state.counter} times.")

# # Method 1: Using the return value (True if clicked)
# if st.button("Method 1: Click to print"):
#     st.write("Button 1 was clicked!")
#     print("Button 1 clicked")


# # # Method 2: Using a callback (runs before the script reruns)
# # def handle_click():
# #     st.session_state.counter += 10
# #     st.toast("Counter incremented by 10!")


# st.button("Method 2: Click to update state")
