from transformations import build_keyword_performance_df

def test_full_transformation(spark):
    data = [
        (
            "http://search.yahoo.com/search?p=Laffy+Taffy",
            "1,2",
            "Candy;Laffy Taffy;1;12.95"
        )
    ]

    df = spark.createDataFrame(
        data,
        ["referrer", "event_list", "product_list"]
    )

    result = build_keyword_performance_df(df).collect()

    assert len(result) == 1
    assert result[0]["Search Engine Domain"] == "search.yahoo.com"
    assert result[0]["Search Keyword"] == "Laffy Taffy"
    assert result[0]["Revenue"] == 12.95
