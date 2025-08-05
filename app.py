# app.py
from flask import Flask, jsonify
import pandas as pd
from scipy import stats
import os

app = Flask(__name__)

@app.route('/analyze')
def analyze_data():
    """
    An API endpoint to perform data analysis and hypothesis testing.
    It reads insurance data and performs an ANOVA test on BMI and children count for female clients.
    """
    file_path = 'insurance.csv'
    if not os.path.exists(file_path):
        return jsonify({"error": f"File not found: {file_path}"}), 404
        
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to read CSV file: {str(e)}"}), 500

    # Stating the Null and Alternate Hypotheses for the ANOVA test
    ho = "No. of children has no effect on bmi"   # Null Hypothesis
    ha = "No. of children has an effect on bmi"   # Alternate Hypothesis

    try:
        female_df = df[df['sex'] == 'female']
        zero_children = female_df[female_df['children'] == 0]['bmi']
        one_child = female_df[female_df['children'] == 1]['bmi']
        two_children = female_df[female_df['children'] == 2]['bmi']
        
        # Perform the one-way ANOVA test
        f_stat, p_value = stats.f_oneway(zero_children, one_child, two_children)

        # Determine the conclusion based on the p-value
        if p_value < 0.05:  # Significance level at 5%
            conclusion = f"{ha} as the p-value ({p_value.round(3)}) < 0.05"
        else:
            conclusion = f"{ho} as the p-value ({p_value.round(3)}) > 0.05"

    except Exception as e:
        return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500
    


    return jsonify({
        "null_hypothesis": ho,
        "alternate_hypothesis": ha,
        "f_statistic": f_stat,
        "p_value": p_value,
        "conclusion": conclusion
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
