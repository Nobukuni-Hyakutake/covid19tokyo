import pandas as pd
url_df = pd.DataFrame(
    {
    "name": ["Python", "pandas"],
    "url": ["https://www.python.org/", "https://pandas.pydata.org"],
    }
    )
print(url_df)
print(url_df.to_html(render_links=True))