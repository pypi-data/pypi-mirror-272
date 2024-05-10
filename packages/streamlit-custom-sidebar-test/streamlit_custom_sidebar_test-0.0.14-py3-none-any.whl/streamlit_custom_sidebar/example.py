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

# def sidebarCreate():

#     loadPageName = "None"

    
#     js_el = f'''
                                
#                 <script>
                    
#                     const sidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
#                     if (sidebar.length < 1){{
                        
#                         const createEL = window.top.document.createElement("section");
#                         createEL.className = 'custom-sidebar';

#                         createEL.style = "position:relative; padding: 1rem .8rem; width: 70px; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:black; z-index:999991";
#                         const body = window.top.document.body.querySelectorAll('div[data-testid="stAppViewContainer"] > section[class*="main"]'); 
#                         body[0].insertAdjacentElement('beforebegin',createEL);

#                         const newSidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
#                         const logoImgContainer = document.createElement("div");    
#                         logoImgContainer.style = 'width:fit-content; height:50px; display:flex; justify-content:center;';

#                         const logoImg = document.createElement("img");
#                         logoImg.src = 'https://lh3.googleusercontent.com/3bXLbllNTRoiTCBdkybd1YzqVWWDRrRwJNkVRZ3mcf7rlydWfR13qJlCSxJRO8kPe304nw1jQ_B0niDo56gPgoGx6x_ZOjtVOK6UGIr3kshpmTq46pvFObfJ2K0wzoqk36MWWSnh0y9PzgE7PVSRz6Y';
#                         logoImg.setAttribute("width", "50px");
#                         logoImg.setAttribute("height", "50px");  

#                         logoImgContainer.appendChild(logoImg); 
#                         newSidebar[0].appendChild(logoImgContainer); 

#                         const lineDivy = document.createElement('div');
#                         const line = document.createElement('hr');
#                         line.style = "border-top: 0.2px solid #bbb;";
#                         lineDivy.appendChild(line);
#                         newSidebar[0].appendChild(lineDivy);

#                         const allNavigation = document.createElement("div");
#                         allNavigation.className = "all-navigation-options";

#                         const navigationTabsContainer = document.createElement('ul');
#                         navigationTabsContainer.className = "navigation-selections-container";
#                         navigationTabsContainer.style = 'list-style-type:none; padding-left:0px; display:flex; flex-direction:column; width:100%; row-gap:15px;';  

#                         var pageName_ = window.top.document.location.pathname.split("/");  
#                         var pageName_ = pageName_[pageName_.length - 1];   

#                         if (pageName_ == ""){{
#                             pageName_ = {data_}[0]["page_name"];
#                         }}                        

#                         {data_}.forEach((el) => {{
#                             const createListEl = document.createElement('li');
#                             createListEl.className = "label-icon-container";  

#                             if ("{loadPageName}" === "None"){{
                                                                           
#                                 if (el.page_name === pageName_){{
#                                     createListEl.id = "active-element";                 
                                    
#                                 }} 
                            
#                             }} else {{
                                
#                                 if (el.page_name === "{loadPageName}"){{
#                                     createListEl.id = "active-element";                                                                  
                                    
#                                 }} 

#                             }}

#                             if (el.icon && el.iconLib !== "Google"){{
#                                 const iconEl = document.createElement('i');
#                                 iconEl.className = el.icon;
#                                 iconEl.id = 'sidebar-element-icons';
#                                 iconEl.style.fontSize = "22px";
#                                 iconEl.style.color = "white";
#                                 createListEl.appendChild(iconEl);
#                             }} else if (el.icon && el.iconLib === "Google"){{
#                                 const iconEl = document.createElement('i');
#                                 iconEl.className = 'material-symbols-outlined';
#                                 iconEl.id = 'sidebar-element-icons';
#                                 iconEl.innerText = el.icon;
#                                 iconEl.style.fontSize = "22px";
#                                 iconEl.style.color = "white";
#                                 createListEl.appendChild(iconEl);
#                             }}

#                             const labelEl = document.createElement('div');
#                             labelEl.className = "navigation-label";
#                             labelEl.dataset.testid = el.page_name;
#                             labelEl.innerHTML = el.label;
#                             labelEl.style = "white-space:nowrap; display:table-cell; color:white;";
#                             createListEl.appendChild(labelEl);
                                
#                             navigationTabsContainer.appendChild(createListEl);

#                         }})
#                         allNavigation.appendChild(navigationTabsContainer);
#                         newSidebar[0].appendChild(allNavigation);

#                         const logoutBtnContainer = document.createElement("div");
#                         logoutBtnContainer.className = "navigation-selections-container";
#                         logoutBtnContainer.style = 'display:flex; flex-direction:column; align-items:center; width:100%; row-gap:15px;';

#                         {base_data_}.length > 0 && {base_data_}.forEach((el) => {{ 
                        
#                             const baseContainer = document.createElement("div");
#                             baseContainer.className = "label-icon-container";

#                             const baseContainerIcon = document.createElement("i");
#                             const baseContainerLabel = document.createElement("div");
#                             if (el.icon && el.iconLib !== "Google"){{
                                
#                                 baseContainerIcon.className = el.icon;
#                                 baseContainerIcon.id = 'sidebar-element-icons';
#                                 baseContainerIcon.style.fontSize = "25px";
#                                 baseContainerIcon.style.color = "white";
#                                 baseContainerIcon.style.cursor= "pointer"; 
#                                 baseContainer.appendChild(baseContainerIcon);
    

#                             }} else if (el.icon && el.iconLib === "Google"){{
                            
#                                 baseContainerIcon.className = 'material-symbols-outlined';
#                                 baseContainerIcon.id = 'sidebar-element-icons';
#                                 baseContainerIcon.innerText = el.icon;
#                                 baseContainerIcon.style.fontSize = "25px";
#                                 baseContainerIcon.style.color = "white";
#                                 baseContainerIcon.style.cursor= "pointer"; 
#                                 baseContainer.appendChild(baseContainerIcon);
                                
#                             }}

#                             baseContainerLabel.className = "navigation-label";  
#                             baseContainerLabel.style = "white-space:nowrap; display:table-cell; color:white;";
#                             baseContainerLabel.innerText = el.label;
#                             baseContainerLabel.dataset.testid = el.page_name;
#                             baseContainer.appendChild(baseContainerLabel);

#                             logoutBtnContainer.appendChild(baseContainer);

#                         }})

#                         allNavigation.appendChild(logoutBtnContainer); 
#                         newSidebar[0].appendChild(allNavigation);    

                        
#                     }}
                
#                 </script> 

#             '''
#     st.components.v1.html(js_el, height=0, width=0) 

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

# def active_navigation():
#     """
#         Configures the active navigation tabs - adds `active-element` id if tab is clicked, removes active style to tab clicked off and sets active style to newly clicked tab.
#     """

#     js_el = f'''
                
#                 <script>
#                     var navigationTabs = window.top.document.querySelectorAll(".custom-sidebar > .all-navigation-options .label-icon-container"); 
#                     navigationTabs.forEach((c) => {{
#                         c.addEventListener("click", (e) => {{
                            
#                             window.top.document.querySelectorAll('#active-element')[0]?.removeAttribute('style');
#                             window.top.document.querySelectorAll('#active-element')[0]?.removeAttribute('id'); 
#                             c.id = "active-element";

#                         }});
#                     }});

#                     let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="navigationTabs"]');
#                     iframeScreenComp[0].parentNode.style.display = "none";
                    
#                 </script>

#             '''
#     st.components.v1.html(js_el, height=0, width=0)



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

import streamlit as st
from streamlit_custom_sidebar import slim_expand_sidebar
from slim_expand_sidebar.__init__ import HoverExpandSidebarTemplate, SidebarIcons

st.set_page_config(layout="wide")

emojis_load = SidebarIcons(None)
emojis_load.Load_All_CDNs()

data_ = [
            {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/"},
            # {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
        ]

base_data_ = [
    {"index":0, "label":"Settings", "page_name":"settings", "page_name_programmed":"None", "icon":"settings", "iconLib":"Google"},
    {"index":1, "label":"Logout", "page_name":"logout", "page_name_programmed":"None", "icon":"ri-logout-box-r-line", "iconLib":""}
]

with st.container(height=1, border=False):
    st.html(
        '''
            <style>
                div[height='1']{
                    display:none;
                }
            </style>
        '''
    )
    test_sidebar_ = HoverExpandSidebarTemplate(base_data=base_data_, data=data_, logoText="Optum Gamer", logoTextSize="20px")
    test_sidebar_.load_custom_sidebar()
    clicked_value_ = test_sidebar_.clicked_page(key="testing_222")

st.write(clicked_value_)


st.html("""
    <style>
        @media (max-width: 1023px){
            .sidebar-section{
                width: 300px !important;
                transform: translateX(0px) !important;
                transition: transform 300ms ease 0s, width 100ms ease 0s !important;
            }
        
            .sidebar-section.sidebar-closed{
                width: 0px !important;
                padding: 0px !important;
                transform: translateX(-310px) !important;
                margin-left: -10px !important;
                transition: transform 300ms ease 0s, width 300ms ease 0s, margin-left 300ms ease 0s !important;
            }
        
            .close-sidebar-btn-container{
                visibility:visible !important;
            }
        }
    </style>
""")


# js_el_ = '''
#             <script>
#                 function changeClassNameForSidebar (event) {

#                     console.log("Hii")

#                     const sidebarSection = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[id="sidebar-closed"]');
#                     console.log("neutral closed", sidebarSection)
#                     const sidebarSectionOpen = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');
#                     console.log("neutral open", sidebarSectionOpen)

#                     if (sidebarSection.length === 0){
#                         sidebarSectionOpen[0].id = "sidebar-closed";
#                     }

            
#                     event.preventDefault();
#                 }

#                 const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"]');
#                 sidebarSectionCloseBtn[0].addEventListener('click', changeClassNameForSidebar);    
#             </script> 

# '''

js_el_ = '''
                    <script>
                        function changeClassNameForSidebar (event) {
                            
                            const sidebarSectionOpen = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');
                            console.log(sidebarSectionOpen) 

                            if (sidebarSectionOpen.length > 0){
                                sidebarSectionOpen[0].className = "sidebar-section sidebar-closed"
                            } else {
                                const sidebarSectionClosed = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section sidebar-closed"]');
                                sidebarSectionClosed[0].className = "sidebar-section"
                            }
                    
                            
                            event.preventDefault();
                        }

                        const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"]');
                        sidebarSectionCloseBtn[0].addEventListener('click', changeClassNameForSidebar);    
                    </script> 

                    '''
# st.components.v1.html(js_el_, height=0, width=0) 
