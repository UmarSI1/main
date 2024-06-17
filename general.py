import pickle
import zipfile
from pathlib import Path
from collections import defaultdict
import os
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import textwrap


######### Data General plot - Total number of Moderation Actions per Company
def sum_company(data, company):
    """ Sum all numbers for a certain company key """
    total_sum = 0
    for harm in data[company].values():
        for content_type in harm.values():
            for moderation_action in content_type.values():
                for automation_status in moderation_action.values():
                    total_sum += automation_status
    return total_sum




######## Data General plot - Total number of Moderation Actions per Company
def plot_company_dataxxz(data, List_of_companies):
    """ Sum all numbers for a certain company key and plot the results as a table. """
    def sum_company(data, company):
        """ Sum all numbers for a certain company key """
        total_sum = 0
        for harm in data[company].values():
            for content_type in harm.values():
                for moderation_action in content_type.values():
                    for automation_status in moderation_action.values():
                        total_sum += automation_status
        return total_sum

    company_data = {'Company': [], 'N# Actions': []}
    total_sum_all_companies = 0
    
    for company in List_of_companies:
        num_actions = sum_company(data, company)
        company_data['Company'].append(company)
        company_data['N# Actions'].append(int(num_actions))
        total_sum_all_companies += num_actions

    # Add the total to the data after the loop
    company_data['Company'].append('Total')
    company_data['N# Actions'].append(total_sum_all_companies)

    df_company = pd.DataFrame(company_data).dropna()

    # Plotting the table
    fig, ax = plt.subplots(figsize=(10, 6))

    # Table
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df_company.values, colLabels=df_company.columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])

    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(df_company.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed



    plt.tight_layout()
    return fig


def plot_company_dataxxz_normalized(data, List_of_companies):
    """ Sum all numbers for a certain company key and plot the results as a normalized bar chart. """
    def sum_company(data, company):
        """ Sum all numbers for a certain company key """
        total_sum = 0
        for harm in data[company].values():
            for content_type in harm.values():
                for moderation_action in content_type.values():
                    for automation_status in moderation_action.values():
                        total_sum += automation_status
        return total_sum

    company_data = {'Company': [], 'N# Actions': []}
    total_sum_all_companies = 0
    
    for company in List_of_companies:
        num_actions = sum_company(data, company)
        company_data['Company'].append(company)
        company_data['N# Actions'].append(num_actions)
        total_sum_all_companies += num_actions

    # Add the total to the data after the loop
    company_data['Company'].append('Total')
    company_data['N# Actions'].append(total_sum_all_companies)

    df_company = pd.DataFrame(company_data).dropna()

    # Normalize the data
    df_company['Normalized Actions'] = df_company['N# Actions'] / total_sum_all_companies

    # Plotting the normalized bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    df_company.plot(kind='bar', x='Company', y='Normalized Actions', ax=ax)
    ax.set_xlabel('Company')
    ax.set_ylabel('Normalized Number of Actions')
    ax.set_title('Normalized Number of Actions per Company')
    ax.set_xticklabels(df_company['Company'], rotation=90)
    plt.xticks(rotation=45)

    plt.tight_layout()
    return fig


######### Data General plot - Total number of Moderation Actions per Harm

def sum_harm(data_ACC):
    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }
    
    # Sum all numbers for each harm type across all companies
    harm_totals = {}
    total_sum_all_harms = 0  # Initialize the total sum for all harms
    
    for company in data_ACC.values():
        for harm, harm_data in company.items():
            if harm not in harm_totals:
                harm_totals[harm] = 0
            for content_type in harm_data.values():
                for moderation_action in content_type.values():
                    for automation_status in moderation_action.values():
                        harm_totals[harm] += automation_status
                        total_sum_all_harms += automation_status  # Accumulate the total sum

    # Add the total to the data after the loop
    harm_totals['Total'] = total_sum_all_harms  # Append the total sum

    harm_data = {'Harm': list(harm_totals.keys()), 'N# Actions': list(harm_totals.values())}
    df_harm = pd.DataFrame(harm_data).dropna()

    # Renaming the harm categories in your DataFrame
    df_harm['Harm'] = df_harm['Harm'].map(category_descriptions).fillna('Total')

    # Plotting the table graph
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_harm.values, colLabels=df_harm.columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])


    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(df_harm.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
               # cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    return fig


######### Data General plot - Total number of Moderation Actions per Type of Content

def plot_content_type_totals(data):
    """ Sum all numbers for each content type across all companies and plot the results as a table. """
    content_type_totals = {}
    total_sum_all_content_types = 0  # Initialize the total sum for all content types

    # Sum all numbers for each content type across all companies
    for company in data.values():
        for harm in company.values():
            for content_type, content_data in harm.items():
                if content_type not in content_type_totals:
                    content_type_totals[content_type] = 0
                for moderation_action in content_data.values():
                    for automation_status in moderation_action.values():
                        content_type_totals[content_type] += automation_status
                        total_sum_all_content_types += automation_status  # Accumulate the total sum

    # Add the total to the data after the loop
    content_type_totals['Total'] = total_sum_all_content_types  # Append the total sum

    # Create a DataFrame for the content type totals
    content_type_data = {'Content Type': list(content_type_totals.keys()), 'N# Actions': list(content_type_totals.values())}
    df_content_type = pd.DataFrame(content_type_data).dropna()

    # Define content type descriptions for mapping
    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    # Rename the content types in the DataFrame
    df_content_type['Content Type'] = df_content_type['Content Type'].map(content_type_descriptions).fillna('Total')

    # Plotting the table
    fig1, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_content_type.values, colLabels=df_content_type.columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])

    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(df_content_type.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
             #   cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Display the table
    plt.show()

    return fig1


######### Data General plot - Total number of Moderation Actions per Type of Moderation Actions

def plot_moderation_action_totals(data):
    """ Sum all numbers for each moderation action across all companies and plot the results as a table. """
    moderation_action_totals = {}
    total_sum_all_moderation_actions = 0  # Initialize the total sum for all moderation actions

    # Sum all numbers for each moderation action across all companies
    for company in data.values():
        for harm in company.values():
            for content_type in harm.values():
                for moderation_action, action_data in content_type.items():
                    if moderation_action not in moderation_action_totals:
                        moderation_action_totals[moderation_action] = 0
                    for automation_status in action_data.values():
                        moderation_action_totals[moderation_action] += automation_status
                        total_sum_all_moderation_actions += automation_status  # Accumulate the total sum

    # Add the total to the data after the loop
    moderation_action_totals['Total'] = total_sum_all_moderation_actions  # Append the total sum

    # Create a DataFrame for the moderation action totals
    moderation_action_data = {'Moderation Action': list(moderation_action_totals.keys()),
                              'N# Actions': list(moderation_action_totals.values())}
    df_moderation_action = pd.DataFrame(moderation_action_data).dropna()

    # Define visibility descriptions for mapping
    visibility_descriptions = {
        '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
        '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
        '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
        '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
        '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
        '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
        '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
        '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
        '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
        '[]': 'NOT DEFINED',
        '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'
    }

    # Rename the moderation actions in the DataFrame
    df_moderation_action['Moderation Action'] = df_moderation_action['Moderation Action'].map(visibility_descriptions).fillna('Total')

    # Plotting the table
    fig2, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_moderation_action.values, colLabels=df_moderation_action.columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])


    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(df_moderation_action.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
               # cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Display the table
    plt.show()

    return fig2


######### Data General plot - Total number of Moderation Actions per Type of Moderation - ADD GRAPH
def plot_automation_status_totals(data):
    """ Sum all numbers for each automation status across all companies and plot the results as a table. """
    automation_status_totals = {}
    total_sum_all_automation_statuses = 0  # Initialize the total sum for all automation statuses

    # Sum all numbers for each automation status across all companies
    for company in data.values():
        for harm in company.values():
            for content_type in harm.values():
                for moderation_action in content_type.values():
                    for automation_status, count in moderation_action.items():
                        if automation_status not in automation_status_totals:
                            automation_status_totals[automation_status] = 0
                        automation_status_totals[automation_status] += count
                        total_sum_all_automation_statuses += count  # Accumulate the total sum

    # Add the total to the data after the loop
    automation_status_totals['Total'] = total_sum_all_automation_statuses  # Append the total sum

    # Create a DataFrame for the automation status totals
    automation_status_data = {'Automation Status': list(automation_status_totals.keys()),
                              'N# Actions': list(automation_status_totals.values())}
    df_automation_status = pd.DataFrame(automation_status_data).dropna()

    # Define automation decision descriptions for mapping
    automated_decision_cleaned = {
        'AUTOMATED_DECISION_FULLY': 'Fully Automated',
        'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
        'AUTOMATED_DECISION_PARTIALLY': 'Partially Automated'
    }

    # Rename the automation statuses in the DataFrame
    df_automation_status['Automation Status'] = df_automation_status['Automation Status'].map(automated_decision_cleaned).fillna('Total')

    # Plotting the table
    fig3, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=df_automation_status.values, colLabels=df_automation_status.columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])

    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(df_automation_status.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
              #  cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed


    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Display the table
    plt.show()

    return fig3

# Example usage with the given data
# fig = plot_automation_status_totals(data_ACC)



######### Data General plot - Number of reported Harms per Company FIX DESIGN
def plot_harm_totals_per_company(data):
    """ Sum all numbers for each harm per company and plot the results as a table. """
    harm_totals_per_company = {company: {} for company in data.keys()}
    total_harm_totals = {company: 0 for company in data.keys()}  # Initialize total sum for each company

    # Sum all numbers for each harm per company
    for company, harms in data.items():
        for harm, harm_data in harms.items():
            if harm not in harm_totals_per_company[company]:
                harm_totals_per_company[company][harm] = 0
            for content_type in harm_data.values():
                for moderation_action in content_type.values():
                    for count in moderation_action.values():
                        harm_totals_per_company[company][harm] += count
                        total_harm_totals[company] += count  # Accumulate the total sum for each company

    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Harm': [], 'N# Actions': []}
    for company, harms in harm_totals_per_company.items():
        for harm, total_actions in harms.items():
            data_for_df['Company'].append(company)
            data_for_df['Harm'].append(harm)
            data_for_df['N# Actions'].append(int(total_actions))
        # Add total for each company
        data_for_df['Company'].append(company)
        data_for_df['N# Actions'].append(int(total_harm_totals[company]))
        data_for_df['Harm'].append('Total')

    df_harm_per_company = pd.DataFrame(data_for_df).dropna()

    # Define harm category descriptions for mapping
    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFUL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    # Rename the harm categories in the DataFrame
    df_harm_per_company['Harm'] = df_harm_per_company['Harm'].map(category_descriptions).fillna('Total')

    # Pivot the DataFrame
    pivot_df = df_harm_per_company.pivot(index='Company', columns='Harm', values='N# Actions').fillna(0).reset_index()

    wrapped_columns = [textwrap.fill(col, width=10) for col in pivot_df.columns]


    # Plotting the table
    fig4, ax = plt.subplots(figsize=(10, 8))  # Adjust the figsize as needed
    ax.axis('tight')
    ax.axis('off')
    ax.set_position([0, 0, 3, 3])

    # Create the table
    table = ax.table(cellText=pivot_df.values, colLabels=wrapped_columns, cellLoc='center', loc='center',  bbox=[0, 0, 1, 1])


    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
             #   cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed



    # Set cell height
    table.auto_set_column_width(col=list(range(len(pivot_df.columns))))
    table.scale(1, 1.5)  # Increase cell height (adjust as needed)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(22)  # Adjust font size as needed

    # Display the table
    plt.show()

    return fig4



######### Data General plot - Number of reported content type  per Company
def plot_content_type_totals_per_company(data):
    """ Sum all numbers for each content type per company and plot the results as a table. """
    content_type_totals_per_company = {company: {} for company in data.keys()}
    total_content_type_totals = {company: 0 for company in data.keys()}  # Initialize total sum for each company

    # Sum all numbers for each content type per company
    for company, harms in data.items():
        for harm in harms.values():
            for content_type, content_data in harm.items():
                if content_type not in content_type_totals_per_company[company]:
                    content_type_totals_per_company[company][content_type] = 0
                for moderation_action in content_data.values():
                    for count in moderation_action.values():
                        content_type_totals_per_company[company][content_type] += count
                        total_content_type_totals[company] += count  # Accumulate the total sum for each company

    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Content Type': [], 'N# Actions': []}
    for company, content_types in content_type_totals_per_company.items():
        for content_type, total_actions in content_types.items():
            data_for_df['Company'].append(company)
            data_for_df['Content Type'].append(content_type)
            data_for_df['N# Actions'].append(int(float(total_actions)))  # Convert to float first, then to int
        # Add total for each company
        data_for_df['Company'].append(company)
        data_for_df['Content Type'].append('Total')
        data_for_df['N# Actions'].append(total_content_type_totals[company])

    df_content_type_per_company = pd.DataFrame(data_for_df).dropna()

    # Define content type descriptions for mapping
    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    # Rename the content type categories in the DataFrame
    df_content_type_per_company['Content Type'] = df_content_type_per_company['Content Type'].map(content_type_descriptions).fillna('Total')

    # Handle duplicate entries by summing them
    df_content_type_per_company = df_content_type_per_company.groupby(['Company', 'Content Type'], as_index=False).sum()



    # Pivot the DataFrame
    pivot_df = df_content_type_per_company.pivot(index='Company', columns='Content Type', values='N# Actions').fillna(0).reset_index()

    wrapped_columns = [textwrap.fill(col, width=15) for col in pivot_df.columns]

    # Plotting the table
    fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the figsize as needed
    ax.axis('tight')
    ax.axis('off')
    ax.set_position([0, 0, 3, 3])

    # Create the table
    table = ax.table(cellText=pivot_df.values, colLabels=wrapped_columns, cellLoc='center', loc='center',  bbox=[0, 0, 1, 1])

    # Set cell height
    table.auto_set_column_width(col=list(range(len(pivot_df.columns))))
    table.scale(1, 3)  # Increase cell height (adjust as needed)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(27)

    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
                cell.get_text().set_text(formatter(int(float(cell.get_text().get_text()))))  # Convert to float first, then to int

    # Set cell height
    table.auto_set_column_width(col=list(range(len(pivot_df.columns))))
    table.scale(1, 1.5)  # Increase cell height (adjust as needed)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(22)

    # Display the table
    plt.show()

    return fig



######### Data General plot - Number of reported moderation action per Company

def sum_reports_per_moderation_action_per_company(data):
    """ 
    Sum all numbers for each moderation action per company
    """
    # Step 1: Initialize total sum dictionary
    total_moderation_action_totals_per_company = {company: 0 for company in data.keys()}
    
    # Step 2: Update loop to accumulate total sum
    moderation_action_totals_per_company = {company: {} for company in data.keys()}
    for company, harms in data.items():
        for harm in harms.values():
            for content_type in harm.values():
                for moderation_action, action_data in content_type.items():
                    if moderation_action not in moderation_action_totals_per_company[company]:
                        moderation_action_totals_per_company[company][moderation_action] = 0
                    for count in action_data.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            moderation_action_totals_per_company[company][moderation_action] += count
                            total_moderation_action_totals_per_company[company] += count  # Accumulate total sum
    
    # Step 3: Add total sum for each company to the data
    data_for_df = {'Company': [], 'Moderation Action': [], 'N# Actions': []}
    for company, moderation_actions in moderation_action_totals_per_company.items():
        for moderation_action, total_actions in moderation_actions.items():
            data_for_df['Company'].append(company)
            data_for_df['Moderation Action'].append(moderation_action)
            data_for_df['N# Actions'].append(int(total_actions))
        # Add total for each company
        data_for_df['Company'].append(company)
        data_for_df['Moderation Action'].append('Total')
        data_for_df['N# Actions'].append(str(int(total_moderation_action_totals_per_company[company])))
    
    df_moderation_action_per_company = pd.DataFrame(data_for_df).dropna()
    
    visibility_descriptions = {
        '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
        '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
        '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
        '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
        '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
        '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
        '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
        '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
        '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
        '[]': 'NOT DEFINED',
        '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'
    }

    # Renaming the harm categories in your DataFrame
    df_moderation_action_per_company['Moderation Action'] = df_moderation_action_per_company['Moderation Action'].map(visibility_descriptions)

    # Handle duplicate entries by summing them
    df_moderation_action_per_company = df_moderation_action_per_company.groupby(['Company', 'Moderation Action'], as_index=False).sum()

    # Pivot the DataFrame
    pivot_df = df_moderation_action_per_company.pivot(index='Company', columns='Moderation Action', values='N# Actions').fillna(0).reset_index()

    wrapped_columns = [textwrap.fill(str(col), width=20) for col in pivot_df.columns]

    fig, ax = plt.subplots(figsize=(13, 8))  # Adjust the figsize as needed
    ax.axis('tight')
    ax.axis('off')
    ax.set_position([0, 0, 3, 3])

    # Create the table
    table = ax.table(cellText=pivot_df.values, colLabels=wrapped_columns, cellLoc='center', loc='center',  bbox=[0, 0, 1, 1])

    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
              #  cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed

    # Set cell height
    table.auto_set_column_width(col=list(range(len(pivot_df.columns))))
    table.scale(1, 3)  # Increase cell height (adjust as needed)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(25)


    return fig



######### Data General plot - Number of reported moderation type  per Company

def plot_automation_status_table_general(data):
    """ Sum all numbers for each automation status per company and plot the results as a table. """
    # Initialize total sum
    total_automation_status_totals = {}
    
    # Sum all numbers for each automation status per company
    automation_status_totals_per_company = {company: {} for company in data.keys()}
    for company, harms in data.items():
        for harm in harms.values():
            for content_type in harm.values():
                for moderation_action in content_type.values():
                    for automation_status, count in moderation_action.items():
                        if automation_status not in automation_status_totals_per_company[company]:
                            automation_status_totals_per_company[company][automation_status] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            automation_status_totals_per_company[company][automation_status] += count
                            total_automation_status_totals[automation_status] = total_automation_status_totals.get(automation_status, 0) + count
    
    # Prepare data for DataFrame
    data_for_df = {'Automation Status': [], 'N# Actions': []}
    for automation_status, total_actions in total_automation_status_totals.items():
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(int(total_actions))
    
    # Add a row for the total sum of all companies combined
    total_sum = sum(total_automation_status_totals.values())
    data_for_df['Automation Status'].append('Total')
    data_for_df['N# Actions'].append(total_sum)
    
    df_automation_status = pd.DataFrame(data_for_df).dropna()

    # Define automated decision descriptions for mapping
    automated_decision_cleaned = {
        'AUTOMATED_DECISION_FULLY': 'Fully Automated',
        'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
        'AUTOMATED_DECISION_PARTIALLY': 'Partially Automated',
        'Total': 'Total'  # Added 'Total' mapping
    }

    # Rename the automated decision categories in the DataFrame
    df_automation_status['Automation Status'] = df_automation_status['Automation Status'].map(automated_decision_cleaned)

    # Plotting the table
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figsize as needed
    ax.axis('tight')
    ax.axis('off')
    ax.set_position([0, 0, 1, 1])

    # Create the table
    table = ax.table(cellText=df_automation_status.values, colLabels=df_automation_status.columns, cellLoc='center', loc='center',  bbox=[0, 0, 1, 1])


    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(df_automation_status.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
        #        cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed

    # Set cell height
    table.auto_set_column_width(col=list(range(len(df_automation_status.columns))))
    table.scale(1, 1.5)  # Increase cell height (adjust as needed)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(18)

    # Display the table
    plt.show()

    return fig



def plot_normalized_automation_status(data):
    """ Plot the normalized counts of each automation status per company as a stacked bar chart. """
    automation_status_totals_per_company = {company: {} for company in data.keys()}
    
    # Sum all numbers for each automation status per company
    for company, harms in data.items():
        for harm in harms.values():
            for content_type in harm.values():
                for moderation_action in content_type.values():
                    for automation_status, count in moderation_action.items():
                        if automation_status not in automation_status_totals_per_company[company]:
                            automation_status_totals_per_company[company][automation_status] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            automation_status_totals_per_company[company][automation_status] += count
    
    # Prepare data for DataFrame
    data_for_df = {'Company': [], 'Automation Status': [], 'N# Actions': []}
    for company, automation_statuses in automation_status_totals_per_company.items():
        for automation_status, total_actions in automation_statuses.items():
            data_for_df['Company'].append(company)
            data_for_df['Automation Status'].append(automation_status)
            data_for_df['N# Actions'].append(total_actions)
    
    df_automation_status_per_company = pd.DataFrame(data_for_df).dropna()

    # Define automated decision descriptions for mapping
    automated_decision_cleaned = {
        'AUTOMATED_DECISION_FULLY': 'Fully Automated',
        'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
        'AUTOMATED_DECISION_PARTIALLY': 'Partially Automated',
    }

    # Rename the automated decision categories in the DataFrame
    df_automation_status_per_company['Automation Status'] = df_automation_status_per_company['Automation Status'].map(automated_decision_cleaned)

    # Pivot the DataFrame
    pivot_df = df_automation_status_per_company.pivot(index='Company', columns='Automation Status', values='N# Actions').fillna(0).reset_index()

    # Normalize the values
    pivot_df.iloc[:, 1:] = pivot_df.iloc[:, 1:].div(pivot_df.iloc[:, 1:].sum(axis=1), axis=0)


    # Plotting the normalized data
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_df.set_index('Company').plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel('Company')
    ax.set_ylabel('Normalized Count')
    ax.set_title('Normalized Automation Status by Company')
    ax.legend(title='Automation Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.xticks(rotation=45)
    return fig





######### Data General plot - Number of reported content type  per Harm

def plot_harm_content_type(data):
    """ Sum all numbers for each harm per content type and plot the results as both a table and a stacked bar chart. """
    harm_content_type_totals = {}
    
    # Sum all numbers for each harm per content type
    for company_data in data.values():
        for harm, harm_data in company_data.items():
            for content_type, content_type_data in harm_data.items():
                if (harm, content_type) not in harm_content_type_totals:
                    harm_content_type_totals[(harm, content_type)] = 0
                for moderation_action in content_type_data.values():
                    for count in moderation_action.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_content_type_totals[(harm, content_type)] += count
    
    # Prepare data for DataFrame
    data_for_df = {'Harm': [], 'Content Type': [], 'N# Actions': []}
    for (harm, content_type), total_actions in harm_content_type_totals.items():
        data_for_df['Harm'].append(harm)
        data_for_df['Content Type'].append(content_type)
        data_for_df['N# Actions'].append(total_actions)

    df_harm_content_type = pd.DataFrame(data_for_df).dropna()

    # Define harm and content type descriptions for mapping
    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    content_type_descriptions = {
            '["CONTENT_TYPE_OTHER"]': 'OTHER',
            '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
            '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
            '["CONTENT_TYPE_TEXT"]': 'TEXT',
            '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
            '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
            '["CONTENT_TYPE_APP"]': 'APP',
            '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
    
            '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
    
            '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
    
            '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
    
            '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
    
            '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
        }

    # Rename the categories in the DataFrame
    df_harm_content_type['Harm'] = df_harm_content_type['Harm'].map(category_descriptions)
    df_harm_content_type['Content Type'] = df_harm_content_type['Content Type'].map(content_type_descriptions)

    # Pivot the DataFrame for the table
    pivot_df_table = df_harm_content_type.pivot(index='Harm', columns='Content Type', values='N# Actions').fillna(0).reset_index()

    # Plotting the table
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    ax.set_position([0, 0, 3, 3])
    table = ax.table(cellText=pivot_df_table.values, colLabels=pivot_df_table.columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])


    table.auto_set_column_width(col=list(range(len(pivot_df_table.columns))))
    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(20)


    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df_table.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
            #    cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed

    # Pivot the DataFrame for the chart
    pivot_df_chart = df_harm_content_type.pivot(index='Harm', columns='Content Type', values='N# Actions').fillna(0).reset_index()
    
    # Normalize the values
    pivot_df_chart.iloc[:, 1:] = pivot_df_chart.iloc[:, 1:].div(pivot_df_chart.iloc[:, 1:].sum(axis=1), axis=0)

    # Plotting the normalized data
    pivot_df_chart.set_index('Harm').plot(kind='bar', stacked=True)
    plt.xlabel('Harm')
    plt.ylabel('Normalized Count')
    plt.title('Normalized Content Type by Harm')
    plt.legend(title='Content Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    return fig


def plot_harm_content_type_normalized(data):
    """ Sum all numbers for each harm per content type and plot the results as a normalized stacked bar chart. """

    harm_content_type_totals = {}
    
    # Sum all numbers for each harm per content type
    for company_data in data.values():
        for harm, harm_data in company_data.items():
            for content_type, content_type_data in harm_data.items():
                if (harm, content_type) not in harm_content_type_totals:
                    harm_content_type_totals[(harm, content_type)] = 0
                for moderation_action in content_type_data.values():
                    for count in moderation_action.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_content_type_totals[(harm, content_type)] += count
    
    # Prepare data for DataFrame
    data_for_df = {'Harm': [], 'Content Type': [], 'N# Actions': []}
    for (harm, content_type), total_actions in harm_content_type_totals.items():
        data_for_df['Harm'].append(harm)
        data_for_df['Content Type'].append(content_type)
        data_for_df['N# Actions'].append(int(total_actions))

    df_harm_content_type = pd.DataFrame(data_for_df).dropna()

    # Define harm and content type descriptions for mapping
    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFUL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO', 
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    # Rename the categories in the DataFrame
    df_harm_content_type['Harm'] = df_harm_content_type['Harm'].map(category_descriptions)
    df_harm_content_type['Content Type'] = df_harm_content_type['Content Type'].map(content_type_descriptions)

    # Pivot the DataFrame for the chart
    pivot_df_chart = df_harm_content_type.pivot(index='Harm', columns='Content Type', values='N# Actions').fillna(0).reset_index()
    
    # Normalize the values
    pivot_df_chart.iloc[:, 1:] = pivot_df_chart.iloc[:, 1:].div(pivot_df_chart.iloc[:, 1:].sum(axis=1), axis=0)

    # Plotting the normalized data
    fig, ax = plt.subplots(figsize=(10, 6))
    
    pivot_df_chart.set_index('Harm').plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel('Harm')
    ax.set_ylabel('Normalized Count')
    ax.set_title('Normalized Content Type by Harm')
    ax.legend(title='Content Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    plt.xticks(rotation=45)
    
    return fig


import matplotlib.ticker as mtick

######## Data General plot - Number of reported Moderation Action  per Harm
def sum_reports_per_harm_per_moderation_action(data):
    """ Sum all numbers for each harm per moderation action and plot a table """
    # Sum all numbers for each harm per moderation action
    harm_moderation_action_totals = {}

    for company_data in data.values():
        for harm, harm_data in company_data.items():
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    if (harm, moderation_action) not in harm_moderation_action_totals:
                        harm_moderation_action_totals[(harm, moderation_action)] = 0
                    for count in moderation_action_data.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_moderation_action_totals[(harm, moderation_action)] += count

    # Prepare data for DataFrame
    data_for_df = {'Harm': [], 'Moderation Action': [], 'N# Actions': []}
    for (harm, moderation_action), total_actions in harm_moderation_action_totals.items():
        data_for_df['Harm'].append(harm)
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['N# Actions'].append(int(total_actions))

    df_harm_moderation_action = pd.DataFrame(data_for_df).dropna()

    # Maps for renaming categories
    visibility_descriptions = {
        '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
        '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
        '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
        '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
        '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
        '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
        '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
        '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
        '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
        '[]': 'NOT DEFINED',
        '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'
    }

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFULL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    # Renaming the harm categories in the DataFrame
    df_harm_moderation_action['Harm'] = df_harm_moderation_action['Harm'].map(category_descriptions)
    df_harm_moderation_action['Moderation Action'] = df_harm_moderation_action['Moderation Action'].map(visibility_descriptions)

    # Pivot the DataFrame
    pivot_df = df_harm_moderation_action.pivot(index='Harm', columns='Moderation Action', values='N# Actions').fillna(0).reset_index()
    pivot_df.columns = pivot_df.columns.map(str)

    wrapped_columns = [textwrap.fill(col, width=20) for col in pivot_df.columns]

    

    # Plotting the table graph
    fig, ax = plt.subplots(figsize=(13, 6))  # Adjust the figsize as needed
    ax.axis('tight')
    ax.axis('off')
    ax.set_position([0, 0, 3, 3])


    # Create the table
    table = ax.table(cellText=pivot_df.values, colLabels=wrapped_columns, cellLoc='center', loc='center',  bbox=[0, 0, 1, 1])

    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
             #   cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed

    # Set cell height
    table.auto_set_column_width(col=list(range(len(pivot_df.columns))))
    table.scale(1, 3)  # Increase cell height (adjust as needed)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(25)

    # Display the figure
    plt.show()

    return fig


######### Data General plot - Number of reported Moderation type  per Harm

def plot_harm_automation_status(data):
    """ Sum all numbers for each harm per automation status and plot the results as a table. """
    harm_automation_status_totals = {}
    
    # Sum all numbers for each harm per automation status
    for company_data in data.values():
        for harm, harm_data in company_data.items():
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    for automation_status, count in moderation_action_data.items():
                        if (harm, automation_status) not in harm_automation_status_totals:
                            harm_automation_status_totals[(harm, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_automation_status_totals[(harm, automation_status)] += count
    
    # Prepare data for DataFrame
    data_for_df = {'Harm': [], 'Automation Status': [], 'N# Actions': []}
    for (harm, automation_status), total_actions in harm_automation_status_totals.items():
        data_for_df['Harm'].append(harm)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

    df_harm_automation_status = pd.DataFrame(data_for_df).dropna()

    # Define automated decision and category descriptions for mapping
    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFUL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    # Rename the categories in the DataFrame
    df_harm_automation_status['Harm'] = df_harm_automation_status['Harm'].map(category_descriptions)
    df_harm_automation_status['Automation Status'] = df_harm_automation_status['Automation Status'].map(automated_decision_cleaned)

    # Pivot the DataFrame for the table
    pivot_df_table = df_harm_automation_status.pivot(index='Harm', columns='Automation Status', values='N# Actions').fillna(0).reset_index()

    # Plotting the table
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=pivot_df_table.values, colLabels=pivot_df_table.columns, cellLoc='center', loc='center')
    table.auto_set_column_width(col=list(range(len(pivot_df_table.columns))))


    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df_table.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
             #   cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed
    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    plt.tight_layout()
    
    return fig


def plot_harm_automation_status_two(data):
    """ Sum all numbers for each harm per automation status and plot the results as a normalized stacked bar chart. """
    harm_automation_status_totals = {}
    
    # Sum all numbers for each harm per automation status
    for company_data in data.values():
        for harm, harm_data in company_data.items():
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    for automation_status, count in moderation_action_data.items():
                        if (harm, automation_status) not in harm_automation_status_totals:
                            harm_automation_status_totals[(harm, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            harm_automation_status_totals[(harm, automation_status)] += count
    
    # Prepare data for DataFrame
    data_for_df = {'Harm': [], 'Automation Status': [], 'N# Actions': []}
    for (harm, automation_status), total_actions in harm_automation_status_totals.items():
        data_for_df['Harm'].append(harm)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(total_actions)

    df_harm_automation_status = pd.DataFrame(data_for_df).dropna()

    # Define automated decision and category descriptions for mapping
    automated_decision_cleaned = {
            'AUTOMATED_DECISION_FULLY': 'Fully Automated',
            'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
            'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }

    category_descriptions = {
        'STATEMENT_CATEGORY_SCOPE_OF_PLATFORM_SERVICE': 'PLATFORM SCOPE',
        'STATEMENT_CATEGORY_DATA_PROTECTION_AND_PRIVACY_VIOLATIONS': 'GDPR VIOLATION',
        'STATEMENT_CATEGORY_PORNOGRAPHY_OR_SEXUALIZED_CONTENT': 'PORN/SEX CONTENT',
        'STATEMENT_CATEGORY_ILLEGAL_OR_HARMFUL_SPEECH': 'ILLEGAL/HARMFUL SPEECH',
        'STATEMENT_CATEGORY_VIOLENCE': 'VIOLENCE',
        'STATEMENT_CATEGORY_SCAMS_AND_FRAUD': 'SCAMS/FRAUD',
        'STATEMENT_CATEGORY_UNSAFE_AND_ILLEGAL_PRODUCTS': 'ILLEGAL PRODUCTS',
        'STATEMENT_CATEGORY_NON_CONSENSUAL_BEHAVIOUR': 'NON CONSENSUAL BEHAVIOUR',
        'STATEMENT_CATEGORY_PROTECTION_OF_MINORS': 'PROTECT MINORS',
        'STATEMENT_CATEGORY_INTELLECTUAL_PROPERTY_INFRINGEMENTS': 'COPYRIGHT',
        'STATEMENT_CATEGORY_NEGATIVE_EFFECTS_ON_CIVIC_DISCOURSE_OR_ELECTIONS': 'NEGATIVE EFFECTS ELECTIONS',
        'STATEMENT_CATEGORY_RISK_FOR_PUBLIC_SECURITY': 'RISK PUBLIC SECURITY',
        'STATEMENT_CATEGORY_ANIMAL_WELFARE': 'ANIMAL WELFARE',
        'STATEMENT_CATEGORY_SELF_HARM': 'SELF HARM'
    }

    # Rename the categories in the DataFrame
    df_harm_automation_status['Harm'] = df_harm_automation_status['Harm'].map(category_descriptions)
    df_harm_automation_status['Automation Status'] = df_harm_automation_status['Automation Status'].map(automated_decision_cleaned)

    # Pivot the DataFrame for the chart
    pivot_df_chart = df_harm_automation_status.pivot(index='Harm', columns='Automation Status', values='N# Actions').fillna(0).reset_index()

    # Normalize the values
    pivot_df_chart.iloc[:, 1:] = pivot_df_chart.iloc[:, 1:].div(pivot_df_chart.iloc[:, 1:].sum(axis=1), axis=0)

    # Plotting the normalized data
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_df_chart.set_index('Harm').plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel('Harm')
    ax.set_ylabel('Normalized Count')
    ax.set_title('Normalized Automation Status by Harm')
    ax.legend(title='Automation Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.xticks(rotation=45)
    
    return fig



######### Data General plot - Number of reported Moderation type  per Content Type

def plot_content_type_automation_status(data):
    """ Sum all numbers for each content type per automation status and plot the results as a table. """
    content_type_automation_status_totals = {}
    
    # Sum all numbers for each content type per automation status
    for company_data in data.values():
        for harm_data in company_data.values():
            for content_type, content_type_data in harm_data.items():
                for moderation_action_data in content_type_data.values():
                    for automation_status, count in moderation_action_data.items():
                        if (content_type, automation_status) not in content_type_automation_status_totals:
                            content_type_automation_status_totals[(content_type, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            content_type_automation_status_totals[(content_type, automation_status)] += count
    
    # Prepare data for DataFrame
    data_for_df = {'Content Type': [], 'Automation Status': [], 'N# Actions': []}
    for (content_type, automation_status), total_actions in content_type_automation_status_totals.items():
        data_for_df['Content Type'].append(content_type)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(int(total_actions))

    df_content_type_automation_status = pd.DataFrame(data_for_df).dropna()

    # Define automated decision and content type descriptions for mapping
    automated_decision_cleaned = {
        'AUTOMATED_DECISION_FULLY': 'Fully Automated',
        'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
        'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }

    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    # Rename the content types and automation statuses in the DataFrame
    df_content_type_automation_status['Content Type'] = df_content_type_automation_status['Content Type'].map(content_type_descriptions)
    df_content_type_automation_status['Automation Status'] = df_content_type_automation_status['Automation Status'].map(automated_decision_cleaned)

    # Pivot the DataFrame for the table
    pivot_df_table = df_content_type_automation_status.pivot(index='Content Type', columns='Automation Status', values='N# Actions').fillna(0).reset_index()

    # Plotting the table
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=pivot_df_table.values, colLabels=pivot_df_table.columns, cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
    table.auto_set_column_width(col=list(range(len(pivot_df_table.columns))))
    table.scale(2, 2)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df_table.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
         #       cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed

    plt.tight_layout()
    
    return fig


def plot_content_type_automation_status_two(data):
    """ Sum all numbers for each content type per automation status and plot the results as a stacked bar chart. """
    content_type_automation_status_totals = {}
    
    # Sum all numbers for each content type per automation status
    for company_data in data.values():
        for harm_data in company_data.values():
            for content_type, content_type_data in harm_data.items():
                for moderation_action_data in content_type_data.values():
                    for automation_status, count in moderation_action_data.items():
                        if (content_type, automation_status) not in content_type_automation_status_totals:
                            content_type_automation_status_totals[(content_type, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            content_type_automation_status_totals[(content_type, automation_status)] += count
    
    # Prepare data for DataFrame
    data_for_df = {'Content Type': [], 'Automation Status': [], 'N# Actions': []}
    for (content_type, automation_status), total_actions in content_type_automation_status_totals.items():
        data_for_df['Content Type'].append(content_type)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(int(total_actions))

    df_content_type_automation_status = pd.DataFrame(data_for_df).dropna()

    # Define automated decision and content type descriptions for mapping
    automated_decision_cleaned = {
        'AUTOMATED_DECISION_FULLY': 'Fully Automated',
        'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
        'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }

    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }

    # Rename the content types and automation statuses in the DataFrame
    df_content_type_automation_status['Content Type'] = df_content_type_automation_status['Content Type'].map(content_type_descriptions)
    df_content_type_automation_status['Automation Status'] = df_content_type_automation_status['Automation Status'].map(automated_decision_cleaned)

    # Pivot the DataFrame for the chart
    pivot_df_chart = df_content_type_automation_status.pivot(index='Content Type', columns='Automation Status', values='N# Actions').fillna(0).reset_index()

    # Normalize the values
    pivot_df_chart.iloc[:, 1:] = pivot_df_chart.iloc[:, 1:].div(pivot_df_chart.iloc[:, 1:].sum(axis=1), axis=0)

    # Plotting the normalized data
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_df_chart.set_index('Content Type').plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel('Content Type')
    ax.set_ylabel('Normalized Count')
    ax.set_title('Normalized Automation Status by Content Type')
    ax.legend(title='Automation Status', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig




######### Data General plot - Number of reported Moderation action  per Content Type


def generate_content_type_moderation_action_figure(data):
    """ Sum all numbers for each content type per moderation action and plot a table """
    # Sum all numbers for each content type per moderation action
    content_type_moderation_action_totals = {}

    for company_data in data.values():
        for harm_data in company_data.values():
            for content_type, content_type_data in harm_data.items():
                for moderation_action, moderation_action_data in content_type_data.items():
                    if (content_type, moderation_action) not in content_type_moderation_action_totals:
                        content_type_moderation_action_totals[(content_type, moderation_action)] = 0
                    for count in moderation_action_data.values():
                        if pd.notna(count):  # Check if the count is not NaN
                            content_type_moderation_action_totals[(content_type, moderation_action)] += count

    # Prepare data for DataFrame
    data_for_df = {'Content Type': [], 'Moderation Action': [], 'N# Actions': []}
    for (content_type, moderation_action), total_actions in content_type_moderation_action_totals.items():
        data_for_df['Content Type'].append(content_type)
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['N# Actions'].append(str(int(total_actions)))

    df_content_type_moderation_action = pd.DataFrame(data_for_df).dropna()

    # Maps for renaming categories
    content_type_descriptions = {
        '["CONTENT_TYPE_OTHER"]': 'OTHER',
        '["CONTENT_TYPE_SYNTHETIC_MEDIA"]': 'SYNTHETIC MEDIA',
        '["CONTENT_TYPE_IMAGE"]': 'IMAGE',
        '["CONTENT_TYPE_TEXT"]': 'TEXT',
        '["CONTENT_TYPE_VIDEO"]': 'VIDEO',
        '["CONTENT_TYPE_PRODUCT"]': 'PRODUCT',
        '["CONTENT_TYPE_APP"]': 'APP',
        '["CONTENT_TYPE_AUDIO"]': 'AUDIO',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT"]': 'IMAGE/TEXT',
        '["CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'IMAGE/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_TEXT"],"CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_TEXT","CONTENT_TYPE_VIDEO"]': 'AUDIO/TEXT/VIDEO/IMAGE',
        '["CONTENT_TYPE_AUDIO","CONTENT_TYPE_IMAGE","CONTENT_TYPE_VIDEO"]': 'AUDIO/IMAGE/VIDEO'
    }


    # Define visibility descriptions for mapping
    visibility_descriptions = {
    '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
    '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
    '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
    '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
    '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
    '[]': 'NOT DEFINED',
    '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'
}
    
    # Renaming the content type categories in the DataFrame
    df_content_type_moderation_action['Content Type'] = df_content_type_moderation_action['Content Type'].map(content_type_descriptions)

    # Renaming the moderation action categories in the DataFrame
    df_content_type_moderation_action['Moderation Action'] = df_content_type_moderation_action['Moderation Action'].map(visibility_descriptions)

    # Pivot the DataFrame
    pivot_df = df_content_type_moderation_action.pivot(index='Content Type', columns='Moderation Action', values='N# Actions').fillna(0).reset_index()

    pivot_df.columns = pivot_df.columns.map(str)

    # Plotting the table graph
    fig, ax = plt.subplots(figsize=(12, 7))  # Adjust the figsize as needed
    ax.axis('tight')
    ax.axis('off')
    ax.set_position([0, 0, 3, 3])

    wrapped_columns = [textwrap.fill(col, width=20) for col in pivot_df.columns]

    # Create the table
    table = ax.table(cellText=pivot_df.values, colLabels=wrapped_columns, cellLoc='center', loc='center',  bbox=[0, 0, 1, 1])

    # Set cell height
    table.auto_set_column_width(col=list(range(len(pivot_df.columns))))
    table.scale(1, 1)  # Increase cell height (adjust as needed)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(25)

    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
              # cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
              text = cell.get_text().get_text()
              try:
                  value = int(float(text))
                  cell.get_text().set_text(formatter(value))
              except ValueError:
                  pass  # or handle the error as needed
            
               

    # Display the figure
    plt.show()

    return fig

# Example usage:
# fig = generate_content_type_moderation_action_figure(data_ACC)







######### Data General plot - Number of reported Moderation type  per Moderation Action

def generate_moderation_action_automation_status_figure(data):
    """ Sum all numbers for each moderation action per automation status and plot a table """
    # Sum all numbers for each moderation action per automation status
    moderation_action_automation_status_totals = {}

    for company_data in data.values():
        for harm_data in company_data.values():
            for content_type_data in harm_data.values():
                for moderation_action, moderation_action_data in content_type_data.items():
                    for automation_status, count in moderation_action_data.items():
                        if (moderation_action, automation_status) not in moderation_action_automation_status_totals:
                            moderation_action_automation_status_totals[(moderation_action, automation_status)] = 0
                        if pd.notna(count):  # Check if the count is not NaN
                            moderation_action_automation_status_totals[(moderation_action, automation_status)] += count

    # Prepare data for DataFrame
    data_for_df = {'Moderation Action': [], 'Automation Status': [], 'N# Actions': []}
    for (moderation_action, automation_status), total_actions in moderation_action_automation_status_totals.items():
        data_for_df['Moderation Action'].append(moderation_action)
        data_for_df['Automation Status'].append(automation_status)
        data_for_df['N# Actions'].append(str(int(total_actions)))

    df_moderation_action_automation_status = pd.DataFrame(data_for_df).dropna()

    # Maps for renaming categories
    visibility_descriptions = {
    '["DECISION_VISIBILITY_CONTENT_REMOVED"]': 'REMOVED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED","DECISION_VISIBILITY_CONTENT_REMOVED"]': 'RESTRICTED/REMOVED',
    '["DECISION_VISIBILITY_CONTENT_REMOVED","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'REMOVED/AGE RESTRICTED',
    '["DECISION_VISIBILITY_OTHER","DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'OTHER/AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_LABELLED"]': 'LABELLED',
    '["DECISION_VISIBILITY_OTHER"]': 'OTHER',
    '["DECISION_VISIBILITY_CONTENT_AGE_RESTRICTED"]': 'AGE RESTRICTED',
    '["DECISION_VISIBILITY_CONTENT_DISABLED"]': 'DISABLED',
    '["DECISION_VISIBILITY_CONTENT_INTERACTION_RESTRICTED"]': 'INTERACTION RESTRICTED',
    '[]': 'NOT DEFINED',
    '["DECISION_VISIBILITY_CONTENT_DEMOTED"]': 'DEMOTED'

    }
   

    automated_decision_cleaned = {
        'AUTOMATED_DECISION_FULLY': 'Fully Automated',
        'AUTOMATED_DECISION_NOT_AUTOMATED': 'Not Automated',
        'AUTOMATED_DECISION_PARTIALLY': 'Partially automated',
    }

    # Renaming the categories in the DataFrame
    df_moderation_action_automation_status['Moderation Action'] = df_moderation_action_automation_status['Moderation Action'].map(visibility_descriptions)
    df_moderation_action_automation_status['Automation Status'] = df_moderation_action_automation_status['Automation Status'].map(automated_decision_cleaned)

    # Pivot the DataFrame
    pivot_df = df_moderation_action_automation_status.pivot(index='Moderation Action', columns='Automation Status', values='N# Actions').fillna(0).reset_index()

    # Plotting the table graph
    fig, ax = plt.subplots(figsize=(7, 6))  # Adjust the figsize as needed
    ax.axis('tight')
    ax.axis('off')

    # Create the table
    table = ax.table(cellText=pivot_df.values, colLabels=pivot_df.columns, cellLoc='center', loc='center',  bbox=[0, 0, 1, 1])

    # Set cell height
    table.auto_set_column_width(col=list(range(len(pivot_df.columns))))
    table.scale(1, 1.5)  # Increase cell height (adjust as needed)

    # Set font size
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    # Display the figure
    fig.tight_layout(pad=1)

    formatter = mtick.FuncFormatter(lambda x, _: f'{x:,.0f}')
    for i in range(1, len(pivot_df.columns)):
        for key, cell in table.get_celld().items():
            if key[0] != 0 and key[1] == i:  # Exclude the header row
               # cell.get_text().set_text(formatter(int(cell.get_text().get_text())))
                text = cell.get_text().get_text()
                try:
                    value = int(float(text))
                    cell.get_text().set_text(formatter(value))
                except ValueError:
                    pass  # or handle the error as needed
                    
                    return fig

# Example usage:
# fig = generate_moderation_action_automation_status_figure(data_ACC)
