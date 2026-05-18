from ydata_profiling import ProfileReport

class Profiler:

    def __init__(self, dataframe):
        self.df = dataframe

    def generate_report(self, output_file="report.html"):

        profile = ProfileReport(
            self.df,
            title="Juvaana Analytics Report",
            explorative=True
        )

        profile.to_file(output_file)

        print(f"Report saved as {output_file}")