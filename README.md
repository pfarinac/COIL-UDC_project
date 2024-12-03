# Linear Reg
This guide is intended for anyone using Linear Reg for the first time and serves as an introduction to Linear Reg’s User Interface (UI), primary functions and usage, and making predictions. Users will be able to understand how linear regression can be used to support data-driven decision-making.

## Overview
Linear Reg 1.0 is a software application that helps users easily create and work with [linear regression models](https://www.spiceworks.com/tech/artificial-intelligence/articles/what-is-linear-regression/ "linear regression models"). The intuitive interface makes it easy for users to apply basic machine learning algorithms to build predictive models and conduct data analysis. Users can quickly grasp how linear regression works and how it can be used efficiently.

## Features
Using predictive mathematical formulas, Linear Reg can make predictions based on specific datasets and the relationship between information variables. By building unique linear regression models, users can predict the value of one variable based on the value of another. The tool also offers unique insights into the model's predictive formula, enabling users to assess models for accuracy, save their models for future use, and update data entries to suit specific scenarios.

## Getting Started
This section covers everything you need to know to get started using Linear Reg.

### Minimum Hardware/System Requirements
This section covers the minimum requirements needed to run Linear Reg.

* **Operating system**: Microsoft Windows 10 or 11
* **Processor**: Intel i5
* **Memory**: 4 GB
* **Storage**: 15 MB available space
* **Display**: 1080 x 768 

### Downloading Linear Reg
You can download Linear Reg in two different ways.

* Go to the [Releases](https://github.com/pfarinac/COIL_project/releases) page to download the latest stable release.
* [Download the source code](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives) and extract the zip file. 

## Introduction to the Linear Reg Interface
Once you have downloaded and locally installed Linear Reg to your computer, click the Linear Reg icon to open the application.

The user interface (UI) is divided into five main components: the data visualization window, input and output selectors, data preprocessing options, the graph and formula displays, and an optional model description field (see: Figure 1).

[screenshot with callouts].

*Figure 1: Screenshot of the Linear Reg interface*

The steps to build a linear regression model are completed in these five sections. Table 1 describes each of the UI components. 

| UI Component          | Description                                                                   |
|:----------------------|:------------------------------------------------------------------------------|
| Data Visualization    | Upload and view your spreadsheet file (.csv. or .xlsx). This information will be used to build the linear regression model.   |
| Input and Output selectors | Select the columns of data you would like the tool to use to make predictions.   |
| Data Preprocessing | Indicate how you would like the tool to handle any missing or incomplete spreadsheet data, called "nulls."  <br><ul><li>Count Null Values - this function will identify how many cells within the selected columns are missing data.</li></ul>Once null values are identified, you can choose one of the following preprocessing conditions:<br><ul><li>Delete Rows with Nulls</li><li>Replace Nulls with Average</li><li>Replace Nulls with Median</li><li>Replace Nulls with Value</li></ul> |
| Graph and Formula windows | Where the graph of your linear regression model and prediction formula displays. |
| Model Description | Enter key details related to a specific model. |

*Table 1: Overview of Linear Reg's interface components*

## Linear Reg Functions and Usage
This section describes how to use Linear Reg’s functions to build linear regression models.

### Uploading your Data
To build your linear regression model, begin by uploading your spreadsheet (dataset). Table 2 lists the accepted spreadsheet file types: 

| File Type | Extension |
| :-------- | :-------- |
| Microsoft Excel | .xls, .xlsx |
| Comma-separated Values | .csv |

*Table 2: Accepted dataset file types*

**To upload your dataset**
1. Click **Open**.
2. Navigate to your spreadsheet, select the file, and click **Open**.<br>The spreadsheet displays in the Data visualization window (Figure 2).

[screenshot]

*Figure 2: Screenshot of the data visualization window*

### Building a Model 
Once your dataset has been uploaded, select the input and output columns you would like to isolate to make your prediction. The “input feature(s)” are the variables used to make the prediction, while the “output target” is the outcome you aim to predict.

[screenshot]

*Figure 3: Screenshot of the input and output selectors*

**To build a model**
1. Select the input column(s). 
2. Select the output column. 
3. Click **Confirm selection**.<br>The Information dialog box appears to confirm your selection has been saved. 
4. Click **OK**.
5. The selected column(s) are highlighted. 

### Setting Data Preprocessing Conditions
Once the input and output data has been selected, set the data preprocessing conditions to specify how Linear Reg should handle any missing or incomplete data. 

**To set preprocessing conditions**
1. Click **Count null values**.<br>The Null Values dialog box indicates how many cells are missing data, within your specified columns. 
2. Click **OK**.
3. Choose how Linear Reg should handle any missing or incomplete data:

| Data Preprocessing option | Use case |
| :---- | :---- |
| Delete rows with nulls | You want to delete the rows where data is missing. |
| Replace nulls with mean | You want to replace missing data with column’s average value. |
| Replace nulls with median | You want to replace missing data with column’s middle value. |
| Replace nulls with constant value | You want to replace the missing data with a specific value. |

Once the preprocessing option is selected, the Replaced Values dialog box opens, confirming your selection.

4. Click **OK**. 
5. Click **Start model**.<br>The linear regression model (graph) and formula displays. 

[screenshot]

*Figure 4: Screenshot of the graph and formula displays*

## Saving and Loading Models
Once the linear regression model has been built, you can save the model for future reference, including an optional model description. You can also load existing models to continue working with them. 

In the Model Description box, enter key details, such as what information variables were used, the relationships to predict, and the accuracy of those predictions. 

**To save a model**

1. Click **Save Model**. 
2. Navigate to the location where you would like to save your model, give your file a name, and click **Save**.<br>The Information dialog box appears to confirm that the model has been saved successfully.  
3. Click **OK**.<br>The model is saved to the specified location on your computer. 

**To load an existing model**

1. Click **Load Model**. 
2. Navigate to your saved model and click **Open**.<br>The Load modal dialog box appears to confirm the model has been loaded successfully.  
3. Click **OK**.<br>The existing model opens and formula displays. 

## Making Predictions
Once a new model has been built or an existing model has been loaded, a unique prediction field (labelled as the selected input column) appears below the Model description field (see Figure 5). New input variables can be entered to form predictions. 

[screenshot]

*Figure 5: Screenshot of the prediction field*

**To make a prediction**

1. Enter a value in the prediction field. 
2. Click **Make Prediction**.<br>The prediction result (labelled as the selected output column) appears. 


To assess the model’s accuracy, the model’s formula includes two metrics for regression analysis, R2 (R-squared) and MSE (Mean Squared Error). 

    R2 measures how well the model captures the variation in the data to indicate how well the model fits the data. R2 will always be between 0 and 1.  

    If R2 = 1, the model explains 100% of the variation in the data – a perfect fit. 

    If R2 = 0, the model doesn’t explain any variation in the data and the model is not useful. 

    MSE measures the average squared difference between the actual data and the model’s predicted values to indicate how much or how little error exists. 

    A lower MSE means the model’s predictions are close to the actual data. Lower value = more accurate predictions. 

    A higher MSE means the model’s predictions are farther from the actual data, which results in a high error probability. 


## Use Case Scenarios for Linear Reg
Linear regression can be used across various professional fields to uncover relationships between variables in many real-world scenarios. The following use case scenarios demonstrate how Linear Reg can be used by specific users for predicting future values based on existing data. 

### Preparing Real Estate Estimates

**Scenario**:
* A real estate agent, Antonio, believes the __number of bedrooms__ is an important factor influencing __property value__ and wants to provide better estimates to potential home buyers and sellers.
* Antonio decides to create a simple linear regression model that predicts the price of a home (output) given the number of bedrooms (input). Antonio gathers a dataset of information from several home sales, including total bedrooms and median value, and uploads the file (housing.csv) to Linear Reg.

**To build this model**

1. Click **Open**.  
2. Navigate to his spreadsheet dataset, “housing.csv” and click **Open**.<br>The spreadsheet displays in the Data visualization window. 
3. Select input column **total_bedrooms**. 
4. Select output column **median_house_value**.
5. Click **Confirm selection**.<br>The Information dialog box appears to confirm your selection has been saved. 
6. Click **OK**.<br>The selected column(s) are highlighted. 

**To set preprocessing conditions and view the model**

1. Click **Count null values**.<br>The Null Values dialog box indicates 200 cells are missing data specified columns. 
2. Click **OK**.<br>Antonio decides rows with missing data can be deleted. 
3. Click **Delete rows with nulls**.<br>The Replaced Values dialog box opens, confirming the selection. 
4. Click **OK**. 
5. Click **Start model**.<br>The graph and formula displays. 

Antonio would like to predict the median house value of 3-bedroom homes.

**To make a prediction**

1. Enter 3 in the prediction field. 
2. Click **Make Prediction**.<br>The prediction result (labelled as the selected output column) appears. (Figure 6)

[screenshot]

*Figure 6: Screenshot of Antonio's prediction result*


INSERT OTHER SCENARIO



## Additional Information

### Support

### Developers

### Authors

### Contribution Guidelines

### License