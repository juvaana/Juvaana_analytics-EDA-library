from juvaana_analytics.eda.analyzer import Analyzer
from juvaana_analytics.report.html_report import HTMLReport


class Profiler:

    def __init__(self, dataframe):
        self.df = dataframe
        self.analyzer = Analyzer(dataframe)

    def generate_report(self, output_file="report.html", title="Juvaana Analytics Report"):

        # --- gather all analysis ---
        overview     = self.analyzer.overview()
        col_types    = self.analyzer.column_types()
        summary      = self.analyzer.numeric_summary()
        missing      = self.analyzer.missing_analysis()
        top_corrs    = self.analyzer.top_correlations()

        # --- prepare raw data for the interactive table / charts ---
        # convert to list-of-dicts; NaN → None so JSON serialises cleanly
        data    = self.df.where(self.df.notna(), other=None).to_dict(orient="records")
        columns = list(self.df.columns)

        # --- build report ---
        report = HTMLReport(title=title)
        report.set_data(data, columns)
        report.set_overview(overview)
        report.set_column_types(col_types)
        report.set_summary(summary)
        report.set_missing(missing)
        report.set_correlations(top_corrs)

        report.generate(output_file)