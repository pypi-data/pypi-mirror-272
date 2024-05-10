import streamlit as st
from streamlit_custom_sidebar import Streamlit_template
# from Streamlit_template.__init__ import CustomSidebarDefault
# from streamlit_session_browser_storage import SessionStorage
# from streamlit_local_storage import LocalStorage 
# from Streamlit_template.__init__ import myComponent

st.set_page_config(layout="wide")
# sidebar_template_ = CustomSidebarDefault()


data_ = [
            {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "href":"http://localhost:8501/"},
            {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
        ]

defaultSidebar = Streamlit_template.CustomSidebarDefault(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local") 
defaultSidebar.load_custom_sidebar()


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


# import streamlit as st
# # from st_screen_stats import ScreenData, StreamlitNativeWidgetScreen, WindowQuerySize, WindowQueryHelper
# # from streamlit_custom_sidebar import Streamlit_template
# # from Streamlit_template.__init__ import CustomSidebarDefault
# # from profile_sidebar.__init__ import CustomSidebarProfile  
# from slim_expand_sidebar.__init__ import CustomSidebarProfile, SidebarIcons
# # from javascript_listener import javascript_listener_frontend

# st.set_page_config(layout="wide")

# # data_ = [
# #             {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "href":"http://localhost:8501/"},
# #             {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
# #         ]

# # if "currentPage" not in st.session_state: # required as component will be looking for this in session state to change page via `switch_page`
# #     st.session_state["currentPage"] = data_[0] 
# # else:
# #     st.session_state["currentPage"] = data_[0] 


# # with st.container(height=1, border=False):
# #     st.html(
# #         """
# #             <div className="sidebar-container-init"></div>
# #             <style>
# #                 div[height='1']{
# #                     display:none;
# #                 }
# #             </style>
# #         """
# #     )
# #     webMedium = "local"
# #     defaultSidebar = CustomSidebarDefault(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local")
# #     defaultSidebar.load_custom_sidebar()
# #     # clicked_value_ = defaultSidebar.clicked_page(key="testing_222")
# #     clicked_value_ = javascript_listener_frontend(initialValue=None, default="example", listenerClassPatter=".custom-sidebar > .navigation-container > .navigation > .label-icon-container > .contents-container > .navigation-label") #".custom-sidebar > .all-navigation-options .label-icon-container > .navigation-label") # #active-element > .navigation-label > .navigation-label
    
# # st.write(clicked_value_)
# # # # st.write(st.session_state["currentPageClicked"])

# # if "previousPage" not in st.session_state:
# #     st.session_state["previousPage"] = "example"
# # else:
# #     st.session_state["previousPage"] = "example"

# # if "currentPage" not in st.session_state:
# #     st.session_state["currentPage"] = value_
# # else:
# #     st.session_state["currentPage"] = value_

# # st.write(st.session_state["currentPage"], st.session_state["previousPage"])







# # # with st.container(height=1, border=False):
# # #     st.html(
# # #         """
# # #             <div className="sidebar-container-init"></div>
# # #             <style>
# # #                 div[height='1']{
# # #                     display:none;
# # #                 }
# # #             </style>
# # #         """
# # #     )
# # #     defaultSidebar = CustomSidebarProfile(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local")
# # #     defaultSidebar.sidebarCreate() 

# #     # defaultSidebar.load_custom_sidebar()
# #     # value_ = defaultSidebar.clicked_page(key="testing_222")

# emojis_load = SidebarIcons(None)
# emojis_load.Load_All_CDNs()

# # # if self.webMedium == "local":
# # #     emojis_load.Load_All_CDNs()
# # # elif self.webMedium == "streamlit-cloud":
# # #     emojis_load.Load_All_CDNs_to_streamlit_cloud()
# # # elif self.webMedium == "custom":
# # #     emojis_load.custom_query_for_my_app_head_tag_CDN()


#     st.html(
#         '''
#             <style>

#                 .all-navigation-options {
#                     display: flex;
#                     flex-direction: column;
#                     justify-content: space-between;
#                     height: 70vh;
#                 }

#                 .label-icon-container{
#                     overflow:hidden;
#                     cursor: pointer;
#                     border-radius: 4px;
#                     cursor: pointer;
#                     display:flex;
#                     align-items: center;
#                     padding: 12px;
#                     width:100%;
#                     height:49px;
#                 }

#                 #active-element{
#                     overflow:hidden;
#                     background-color:white !important;
#                     border-radius: 4px;
#                     cursor: pointer;
#                     display: flex;
#                     align-items: center;
#                     padding: 12px;
#                     width: 100%;
#                     height: 49px;
#                 }

#                 #active-element > #sidebar-element-icons {
#                     color: black !important;                    
#                 }

#                 #active-element > .navigation-label{
#                     color: black !important;                    
#                 }

#                 .navigation-label{
#                     margin-left:30px;
#                 }

#                 .label-icon-container:hover {
#                     background-color: white;                    
#                 }

#                 .label-icon-container:hover > #sidebar-element-icons {
#                     color: black !important;                    
#                 }

#                 .label-icon-container:hover > .navigation-label {
#                     color: black !important;                    
#                 }

#                 .custom-sidebar{
#                     transition: 0.5s ease;
#                     position: relative;
#                     cursor:pointer;
#                 }

#                 .custom-sidebar:hover{
#                     width: 300px !important;
#                 } 

#             </style>
#         '''
#     )



# with st.container(height=1, border=False):
#     st.html(
#         '''
#             <style>
#                 div[height='1']{
#                     display:none;
#                 }
#             </style>
#         '''
#     )
#     test_sidebar_ = CustomSidebarProfile(base_data=base_data_, data=data_)
#     test_sidebar_.load_custom_sidebar()
#     # test_sidebar_.sidebarCreate()
#     # test_sidebar_.active_navigation()
#     # clicked_value_ = javascript_listener_frontend(initialValue=None, default="example", listenerClassPatter=".navigation-label") #".custom-sidebar > .all-navigation-options .label-icon-container > .navigation-label") # #active-element > .navigation-label > .navigation-label

# st.write("**Hey man**") 
# # st.write(clicked_value_) 

# import streamlit as st
# from streamlit_custom_sidebar import slim_expand_sidebar
# from slim_expand_sidebar.__init__ import HoverExpandSidebarTemplate, SidebarIcons

# st.set_page_config(layout="wide")


# if "clicked_page_" not in st.session_state:
#     st.session_state["clicked_page_"] = None

# current_page = "example"

# emojis_load = slim_expand_sidebar.SidebarIcons(None)
# emojis_load.Load_All_CDNs()

# data_ = [
#             {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/"},
#             {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
#         ]

# base_data_ = [
#     {"index":0, "label":"Settings", "page_name":"settings", "page_name_programmed":"None", "icon":"settings", "iconLib":"Google"},
#     {"index":1, "label":"Logout", "page_name":"logout", "page_name_programmed":"None", "icon":"ri-logout-box-r-line", "iconLib":""}
# ]

# test_sidebar_ = HoverExpandSidebarTemplate(base_data=base_data_, data=data_, logoText="Optum Gamer", logoTextSize="20px")
# test_sidebar_.load_custom_sidebar()

# st.write("**Sup Bro**")
# st.write("**Hey Man, Bro**")

