from src.recommender import recommend_product

def test_recommend_with_id():
    products = recommend_product(1)
    assert len(products) > 0

def test_recommend_without_id():
    products = recommend_product(None)
    assert products == []
