# 2.- Accessing the API



## 2.1.- Basic usage with curl

```
curl -X POST https://www.inspiration-q.com/api/v1/iq-finance/index-tracking -H "Content-Type: application/json" -H "Accept: application/json" -H "Ocp-Apim-Subscription-Key: <your-api-key>" -d '{
  "assets_covariance_matrix": [
    [3.571705619883564, -0.7955365555749586, 0.12557964034596986, 1.0639482728918976, -0.40191777016183283, 0.6863605725971405, -0.13949908918445247, 0.1711775516765147, 0.6755160399639315, 2.51293081246698],
    [-0.7955365555749586, 5.415520138923123, -2.0174005804761763, 0.030388266205496173, 2.550222403729447, 0.5643289518319003, -1.293304939459475, -0.5751123806041349, 3.594236909963808, 1.8956893890593007],
    [0.12557964034596986, -2.0174005804761763, 6.365322954156529, 2.257879191752247, -3.658046606965999, -0.45033274824515956, -1.0273304859751011, -0.21571777326705427, -0.3865083786928926, -1.533229084930434],
    [1.0639482728918976, 0.030388266205496173, 2.257879191752247, 3.9943121946674895, -1.78048417102389, 0.5687925714650388, -1.1084218725187323, -0.1515180112312195, -2.5176791064421384, 1.088241626988272],
    [-0.40191777016183283, 2.550222403729447, -3.658046606965999, -1.78048417102389, 8.390493238417324, 2.2223130935800453, -1.77173431354756, -1.3492997496155428, 3.448640251236081, 0.0298926428035794],
    [0.6863605725971405, 0.5643289518319003, -0.45033274824515956, 0.5687925714650388, 2.2223130935800453, 4.449214575445028, -2.713857481152314, -0.8300224805092693, -0.727328631285821, -0.3117075238989559],
    [-0.13949908918445247, -1.293304939459475, -1.0273304859751011, -1.1084218725187323, -1.77173431354756, -2.713857481152314, 4.0926798019898545, 2.3976179895459238, 0.27049000177733207, -0.29585690145164956],
    [0.1711775516765147, -0.5751123806041349, -0.21571777326705427, -0.1515180112312195, -1.3492997496155428, -0.8300224805092693, 2.3976179895459238, 3.864597206599372, -0.2604720356119854, -1.9647359528399329],
    [0.6755160399639315, 3.594236909963808, -0.3865083786928926, -2.5176791064421384, 3.448640251236081, -0.727328631285821, 0.27049000177733207, -0.2604720356119854, 9.083901928836333, 1.4490996023473937],
    [2.51293081246698, 1.8956893890593007, -1.533229084930434, 1.088241626988272, 0.0298926428035794, -0.3117075238989559, -0.29585690145164956, -1.9647359528399329, 1.4490996023473937, 5.4073509688190695]
  ],
  "index_assets_covariance_vector": [0.05177358659202069, -0.3356720686060817, 0.3206831344776768, 0.41750733093212566, 0.3313631827597856, -0.13542997653680122, -0.43400507867532734, 0.29062468284108733, 0.15880933369691574, -0.441086589088471],
  "portfolio_size": "8",
  "asset_names": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
  "randomNumberGenerator": "359133650"
}'
```


## 2.2.- A Postman collection

### Overview
In the `api` folder, we provide a **Postman collection** named **`Inspiration-Q_Index_Tracking_API.postman_collection.json`**. This collection contains predefined requests for interacting with the **Inspiration-Q Index Tracking API**.

Using this collection, you can easily test API endpoints, send requests, and review responses without manually setting up each request.

### How to Use the Postman Collection

#### 1. Install Postman
If you haven't already, download and install **Postman**:
- [Download Postman](https://www.postman.com/downloads/)

#### 2. Import the Postman Collection
Follow these steps to import the provided Postman collection:
1. Open **Postman**.
2. Click on **File** → **Import** (or use the **Import** button in the top-left corner).
3. Select **Upload Files** and browse to `api/Inspiration-Q_Index_Tracking_API.postman_collection.json`.
4. Click **Open** to import the collection.

#### 3. Configure Environment Variables
To simplify API requests, the collection uses **environment variables**. Before making requests, you need to set up these variables:

1. Click on **Environments** in Postman.
2. Create a new environment named `Inspiration-Q API`.
3. Add the following variables:
   - **baseUrl**: `https://www.inspiration-q.com/api/v1`
   - **apiKey**: `<your-API-key>` (replace with your actual API key)
4. Save the environment and select it before making requests.

#### 4. Make API Requests
Once the collection is imported and environment variables are set:
- Expand the **`Inspiration-Q Index Tracking API`** collection.
- Select an endpoint (e.g., **Create a new Index Tracking computation**).
- Click **Send** to execute the request.
- Review the API response in the Postman interface.

#### 5. Testing Different Requests
The collection includes requests for:
- **Creating an Index Tracking computation** (`POST /iq-finance/index-tracking`)
- **Retrieving a computation by ID** (`GET /iq-finance/index-tracking/{indexTrackingComputationId}`)

## 2.3.- Using Python without the SDK

This guide explains how to use the Inspiration-Q Index Tracking API in Python. The provided Python script demonstrates how to:

Create a new Index Tracking computation by sending a POST request.

Retrieve the computation results using a GET request.

Poll the API until the computation is completed.

### Prerequisites
- Python 3 installed on your system.
- The requests library installed (pip install requests).
- An API key for Inspiration-Q (replace YOUR_API_KEY in the script).

### Python script
You can find the code in the file `IndexTrackingNoSDK.py` provided inside the [Examples Folder](../examples/).

```
import requests
import time

# API Configuration
BASE_URL = "https://www.inspiration-q.com/api/v1"
API_KEY = "YOUR_API_KEY"
HEADERS = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": API_KEY
}

# Define the payload for creating an index tracking computation
payload = {
    "description": "SP500 tracker, size=60",
    "assets_covariance_matrix": [[1.23, 2.13], [3.13, 4.09]],
    "index_assets_covariance_vector": [1.31, 33.541],
    "asset_names": ["ticker_a", "ticker_b"],
    "portfolio_size": 2,
    "minimum_weight": 0.25,
    "maximum_weight": 1.0,
    "sum_of_portfolio_weights": 1.0,
    "random_number_generator_seed": 1334
}

# Step 1: Create a new Index Tracking computation
response = requests.post(f"{BASE_URL}/iq-finance/index-tracking", json=payload, headers=HEADERS)

if response.status_code == 201:
    computation_result = response.json()
    computation_id = computation_result["computationId"]
    print(f"Computation created successfully. ID: {computation_id}")
else:
    print(f"Error creating computation: {response.status_code} - {response.text}")
    exit()

# Step 2: Retrieve the computation results by ID
print("Fetching computation results...")

while True:
    response = requests.get(f"{BASE_URL}/iq-finance/index-tracking/{computation_id}", headers=HEADERS)

    if response.status_code == 200:
        result = response.json()
        print(f"Computation Status: {result['status']}")
        
        if result["status"] in ["Failed", "Ok"]:
            print("Computation complete!")
            print("Computation Details:", result)
            break
    elif response.status_code == 404:
        print("Computation not found. Retrying...")
    else:
        print(f"Error fetching computation: {response.status_code} - {response.text}")
        break

    time.sleep(5)  # Wait before retrying
```

### How It Works

#### Step 1: Create an Index Tracking Computation
- The script sends a POST request with the input data (covariance matrix, portfolio size, etc.).
- If successful, the API returns a computation ID.

#### Step 2: Poll the API for Results
- The script sends a GET request to fetch the computation status using the computation ID.
- If the status is Pending or Computing, it retries every 5 seconds.
- When the status is Ok (Completed) or Failed, it prints the computation results.

### Notes

- Replace `YOUR_API_KEY` with your actual API key.
- Adjust the payload parameters as needed for different computations.
- Increase or decrease the polling interval (time.sleep(5)) based on expected computation time.

