from src.recommender import recommend_product

def test_recommend_with_id():
    products = recommend_product(1)
    assert len(products) > 0

