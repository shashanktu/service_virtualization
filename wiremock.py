import requests
from urllib.parse import urlparse
from sql import delete_record
# base_url="https://4dz7r.wiremockapi.cloud/"
# mock_url = "https://api.wiremock.cloud/v1/mock-apis/4dz7r/mappings" 
# mock_headers = {"Authorization": "Token wmcp_lw9gg_5262823d7ef3be9489fd3ddf2d7fe074_ee6671e8",
#                         "Content-Type": "application/json"
#                     } 

base_url="https://r1j4l.wiremockapi.cloud/"
mock_url = "https://api.wiremock.cloud/v1/mock-apis/r1j4l/mappings"
                
mock_headers = {
                    "Authorization": "Token wmcp_7l0od_a86e9838fdc8c8a48bdb0d95d3c706c9_b2437e2f",
                    "Content-Type": "application/json"
                }


def update_wiremock(wiremock_id, url, response):
     
    parsed_url = urlparse(url)
    mock_path = parsed_url.path
    if parsed_url.query:
                    mock_path += f"?{parsed_url.query}"   

    mock_url_path =  mock_path

    payload = {
                        "request": {
                            "method": "GET",
                            "url": mock_url_path
                        },
                        "response": {
                            "body": response
                       }
                    }

    response = requests.put(
                        f"{mock_url}/{wiremock_id}",
                        headers=mock_headers,
                        json=payload,
                        allow_redirects=True
                    )
    
    return response

def delete_wiremock_data(id):
    response=requests.delete(
    f"{mock_url}/{id}",
    headers=mock_headers
)
    
    print(response)
    if response.status_code ==200:
            status=delete_record(id)
            return status
    return False