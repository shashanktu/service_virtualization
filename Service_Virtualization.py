import streamlit as st
import requests
import json
from datetime import datetime
from urllib.parse import urlparse
from sql import create_wiremock_table, insert_wiremock_data

# Page config
st.set_page_config(
    page_title="Service Virtualization",
    # page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set page name for sidebar navigation
if "page_name" not in st.session_state:
    st.session_state.page_name = "Service Virtualization"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6C37;
        text-align: center;
        margin-bottom: 2rem;
    }
    .response-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .response-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .status-code {
        font-weight: bold;
        font-size: 1.2rem;
    }
    .scrollable-json {
        max-height: 300px;
        overflow-y: auto;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 10px;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header with Logo
col_logo, col_title = st.columns([1, 4])
with col_logo:
    try:
        st.image("src/ValueMomentum_logo.png", width=100)
    except:
        st.write("")
with col_title:
    st.markdown('<div class="main-header">Command Center(NPE Services Virtualization)</div>', unsafe_allow_html=True)

# Sidebar Navigation
# st.sidebar.title("Navigation")
# if st.sidebar.button("🏠 API Testing", use_container_width=True):
#     st.rerun()
# if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
#     st.switch_page("pages/Refresh_Data.py")
# if st.sidebar.button("🗑️ Remove API", use_container_width=True):
#     st.switch_page("pages/Routing_Portal.py")

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Request Configuration")
    
    # HTTP Method and URL
    method_col, url_col = st.columns([1, 4])
    with method_col:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])
    with url_col:
        url = st.text_input("Enter API URL", placeholder="https://api.example.com/endpoint")
    
    # Tabs for different configurations
    tab1, tab2, tab3, tab4,tab5 = st.tabs(["Headers", "Authorization", "Body", "Params","API Details"])
    
    with tab1:
        st.write("**Headers**")
        headers = {}
        num_headers = st.number_input("Number of headers", min_value=0, max_value=10, value=1)
        for i in range(num_headers):
            col_key, col_value = st.columns(2)
            with col_key:
                key = st.text_input(f"Header {i+1} Key", key=f"header_key_{i}")
            with col_value:
                value = st.text_input(f"Header {i+1} Value", key=f"header_value_{i}")
            if key and value:
                headers[key] = value
    
    with tab2:
        st.write("**Authorization**")
        auth_type = st.selectbox("Type", ["None", "Bearer Token", "Basic Auth", "API Key"])
        
        auth_headers = {}
        if auth_type == "Bearer Token":
            token = st.text_input("Token", type="password")
            if token:
                auth_headers["Authorization"] = f"Bearer {token}"
        elif auth_type == "Basic Auth":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if username and password:
                import base64
                credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
                auth_headers["Authorization"] = f"Basic {credentials}"
        elif auth_type == "API Key":
            key_name = st.text_input("Key Name", value="X-API-Key")
            api_key = st.text_input("API Key", type="password")
            if key_name and api_key:
                auth_headers[key_name] = api_key
    
    with tab3:
        st.write("**Request Body**")
        body_type = st.selectbox("Body Type", ["None", "JSON", "Form Data", "Raw Text"])
        
        body_data = None
        if body_type == "JSON":
            body_text = st.text_area("JSON Body", height=150, placeholder='{"key": "value"}')
            if body_text:
                try:
                    body_data = json.loads(body_text)
                    headers["Content-Type"] = "application/json"
                except json.JSONDecodeError:
                    st.error("Invalid JSON format")
        elif body_type == "Form Data":
            num_fields = st.number_input("Number of fields", min_value=0, max_value=10, value=1)
            form_data = {}
            for i in range(num_fields):
                col_key, col_value = st.columns(2)
                with col_key:
                    key = st.text_input(f"Field {i+1} Key", key=f"form_key_{i}")
                with col_value:
                    value = st.text_input(f"Field {i+1} Value", key=f"form_value_{i}")
                if key and value:
                    form_data[key] = value
            if form_data:
                body_data = form_data
        elif body_type == "Raw Text":
            body_data = st.text_area("Raw Body", height=150)
    
    with tab4:
        st.write("**Query Parameters**")
        params = {}
        num_params = st.number_input("Number of parameters", min_value=0, max_value=10, value=0)
        for i in range(num_params):
            col_key, col_value = st.columns(2)
            with col_key:
                key = st.text_input(f"Param {i+1} Key", key=f"param_key_{i}")
            with col_value:
                value = st.text_input(f"Param {i+1} Value", key=f"param_value_{i}")
            if key and value:
                params[key] = value
    with tab5:
        st.write("**API Details**")
        st.text_area("API Documentation", height=150)
        st.write("**Environment**")
        env = st.selectbox("Environment", ["Dev", "Test", "Staging", "Prod"])
        st.write("**LOB**")
        lob = st.selectbox("Line of Business", ["Policy", "Claims", "Small Business"])

with col2:
    st.subheader("Validate")
    
    # Initialize session state for storing validated response
    if 'validated_response' not in st.session_state:
        st.session_state.validated_response = None
    
    # Send button
    if st.button("Validate", type="primary", use_container_width=True):
        if not url:
            st.error("Please enter a URL")
        else:
            try:
                # Combine headers
                all_headers = {**headers, **auth_headers}
                
                # Make request
                start_time = datetime.now()
                
                if method == "GET":
                    response = requests.get(url, headers=all_headers, params=params)
                elif method == "POST":
                    if body_type == "JSON" and body_data:
                        response = requests.post(url, headers=all_headers, params=params, json=body_data)
                    else:
                        response = requests.post(url, headers=all_headers, params=params, data=body_data)
                elif method == "PUT":
                    if body_type == "JSON" and body_data:
                        response = requests.put(url, headers=all_headers, params=params, json=body_data)
                    else:
                        response = requests.put(url, headers=all_headers, params=params, data=body_data)
                elif method == "DELETE":
                    response = requests.delete(url, headers=all_headers, params=params)
                elif method == "PATCH":
                    if body_type == "JSON" and body_data:
                        response = requests.patch(url, headers=all_headers, params=params, json=body_data)
                    else:
                        response = requests.patch(url, headers=all_headers, params=params, data=body_data)
                
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds() * 1000
                
                # Store validated response for mock API
                try:
                    st.session_state.validated_response = response.text
                except:
                    st.session_state.validated_response = response.text
                
                # Display response
                status_color = "success" if 200 <= response.status_code < 300 else "error"
                
                st.markdown(f"""
                <div class="response-{status_color}">
                    <span class="status-code">Status: {response.status_code}</span>
                    <span style="float: right;">Time: {response_time:.0f}ms</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Response tabs
                resp_tab1, resp_tab2, resp_tab3 = st.tabs(["Body", "Headers", "Raw"])
                
                with resp_tab1:
                    try:
                        json_response = response.json()
                        with st.container():
                            st.markdown('<div class="scrollable-json">', unsafe_allow_html=True)
                            st.json(json_response)
                            st.markdown('</div>', unsafe_allow_html=True)
                    except:
                        st.text_area("Response", response.text, height=300)
                
                with resp_tab2:
                    with st.container():
                        st.markdown('<div class="scrollable-json">', unsafe_allow_html=True)
                        st.json(dict(response.headers))
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with resp_tab3:
                    st.text(f"Status Code: {response.status_code}")
                    st.text(f"Response Time: {response_time:.0f}ms")
                    st.text(f"Content Length: {len(response.content)} bytes")
                    st.text("Raw Response:")
                    st.code(response.text)
                
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    
    # Mock API button
    if st.button("Mock API", use_container_width=True):
        if st.session_state.validated_response is None:
            st.error("Please validate an API first to get response data for mocking")
        else:
            try:
                # Extract path from URL
                
                parsed_url = urlparse(url)
                mock_path = parsed_url.path
                if parsed_url.query:
                    mock_path += f"?{parsed_url.query}"
                
                # WireMock API call
                base_url="https://r1j4l.wiremockapi.cloud/"
                mock_url = "https://api.wiremock.cloud/v1/mock-apis/r1j4l/mappings"
                
                mock_headers = {
                    "Authorization": "Token wmcp_7l0od_a86e9838fdc8c8a48bdb0d95d3c706c9_b2437e2f",
                    "Content-Type": "application/json"
                }
                
                # Use extracted path and validated response
                payload = {
                    "request": {
                        "method": "GET",
                        "url":"/service-virtualisation"+ mock_path,
                        "basicAuth": {
                            "username": "pshmockapi",
                            "password": "mock@api123"
                        }
                    },
                    "response": {
                        "body": st.session_state.validated_response
                    }
                }
                
                start_time = datetime.now()
                response = requests.post(
                    mock_url,
                    headers=mock_headers,
                    json=payload,
                    allow_redirects=True
                )
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds() * 1000
                
                # If mock API creation was successful, store the data in database
                if 200 <= response.status_code < 300:
                    # Prepare API details as JSON
                    api_details_data = {
                        "environment": env if 'env' in locals() else "Not specified",
                        "line_of_business": lob if 'lob' in locals() else "Not specified",
                        "headers": {**headers, **auth_headers},
                        "parameters": params,
                        "body_type": body_type if 'body_type' in locals() else "None",
                        "body_data": body_data,
                        "auth_type": auth_type if 'auth_type' in locals() else "None",
                        "response_time_ms": response_time,
                        "original_response": st.session_state.validated_response,
                        "created_timestamp": datetime.now().isoformat()
                    }
                    
                    # Generate the mock endpoint URL
                    mock_endpoint_url = f"{base_url}service-virtualisation{mock_path}"
                    # print("==========================")
                    # print(response.json().get('id'))
                    # print("==========================")

                    
                    # Store in database with LOB and Environment
                    record_id = insert_wiremock_data(
                        original_url=url,
                        operation=method,
                        api_details=json.dumps(api_details_data),
                        mock_url=mock_endpoint_url,
                        wiremock_id=response.json().get('id'),
                        lob=lob if 'lob' in locals() else None,
                        environment=env if 'env' in locals() else None,
                        headers=json.dumps({**headers, **auth_headers}),
                        parameters=json.dumps(params)
                    )
                    
                    if record_id:
                        st.success(f"Mock API created and stored in database with ID: {record_id}")
                        st.info(f"Mock endpoint: {mock_endpoint_url}")
                    else:
                        st.warning("Mock API created but failed to store in database")
                
                # Display mock response
                status_color = "success" if 200 <= response.status_code < 300 else "error"
                
                st.markdown(f"""
                <div class="response-{status_color}">
                    <span class="status-code">Mock API Status: {response.status_code}</span>
                    <span style="float: right;">Time: {response_time:.0f}ms</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Mock response tabs
                mock_tab1, mock_tab2, mock_tab3 = st.tabs(["Body", "Headers", "Raw"])
                
                with mock_tab1:

                    try:
                        json_response = response.json()
                        # st.write(api_url)
                        
                        st.json(json_response)
                    except:
                        st.text(response.text)
                
                with mock_tab2:
                    st.json(dict(response.headers))
                
                with mock_tab3:
                    st.text(f"Status Code: {response.status_code}")
                    st.text(f"Response Time: {response_time:.0f}ms")
                    st.text(f"Content Length: {len(response.content)} bytes")
                    st.text("Raw Response:")
                    st.code(response.text)
                    
            except requests.exceptions.RequestException as e:
                st.error(f"Mock API request failed: {str(e)}")
            except Exception as e:
                st.error(f"Mock API error: {str(e)}")
    
    # Request preview
    st.subheader("Request Preview")
    if url:
        preview_headers = {**headers, **auth_headers}
        st.code(f"""
{method} {url}
Headers: {json.dumps(preview_headers, indent=2) if preview_headers else 'None'}
Params: {json.dumps(params, indent=2) if params else 'None'}
Body: {json.dumps(body_data, indent=2) if body_data else 'None'}
        """)
    

# Footer
st.markdown("---")
st.markdown("© 2026 ValueMomentum. All Rights Reserved.")