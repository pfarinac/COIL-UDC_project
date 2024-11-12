# Linear Reg

## Introduction


### Overview
Linear Reg 1.0 is a software application that helps users easily create and work with linear regression models. Using predictive mathematical formulas, this tool is used to predict a result based on specific information variables and datasets. 
Its intuitive interface will allow users to easily explore relationships between data inputs and outputs. The tool also provides unique insights into the model’s predictive formula, enabling users to assess models for accuracy. Users can save their models for future use and update data entries to suit different scenarios.
### Features

## Getting Started

### Hardware/System Requirements

### Installing Python

Python is required to run Linear Reg as it was developed in this language.

1. Download Python from the [official website](https://www.python.org/downloads/ "Official Python website").
2. Run the Python installer.
3. Select "custom installation."
4. Make sure the following are checked:
    - Add Python to environment variables.
    - Install pip.
5. Finish installing Python.

### Downloading Linear Reg

You can download Linear Reg in three different ways.

- Go to the [Releases](https://github.com/pfarinac/COIL_project/releases) page to download the latest stable release.
- [Clone the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your local machine.
- [Download the source code](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives) and extract the zip file. 

#### Integrated development environment

An integrated development environment (IDE) is not necessary to run Linear Reg. (Go into more detail on what IDEs can help with?)

Here are some tips for using Visual Studio Code to run Python programs:
- Make sure to restart VS Code after [installing Python](#installing-python).
- Install the Python extension on VS Code.
    1. Select Extensions on the navigation tab.
    2. Type "ms-python.python" in the Search Extensions bar.
    3. Select the Install button.

### Installing Python libraries

For this section, you'll need to use a terminal. Here are some examples:
- (Windows) Command Prompt
- (Windows) PowerShell
- (MacOS) Terminal
- Visual Studio Code Terminal

1. Open your terminal of choice to the Linear Reg folder.
2. Type each of the following lines one at a time.

```
pip install PyQT6
pip install pandas
pip install scikit-learn
pip install matplotlib
```
3. Press Enter to install the library.
4. Repeat steps 2-3 until all libraries have been installed.

## User Interface
The user interface (UI) is divided into four main components: the data visualization window, input and output selectors, data preprocessing options, and an optional model description field.

[screenshot with callouts].

The steps to produce a linear regression model are completed in these four sections. The following table describes each of the UI components.

| UI Component| Description|
|:----------------------|:------------------------------------------------------------------------------|
| Data Visualization| Where you will upload and view your spreadsheet file (.csv. or .xlsx). This information will be used to create the linear regression model. Once the model is complete, the tool will display a graph of the data, incluing the model's prediction.|
| Input and Output selectors| Where you will select the columns of data you would like the tool to use to make predictions. Input "features" specify the conditional information to be retrieved and the output "targets" specify the outcome to predict. For example, ma model that predicts the price of a home (output) given the number of bedrooms (input).|
| Data Preprocessing| Where you will indicate how you would like the tool to handle any missing or incomplete spreadsheet data, called "nulls." LinearReg can: 
* Count Null Values - use this to include missing data, as is. 
* Delete Rows with Nulls - use this to delete the rows where data is missing.
* Replace Nulls with Average - use this to replace missing data with column's average value.
* Replace Nulls with Median - use this to replace the missing data with column's median value.
* Replace Nulls with Value - use this to replace the missing data with a specific value.

| Model Description| Where you can write key details related to a specific model, such as what information was used, the relationships to predict, and the accuracy of those predictions.|


## Functions and Usage

## Additional Information

### Support

### Developers

### Authors

### Contribution Guidelines

### License