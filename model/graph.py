import matplotlib.pyplot as plt
import seaborn as sns
import model as PaperAnalysis
class DataVisualization:
    def __init__(self, pdf_path):
        # Initialize PaperAnalysis object with the given PDF path
        self.objectTarget = PaperAnalysis.PaperAnalysis(pdf_path)
        # Extract the combined data (assuming this returns a list)
        self.objectReturn = self.objectTarget.data_combination()

    def visualize_male_female_participants_pie_chart(self):
        # Extract the relevant data for the pie chart
        male_participants_count = self.objectReturn[0]
        female_participants_count = self.objectReturn[1]

        # Total participants
        total_participants = male_participants_count + female_participants_count

        # Prepare data for the pie chart
        if total_participants == 0:
            sizes = [1]  # Only one category for no participants
            labels = ["N/A"]
            pie_colors = ["gray"]
            title = "Males vs Females Participants Data"
            autopct = None  # No percentage display needed for single category
        else:
            sizes = [male_participants_count, female_participants_count]
            labels = ['Male', 'Female']
            pie_colors = ["#CB2529", "#70374B"]  # Red for male, purple for female
            title = "Male vs Female Participants Data"

            # Define autopct to show both percentage and number of participants
            def autopct_func(pct, allvalues):
                total = sum(allvalues)
                absolute = int(pct / 100. * total)
                return f'{pct:.1f}%\n({absolute} Participants)'

            autopct = lambda pct: autopct_func(pct, sizes)

        # Create the pie chart
        plt.figure(figsize=(8, 8))
        if (total_participants == 0):
            wedges, texts = plt.pie(
            sizes,
            labels=labels,
            colors=pie_colors,
            autopct=autopct,
            startangle=140,
            textprops=dict(color="white", fontsize=12)
            )
        else:
            wedges, texts, autotexts = plt.pie(
            sizes,
            labels=labels,
            colors=pie_colors,
            autopct=autopct,
            startangle=140,
            textprops=dict(color="white", fontsize=12)
            )


        # Add title
        plt.title(title, color="#CCC8A8", fontsize=16)

        # Set background color of the plot
        plt.gcf().set_facecolor("#472E34")

        plt.savefig("participants_pie_chart.png", format="png", dpi=300, bbox_inches='tight')

    def visualize_male_female_authors_pie_chart(self):
        # Extract the relevant data for the pie chart
        male_authors_count = self.objectReturn[2]
        female_authors_count = self.objectReturn[3]

        # Total participants
        total_authors = male_authors_count + female_authors_count

        # Prepare data for the pie chart
        if total_authors == 0:
            sizes = [1]  # Only one category for no participants
            labels = ["N/A"]
            pie_colors = ["gray"]
            title = "Males vs Females Authors Reference Data"
            autopct = None  # No percentage display needed for single category
        else:
            sizes = [male_authors_count, female_authors_count]
            labels = ['Male', 'Female']
            pie_colors = ["#CB2529", "#70374B"]  # Red for male, purple for female
            title = "Male vs Female Authors Reference Data"

            # Define autopct to show both percentage and number of participants
            def autopct_func(pct, allvalues):
                total = sum(allvalues)
                absolute = int(pct / 100. * total)
                return f'{pct:.1f}%\n({absolute} Authors)'

            autopct = lambda pct: autopct_func(pct, sizes)

        # Create the pie chart
        plt.figure(figsize=(8, 8))
        if (total_authors == 0):
            wedges, texts = plt.pie(
            sizes,
            labels=labels,
            colors=pie_colors,
            autopct=autopct,
            startangle=140,
            textprops=dict(color="white", fontsize=12)
            )
        else:
            wedges, texts, autotexts = plt.pie(
            sizes,
            labels=labels,
            colors=pie_colors,
            autopct=autopct,
            startangle=140,
            textprops=dict(color="white", fontsize=12)
            )


        # Add title
        plt.title(title, color="#CCC8A8", fontsize=16)

        # Set background color of the plot
        plt.gcf().set_facecolor("#472E34")

        plt.savefig("authors_pie_chart.png", format="png", dpi=300, bbox_inches='tight')
    

    def visualize_male_female_pronouns_pie_chart(self):
        # Extract the relevant data for the pie chart
        male_pronouns_count = self.objectReturn[4]
        female_pronouns_count = self.objectReturn[5]

        # Total participants
        total_pronouns = male_pronouns_count + female_pronouns_count

        # Prepare data for the pie chart
        if total_pronouns < 3:
            sizes = [1]  # Only one category for no participants
            labels = ["N/A"]
            pie_colors = ["gray"]
            title = "Males vs Females Pronouns Data"
            autopct = None  # No percentage display needed for single category
        else:
            sizes = [male_pronouns_count, female_pronouns_count]
            labels = ['Male', 'Female']
            pie_colors = ["#CB2529", "#70374B"]  # Red for male, purple for female
            title = "Male vs Female Pronouns Data"

            # Define autopct to show both percentage and number of participants
            def autopct_func(pct, allvalues):
                total = sum(allvalues)
                absolute = int(pct / 100. * total)
                return f'{pct:.1f}%\n({absolute} Pronouns)'

            autopct = lambda pct: autopct_func(pct, sizes)

        # Create the pie chart
        plt.figure(figsize=(8, 8))
        if (total_pronouns < 3):
            wedges, texts = plt.pie(
            sizes,
            labels=labels,
            colors=pie_colors,
            autopct=autopct,
            startangle=140,
            textprops=dict(color="white", fontsize=12)
            )
        else:
            wedges, texts, autotexts = plt.pie(
            sizes,
            labels=labels,
            colors=pie_colors,
            autopct=autopct,
            startangle=140,
            textprops=dict(color="white", fontsize=12)
            )


        # Add title
        plt.title(title, color="#CCC8A8", fontsize=16)

        # Set background color of the plot
        plt.gcf().set_facecolor("#472E34")

        plt.savefig("pronouns_pie_chart.png", format="png", dpi=300, bbox_inches='tight')

    def graph_combination(self):
        graphResult.visualize_male_female_participants_pie_chart()   
        graphResult.visualize_male_female_authors_pie_chart()
        graphResult.visualize_male_female_pronouns_pie_chart()
if __name__ == "__main__":
    graphResult = DataVisualization("HotFlashes.pdf")
    graphResult.graph_combination()
    