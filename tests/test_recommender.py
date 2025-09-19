from src.recommender import recommend_product

def test_recommend_with_id():
    products = recommend_product(1)
    assert len(products) > 0

def test_recommend_without_id():
    products = recommend_product(None)
    assert products == []
def test_recommend_force_fail():
    # ❌ kasıtlı hata
    result = recommend("")
    assert result == ["dummy"]  # hiç olmayacak bir şey bekliyoruz