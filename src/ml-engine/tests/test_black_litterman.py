import pytest
from main_app.data_classes.BlackLittermanModelData import BlackLittermanModelData
from main_app.models.black_litterman.BlPortfolioModel import BlPortfolioModel

@pytest.fixture
def sample_json():
    """
    Provides a sample JSON string representing a BlackLitterman model configuration for testing.

    Returns:
        A multi-line JSON string containing model details, risk-free rates, and crypto market data.
    """
    with open("test_data/black_litterman_explicit_view_test_data.json", "r") as file:
        return file.read()


@pytest.mark.parametrize(
    "expected_model_name,expected_sub_model_name,expected_risk_free_rate_term,expected_risk_free_rate_rate,expected_m1_date",
    [("BlackLitterman", "ExplicitExcessReturnView-v0", "1D", 0.0175, "2025-05-03T15:30:00.123Z")],
)
def test_deserialization(sample_json: str, expected_model_name: str, expected_sub_model_name,
                         expected_risk_free_rate_term: str,
                         expected_risk_free_rate_rate: str, expected_m1_date: str):
    model_data = BlackLittermanModelData.from_json(sample_json)
    model = BlPortfolioModel(model_data)
    results = model.calculate()
    print(results.to_json())
    assert results.Model == expected_model_name
    assert results.Submodel == expected_sub_model_name
