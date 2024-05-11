# Statlance

Statlance is a Python library for exploratory data analysis (EDA), visualization, and dashboarding.

## Installation

You can install Statlance using pip:

```bash
pip install statlance

# Data Loading and EDA
import statlance


# Load data
data = statlance.core.data_processing.load_data("data.csv")

# Display basic statistics
summary_stats = statlance.core.statistical_analysis.summary_statistics(data)
print(summary_stats)

# Visualize data distribution
statlance.core.visualization.histogram(data)

# Data Visualization
import statlance

# Load data
data = statlance.core.data_processing.load_data("data.csv")

# Visualize correlation matrix
statlance.core.visualization.correlation_matrix(data)

# Visualize scatter plot
statlance.core.visualization.scatter_plot(data, x='Feature1', y='Feature2')

# Dashboarding
import statlance

# Load data
data = statlance.core.data_processing.load_data("data.csv")

# Create a Streamlit dashboard
statlance.integration.streamlit_integration.create_dashboard(data)

# Machine Learning Model Training and Evaluation
import statlance

# Load data
data = statlance.core.data_processing.load_data("data.csv")

# Split data into features and target
X = data.drop('target', axis=1)
y = data['target']

# Train a machine learning model
model = statlance.core.statistical_analysis.train_model(X, y)

# Evaluate model performance
accuracy = statlance.core.statistical_analysis.evaluate_model(model, X, y)
print("Model accuracy:", accuracy)

