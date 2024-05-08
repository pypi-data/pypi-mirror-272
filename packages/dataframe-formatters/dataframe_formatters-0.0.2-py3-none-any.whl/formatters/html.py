"""HTML formatting utilities."""
import re
import pandas as pd
import warnings


def dataframe(df: pd.DataFrame, index: bool = True) -> str:
    """Return raw html table without formatting."""
    warnings.warn('use `remove_pandas_tags` instead', DeprecationWarning)
    return remove_pandas_tags(df.to_html(index=index))


def remove_pandas_tags(html: str) -> str:
    """Remove pandas tags from generated html output."""
    return re.sub(r'<tr.*>', '<tr>', html.replace('border="1"', ''))


def hyperlink(text: str, url: str) -> str:
    """Return anchor tag for hyperlink."""
    return f'<a href="{url}">{text}</a>'
