from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from jsonschema import validate, ValidationError
from main_app.models.BlackLittermanYieldModel import BlackLittermanYieldModel
from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData
from infrastructure.defi_llama import get_historic_tvl_and_apy_from_symbol
import json
import uvicorn


class ModelEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        model_name = request.path_params['model_name']

        schema_file = 'data_classes/BlackLittermanModelDataSchema.json'
        with open(schema_file, 'r') as file:
            schema = json.load(file)
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            return JSONResponse({'error': str(e)}, status_code=400)

        result = self.run_model(model_name, data)
        return JSONResponse({'result': result})


    def run_model(self, model_name, payload):
        if str(model_name).lower() != 'blacklitterman':
            raise Exception('Only BlackLitterman model is supported at present')

        # Build model and calculate
        json_payload = json.dumps(payload)
        model_data = BlackLittermanModelData.from_json(json_payload)
        model = BlackLittermanYieldModel(model_data=model_data)
        model.calculate()

        # todo For mvp, return sample portfolio. Replace with above once data has been integrated.
        return """
    {
      "Model": "BlackLitterman",
      "ModelResults": [
        {
          "Views": [
            {
              "Weights": [
                { "asset": "stETH", "weight": 1.0 },
                { "asset": "tzBTC", "weight": -1.0 }
              ],
              "Return": 0.0125
            },
            {
              "Weights": [
                { "asset": "USDC", "weight": 1.0 }
              ],
              "Return": 0.03
            }
          ],
          "Allocations": [
            { "asset": "stETH", "weight": 0.5 },
            { "asset": "tzBTC", "weight": 0.2 },
            { "asset": "USDC", "weight": 0.3 }
          ]
        },
        {
          "Views": [
            {
              "Weights": [
                { "asset": "stETH", "weight": 1.0 },
                { "asset": "USDC", "weight": -1.0 }
              ],
              "Return": 0.02
            },
            {
              "Weights": [
                { "asset": "USDC", "weight": 1.0 }
              ],
              "Return": 0.02
            },
            {
              "Weights": [
                { "asset": "tzBTC", "weight": 1.0 }
              ],
              "Return": 0.035
            }
          ],
          "Allocations": [
            { "asset": "stETH", "weight": 0.4 },
            { "asset": "tzBTC", "weight": 0.5 },
            { "asset": "USDC", "weight": 0.1 }
          ]
        }
      ]
    }
    """

class MarketDataEndpoint(HTTPEndpoint):
    async def get(self, request):
        # Handle the GET request for `/symbols`
        if request.url.path == "/market_data/symbols":
            return await self.get_supported_symbols_json()

        if "metric_set" in request.path_params:
            return await self.get_metrics(request)

        return JSONResponse({"error": "Endpoint not found"}, status_code=404)

    async def post(self, request):
        # Handle the POST request for `/metrics`
        if "metrics" in request.path_params:
            return await self.get_metrics(request)
        return JSONResponse({"error": "Endpoint not found"}, status_code=404)

    async def get_metrics(self, request):
        provider = str(request.path_params['provider'])
        metric_set = str(request.path_params['metric_set'])
        symbol = str(request.path_params['symbol'])
    
        if provider.lower() != 'defillama':
            return JSONResponse({"error": "'Only DefiLlama market data provider is supported at present'"}, status_code=404)
    
        if metric_set.lower() != 'tvl_and_apy':
            return JSONResponse({"error": "'Only tvl_and_apy market data metric set is supported at present'"}, status_code=404)

        if symbol.upper() not in self.get_supported_symbols():
            return JSONResponse({"error": "Symbol not supported"}, status_code=404)
    
        df = get_historic_tvl_and_apy_from_symbol(symbol.upper())
        json_data = df.to_json(orient="records")
        return JSONResponse(content=json.loads(json_data), status_code=200)

    async def get_supported_symbols_json(self):
        # Logic to return the supported symbols for market data
        return JSONResponse({"symbols": self.get_supported_symbols()})

    def get_supported_symbols(self):
        # Logic to return the supported symbols for market data
        return ["STETH", "GHO", "USDC", "WBTC", "JITOSOL"]


routes = [
    Route('/run_model/{model_name}', ModelEndpoint),
    Route('/market_data/metrics/{provider}/{metric_set}/{symbol}', MarketDataEndpoint),
    Route('/market_data/symbols', MarketDataEndpoint)
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)