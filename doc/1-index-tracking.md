# 1.- Index Tracking

## 1.1.- The index tracking problem

The index tracking problem consists on selecting a portfolio of $k$ assets from a benchmark index such that the returns of the portfolio track the returns of the index as close as possible. This closeness of the returns during a specific time window is measured by the tracking error, defined as the standard deviation of the difference between the returns of the index and the portfolio 

$$
\mathrm{TE}^2 = \textrm{Var}\left[r_I(t) - r_p(t)\right],
$$

with $r_I(t),r_p(t)$ the returns of the index and the portfolio, respectively, during the time window. 

We define a tracker portfolio by a vector of weights $\vec{\omega}$, whose elements $\omega_i$ define the allocation weight of asset $i$ inside the portfolio. Using this notation, the TE is written as

$$\textrm{TE}^2 = \sigma_I^2 - 2\, \vec{\omega}\,\vec{g} + \vec{\omega}\,\sigma\,\vec{\omega},$$

with $\sigma_I^2$ the variance of the index' returns, $\vec{g}$ the vector of covariance between the assets' and index returns, and $\sigma$ the covariance matrix of the assets' returns.

In general, a portfolio manager must satisfy some restrictions when building a tracker portfolio and at the same time the manager should try to reduce the transaction costs. In iQ-Finance we provide a series of constraints that apply both restrictions:

1. Constraints that reduce the transaction costs: these constraints aim to reduce the transaction costs when we rebalance a portfolio. They use a previous portfolio - `previous_portfolio` in the API - from which they define two rotation constraints

    * Ticker rotation: the number of assets that leaves the portfolio at one rebalance. It can be set to be below a maximum number, which is defined as `max_companies_rotation` in the API.

    * Turnover rotation: the weight of the assets that is sold from the portfolio at one rebalance. It can be set to be below a maximum number, which is defined as `max_sales_rotation` in the API. Its mathematical definition is 
    
    
    $$
        \frac{1}{2}\sum_i |w_i(t) - w_i(t-1)| \leq max\ sales\ rotation.
    $$

2. Constraints that define the weight allocation: the `maximum_weight` and `minimum_weight` constraints define the maximum and minimum allocation weight of an asset inside the tracker portfolio, respectively. These are given as 0 to 1 numbers. E.g. a 8% weight is given as 0.08.

## 1.2.- Index Tracking API

The **Inspiration-Q Index Tracking API** provides endpoints to create and track index computation processes for portfolio management. It allows users to define a financial index tracking computation, monitor its progress, and retrieve results upon completion.

It is exposed in the following URL:

```
https://www.inspiration-q.com/api/v1/iq-finance/index-tracking
```

A full explanation of the usage of the API can be found in **[Accessing the API](doc/2-accessing-the-api.md)**. Besides that, here you can find an explanation of the data that the API needs: the input and the output obtained.

### An overview of the input and the output

The Index Tracking API is designed to construct an optimal portfolio that closely replicates the performance of a given index while adhering to various constraints and optimization criteria. This API enables users to provide detailed input parameters, including asset covariance data, portfolio constraints, and sectorial restrictions, to generate an optimized portfolio composition.

The computation process involves solving a mathematical optimization problem that minimizes the tracking error between the constructed portfolio and the target index. Once a request is submitted, the API returns a structured response detailing the computation's status, results, and associated metadata.

The API accepts a structured set of input parameters that define the characteristics and constraints of the portfolio optimization problem. 

#### Input parameters of an Index Tracking computation: IndexTracking
| Field name | Type | Description |
|--------|------|-------------|
| description | string | A brief description of the portfolio. |
| assets_covariance_matrix | array | Covariance matrix of assets. |
| index_assets_covariance_vector | array | Covariance vector between assets and index. |
| asset_names | array | Names or identifiers of assets. |
| portfolio_size | integer | Number of assets in the portfolio (1-2047). |
| minimum_weight | number (optional) | Minimum weight for each asset (default: 0). |
| maximum_weight | number (optional) | Maximum weight for each asset (default: 1). |
| linear_constraints_matrix | array (optional) | Linear constraints matrix. |
| lower_bounds_vector | array (optional) | Lower bounds for constraints. |
| upper_bounds_vector | array (optional) | Upper bounds for constraints. |
| previous_portfolio | object (optional) | Asset-weight map for previous portfolio. |
| max_companies_rotation | integer (optional) | Max assets changing from previous portfolio. |
| max_sales_rotation | number (optional) | Max sell percentage from previous portfolio. |
| sectorial_weights | object (optional) | Sector-weight distribution for portfolio. |
| sectorial_distribution | object (optional) | Asset-to-sector mapping. |
| sectorial_weight_tolerance | number (optional) | Maximum deviation from sectorial weights. |
| sum_of_portfolio_weights | number (optional) | Expected sum of output weights. |
| random_number_generator_seed | integer (optional) | Seed for random number generator. |

#### Output parameters: ComputationResult
Upon submitting an optimization request, the API returns a response containing details about the computation's execution and results

| Field | Type | Description |
|--------|------|-------------|
| computationId | string | Identifier of the computation. |
| type | string | Type of computation launched. |
| description | string | Description of the computation use case. |
| status | string | Computation status: Pending, Computing, Failed, Ok. |
| progress | integer | Progress percentage of the computation. |
| computationTime | number | Time spent in computation (seconds). |
| computationStartTime | string (date-time) | Start time of computation. |
| computationStoreTime | string (date-time) | Time when computation was stored. |
| solution | array (number) | Optimal solution found. |
| named_solution | object | Solution mapped to identifiers. |
| info | number | Algorithm status code. 0 = No issues. |
| cost | number (optional) | Minimum value of cost function. |
| weights | array (number) (optional) | Weights of the solution. |

#### The first output: the Index Tracking is being computed
After submitting a request with the specified input parameters, the Index Tracking API begins processing the optimization. The API responds immediately with an initial response containing a computation ID and a status indicating that the computation is in progress.

Upon successful submission, the API returns a response similar to the following:

```
{
    "computationId": "f03efc3c-cd8f-4341-a84e-000caa380f89",
    "status": "Computing",
    "computationTimeInSeconds": 63876256052.5542,
    "computationStartTimeUtc": "0001-01-01T00:00:00"
}
```

This response confirms that the computation has started and provides a unique identifier (**computationId**) that can be used to track progress. The status field will be `Computing` until the optimization is completed.

#### The results of the Index Tracking computation

Once the computation finishes, a request using the computationId will return the final results, including the optimized portfolio weights:

```
{
    "computationId": "f03efc3c-cd8f-4341-a84e-000caa380f89",
    "status": "Ok",
    "computationTimeInSeconds": 6.04132682457566,
    "computationStartTimeUtc": "2025-02-27T12:27:34",
    "computationEndTimeUtc": "2025-02-27T12:27:40",
    "computationStoreTimeUtc": "2025-02-27T12:27:25.013",
    "named_solution": {
        "a": 0.07245113723813226,
        "b": 0.0,
        "c": 0.18209735393732956,
        "d": 0.1715528469182913,
        "e": 0.2063531488919239,
        "f": 0.025268033179531774,
        "g": 0.0,
        "h": 0.25879286394294676,
        "i": 0.0492202456041059,
        "j": 0.03426501268672931
    },
    "info": 0
}
```

### The main components of the input: creating a new portfolio
The Index Tracking API is designed to be flexible, allowing users to specify only the necessary parameters for their specific use case. While many parameters are optional and can be used to impose constraints or refine the optimization, there are a few mandatory parameters that must always be provided, whether you are creating a new portfolio from scratch or rebalancing an existing one.

The following parameters are always required for a valid computation request:

- assets_covariance_matrix: The covariance matrix of assets, representing the risk and correlation between them.
- index_assets_covariance_vector: The covariance vector between assets and the index, used to measure how each asset relates to the index.
- portfolio_size: The number of assets to be included in the portfolio (ranging from 1 to 2047).
- asset_names: An array of asset identifiers or names, providing a reference for interpreting the results.

Additionally, while not strictly mandatory, it is always helpful to include:
- description: A brief description of the computation, aiding in tracking and identifying different requests.

A valid request with only the mandatory parameters (plus a description for clarity) might look like this:

```
{
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
  "description": "Testing from Postman",
  "asset_names": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
}
```

### Adding basic constraints
As we mentioned in **[The index tracking problem](#11--the-index-tracking-problem)**, we can impose conditions

### Rebalancing a portfolio

### Sectorization

### Advanced constraints




