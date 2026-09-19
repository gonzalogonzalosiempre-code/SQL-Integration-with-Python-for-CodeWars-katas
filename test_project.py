from project import extract_year_month, format_datos,combined_datos


def test_extract_year_month():
    assert extract_year_month('2026-09-16T05:39:12.554Z') == '2026-09'
def test_format_datos():
    tmp = ['manzana','pera','papaya']
    assert format_datos(tmp) == 'manzana pera papaya'
def test_combined_datos():
    kata_mock = {
    "name": "Multiply",
    "id": "50654ddff8835d0e2d000001",
    "completedLanguages": ["python", "javascript"],
    "completedAt": "2023-10-15T10:00:00Z"
    }

    detalle_mock = {
        "rank": {
            "name": "8 kyu"
        }
    }
    resultado = combined_datos(kata_mock,detalle_mock)
    assert resultado["name"] == "Multiply"
    assert resultado["id"] == "50654ddff8835d0e2d000001"
    assert resultado["rank.name"] == "8 kyu"
    assert resultado["completedAt"] == "2023-10-15T10:00:00Z"
    assert "completedLanguages" in resultado
