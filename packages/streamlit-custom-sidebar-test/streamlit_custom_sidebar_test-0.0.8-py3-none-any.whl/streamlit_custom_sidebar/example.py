# import streamlit as st
# from Streamlit_template.__init__ import CustomSidebarDefault
# from streamlit_session_browser_storage import SessionStorage
# from streamlit_local_storage import LocalStorage 
# from Streamlit_template.__init__ import myComponent

# st.set_page_config(layout="wide")
# sidebar_template_ = CustomSidebarDefault()

# # data_ = [
# #             {"index":0, "label":"Example", "page":"example", "href":"http://localhost:8501/"},
# #             {"index":1, "label":"Page", "page":"page", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
# #         ]

# data_ = [
#             {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "href":"http://localhost:8501/"},
#             {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
#         ]

# if "currentPage" not in st.session_state: # required as component will be looking for this in session state to change page via `switch_page`
#     st.session_state["currentPage"] = data_[0] 
# else:
#     st.session_state["currentPage"] = data_[0] 


# with st.container(height=1, border=False):
#     st.html(
#         """
#             <div className="sidebar-container-init"></div>
#             <style>
#                 div[height='1']{
#                     display:none;
#                 }
#             </style>
#         """
#     )
#     defaultSidebar = CustomSidebarDefault(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local") 
#     defaultSidebar.load_custom_sidebar()
#     # defaultSidebar.change_page()

# st.write("Hiiii")

# if "clickedPage" not in st.session_state:
#     st.session_state["clickedPage"] = None 
    
# value = myComponent(default="example") #my_input_value="hello there")
# st.write("Received", value)


# # sessionS = LocalStorage(key="session_storage_init_2")
# # # sessionS.refreshItems()
# # # pageSelect = sessionS.getItem(itemKey="currentPage") 
# # pageClicked = sessionS.getItem(itemKey="clickedPage") 
# # st.write("clickedPage", pageClicked) 
# # sessionS.refreshItems()

# # st.write(st.session_state["session_storage_init_2"]) 


# # st.button("Click me")


# # if pageClicked != None and pageClicked != st.session_state["clickedPage"]:
# # st.write("previousPage", st.session_state["clickedPage"])
# # pageClicked = sessionS.getItem(itemKey="clickedPage") 
# # st.session_state["clickedPage"] = pageClicked
# # st.write( "clickedPage",pageClicked )



# # st.write("current_page", pageSelect)
# # st.write("clicked_page", pageClicked)

# # keyValList = [pageClicked]
# # expectedResult = [d for d in data_ if d['page_name'] in keyValList]
# # st.write(expectedResult)


import streamlit as st
from st_screen_stats import ScreenData, StreamlitNativeWidgetScreen, WindowQuerySize, WindowQueryHelper
from streamlit_custom_sidebar import Streamlit_template

data_ = [
            {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "href":"http://localhost:8501/"},
            {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
        ]

if "currentPage" not in st.session_state: # required as component will be looking for this in session state to change page via `switch_page`
    st.session_state["currentPage"] = data_[0] 
else:
    st.session_state["currentPage"] = data_[0] 


with st.container(height=1, border=False):
    st.html(
        """
            <div className="sidebar-container-init"></div>
            <style>
                div[height='1']{
                    display:none;
                }
            </style>
        """
    )
    defaultSidebar = Streamlit_template.CustomSidebarDefault(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local") 
    defaultSidebar.load_custom_sidebar()
    # defaultSidebar.change_page()

value_ = Streamlit_template.myComponent()
st.write(value_)