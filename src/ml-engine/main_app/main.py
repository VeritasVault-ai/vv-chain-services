from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from jsonschema import validate, ValidationError
import json
import uvicorn

from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData

class ModelEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        model_name = request.path_params['model_name']

        try:
            import os
            schema_file = os.path.join(
                os.path.dirname(__file__),
                'data_classes',
                'BlackLittermanModelDataSchema.json'
            )
            with open(schema_file, 'r') as file:
                schema = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return JSONResponse({'error': f"Schema error: {str(e)}"}, status_code=500)

        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            return JSONResponse({'error': str(e)}, status_code=400)
        result = run_model(model_name, data)
        return JSONResponse({'result': result})


async def run_model(model_name, payload):
    # Place your model running code here
    if model_name != 'BlackLitterman':
        raise Exception('Only BlackLitterman model is supported at present')

    model_data = BlackLittermanModelData.from_dict(payload)
    
    # Import and instantiate the model
    from main_app.models.blacklittermanyieldmodel import BlackLittermanYieldModel
    model = BlackLittermanYieldModel(model_data)
    
    # Run the model and get results
    results = await model.run()
    
    # Return JSON serialized results
    return results.to_json()

routes = [
    Route('/run_model/{model_name}', ModelEndpoint),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)