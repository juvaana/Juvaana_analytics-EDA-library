import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from juvaana_analytics.core.loader import DataLoader
from juvaana_analytics.eda.analyzer import Analyzer
from juvaana_analytics.report.html_report import HTMLReport

# -----------------------------------
# LOAD DATA
# -----------------------------------
loader = DataLoader("C:\\Users\\kenne\\OneDrive\\Desktop\\Juvaana_analytics\\data\\sample.csv")

df = loader.load_csv()

print(df.head())

# -----------------------------------
# ANALYZE
# -----------------------------------
analyzer = Analyzer(df)

overview     = analyzer.overview()
summary      = analyzer.numeric_summary()
missing      = analyzer.missing_analysis()
correlations = analyzer.top_correlations()
column_types = analyzer.column_types()

# -----------------------------------
# REPORT
# -----------------------------------
report = HTMLReport()

report.set_data(
    df.to_dict(orient="records"),
    list(df.columns)
)

report.set_overview(overview)
report.set_summary(summary)
report.set_missing(missing)
report.set_correlations(correlations)
report.set_column_types(column_types)

# -----------------------------------
# GENERATE
# -----------------------------------
report.generate()

print("DONE")