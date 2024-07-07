import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
import plotly.offline as pyo
from plotly.subplots import make_subplots
import seaborn as sns

## paginas GLOBAL, e para cada arquitetura


def print_accuracies(accuracies):
    # apresentar acuracia como rotulo
    # apresentar em gráfico de barras em comparacao entre as arquiteturas
    print('acc',accuracies)
    models = list(accuracies.keys())
    accuracies_list = [float(value) for value in accuracies.values()]

    fig = go.Figure()

    colors = {
    'True_Label': 'green', 
    'MLP': 'blue', 
    'SVM': 'red', 
    'KNN': 'purple', 
    'RANDOMFOREST': 'orange', 
    'DECISIONTREE': 'brown', 
    'NAIVEBAYES': 'pink'
    }

    colors_list = [colors[model] for model in models]

    for model, accuracy, color in zip(models, accuracies_list, colors_list):
        fig.add_trace(go.Bar(
            x=[model], 
            y=[accuracy], 
            marker_color=color, 
            name=model
        ))

    # Updating layout for better visualization
    fig.update_layout(
        title='Model Accuracies',
        xaxis_title='Model',
        yaxis_title='Accuracy (%)',
        yaxis=dict(range=[0, 100]), # Ensures the y-axis goes from 0 to 100%
    )

    fig.write_html("graphs/model_accuracies.html")

def print_occurrences(occurrences):
    # pizza
    print('OCCURRENCES:', occurrences)

    color_labels = {
        'Vertical_127_Hor_2_Mis': '#66c2a5',
        'Normal': '#fc8d62',
        'Vertical_Mis_127mm': '#8da0cb',
        'Unbalanced_30g': '#e78ac3',
        'Unbalanced_30g_Hor_Mis_2mm': '#a6d854',
        'Unbalanced_30g_Ver_Mis_127mm': '#ffd92f',
        'Horizontal_Mis_2mm': '#b3b3b3'
    }
    
    dfs = {}

    # Process each key in OCCURRENCES to create a DataFrame
    for key, value_list in occurrences.items():
        # Initialize a dictionary to accumulate occurrences
        aggregate_occurrences = {
            'Vertical_127_Hor_2_Mis': 0,
            'Normal': 0,
            'Vertical_Mis_127mm': 0,
            'Unbalanced_30g': 0,
            'Unbalanced_30g_Hor_Mis_2mm': 0,
            'Unbalanced_30g_Ver_Mis_127mm': 0,
            'Horizontal_Mis_2mm': 0
        }
        
        # Aggregate occurrences from the value_list for the current key
        for value in value_list:
            fault, occurrence = value
            if fault in aggregate_occurrences:
                aggregate_occurrences[fault] += occurrence
        
        # Convert aggregate_occurrences dictionary to a DataFrame
        df = pd.DataFrame(list(aggregate_occurrences.items()), columns=['fault', 'occurrence'])
        
        # Store the DataFrame in the dictionary with key as the key from OCCURRENCES
        dfs[key] = df

    # Accessing individual DataFrames for each key
    for key, df in dfs.items():
        print(f"DataFrame for {key}:")
        print(df)
        print()

        fig2 = px.pie(df, values='occurrence', names='fault', color='fault', color_discrete_map=color_labels,
                title=f'{key} Distribution', 
                hover_data=['occurrence'],  # Show occurrence on hover
                labels={'fault': 'Fault Type', 'occurrence': 'Occurrences'})  # Customize hover labels
    
        # Customize text inside each pie slice
        fig2.update_traces(textinfo='label+percent', 
                        textposition='inside',
                        textfont_size=20)
        # Save the pie chart as an HTML file
        fig2.write_html(f'graphs/{key}_distribution_pie_chart.html')

def print_data_bruta(data):
    # curves
    fault_types = ['Normal', 'Unbalanced_30g', 'Horizontal_Mis_2mm', 'Vertical_Mis_127mm', 
               'Vertical_127_Hor_2_Mis', 'Unbalanced_30g_Hor_Mis_2mm', 'Unbalanced_30g_Ver_Mis_127mm']

    # Initialize dict_fault
    dict_fault = {}

    # Iterate over each key in data and populate dict_fault
    for key, labels in data.items():
        dict_fault[key] = {}
        for fault_type in fault_types:
            dict_fault[key][fault_type] = [1 if label == fault_type else 0 for label in labels]

    # Fault types
    fault_types = ['Normal', 'Unbalanced_30g', 'Horizontal_Mis_2mm', 'Vertical_Mis_127mm', 
                'Vertical_127_Hor_2_Mis', 'Unbalanced_30g_Hor_Mis_2mm', 'Unbalanced_30g_Ver_Mis_127mm']

    # List of architectures (excluding True_Label)
    architectures = ['MLP', 'SVM', 'KNN', 'RANDOMFOREST', 'DECISIONTREE', 'NAIVEBAYES']

    color_labels = {
        'Vertical_127_Hor_2_Mis': '#66c2a5',
        'Normal': '#fc8d62',
        'Vertical_Mis_127mm': '#8da0cb',
        'Unbalanced_30g': '#e78ac3',
        'Unbalanced_30g_Hor_Mis_2mm': '#a6d854',
        'Unbalanced_30g_Ver_Mis_127mm': '#ffd92f',
        'Horizontal_Mis_2mm': '#b3b3b3'
    }

    # colors_map = color_scale[:len(fault_types)] 

    # Create separate graphs for each architecture
    for arch_idx, architecture in enumerate(architectures):
        fig3 = make_subplots(rows=2, cols=1, subplot_titles=("True_Label", architecture))

        # Add traces for True_Label
        for fault_idx, fault_type in enumerate(fault_types):
            fig3.add_trace(go.Scatter(x=list(range(1, 13)), y=dict_fault['True_Label'][fault_type],
                                    mode='lines+markers',
                                    name=f"{fault_type}",
                                    line=dict(color=color_labels[fault_type])),
                        row=1, col=1)

        # Add traces for the current architecture
        for fault_idx, fault_type in enumerate(fault_types):
            fig3.add_trace(go.Scatter(x=list(range(1, 13)), y=dict_fault[architecture][fault_type],
                                    mode='lines+markers',
                                    line=dict(color=color_labels[fault_type]),
                                    showlegend=False),
                        row=2, col=1)

        # Update layout to show legend and set legend titles
        fig3.update_layout(title=f"Comparison: True_Label vs {architecture}",
                        height=600, width=800, showlegend=True)

        # Update x-axis and y-axis titles for each subplot
        fig3.update_xaxes(title_text="Time", row=2, col=1)
        fig3.update_yaxes(title_text="Detection", row=2, col=1)

        # Save as HTML
        html_filename = f"graphs/true_label_vs_{architecture.lower()}_subplot.html"
        pyo.plot(fig3, filename=html_filename, auto_open=False)
    print('DATA BRUTA:', dict_fault)

def calculate_false_positives_and_negatives(normal_fault):
    """
    Calculate false positives (FP) and false negatives (FN) for each architecture/model.

    Parameters:
    true_labels (dict): Dictionary containing true labels of 'Normal' and 'Fault'.
    predictions (dict): Dictionary containing predictions of various models.

    Returns:
    fp_fn_dict (dict): Dictionary with FP and FN counts for each model.
    """

    fp_fn_dict = {}
    true_labels = normal_fault['True_Label']
    predictions = {key: value for key, value in normal_fault.items() if key != 'True_Label'}

    # Calculate FP and FN for each model
    for model, pred_counts in predictions.items():
        if pred_counts['Normal'] - true_labels['Normal'] >=0:
            fn = pred_counts['Normal'] - true_labels['Normal']
        else:
            fn = 0
        
        if pred_counts['Fault'] - true_labels['Fault'] >=0:
            fp = pred_counts['Fault'] - true_labels['Fault']
        else:
            fp = 0

        fp_fn_dict[model] = {'False_Negative': fn, 'False_Positive': fp}

    return fp_fn_dict

def print_normal_fault(normal_fault):
    # numero de FP e FN

    fp_fn_results = calculate_false_positives_and_negatives(normal_fault)

    for model, results in fp_fn_results.items():
        print(f"Model: {model}")
        print(f"False Positive: {results['False_Positive']}")
        print(f"False Negative: {results['False_Negative']}")
        print()