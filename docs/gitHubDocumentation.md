# GitHub Documentation

This document contains background information on the Linear Reg project, related artificial intelligence topics, and the project management methodology used.

## Linear Reg Project Overview

Linear Reg 1.0 is a software application that helps users easily create and work with [linear regression models](https://www.spiceworks.com/tech/artificial-intelligence/articles/what-is-linear-regression/). Using predictive mathematical formulas, this tool can make predictions based on specific information variables and datasets. The tool also offers unique insights into the model's predictive formula, enabling users to assess models for accuracy, save their models for future use, and update data entries to suit specific scenarios.

### Purpose and Goals

The purpose of this project is to build a dual-purpose educational tool, for both inexperienced users and developers, to gain experience working with the applications of artificial intelligence (AI).

For users, Linear Reg simplifies the process of creating linear regression models. The intuitive interface makes it easy for users to apply basic machine learning algorithms to build predictive models and conduct data analysis. Users can quickly grasp how linear regression works and how it can be used efficiently.

For developers, Linear Reg serves as a training opportunity to refine coding practices. The platform offers practical exercises to help new developers understand how to implement linear regression and write clean and efficient code. Linear Reg introduces the basics of machine learning and gives new developers a foundation to build upon as they begin working with AI.

### Target Audience

Primary users are post-secondary students or recent graduates, at the onset of their professional careers. Users will need to have some experience working with large bodies of data but could have little exposure to statistics and data-driven decision-making.

### Platforms and Technology

The following tools and equipment in Table 1 were used in the development of Linear Reg and complete the documentation:

| **Tools/Equipment**   | **Description** |
| :-------------------- | :-------------- |
| Visual Studio Code (version 1.93) | Code editor that will be used to view the developer's code and to edit Markdown files. |
| GitHub Desktop (version 3.4.5 x64) | Version control client to commit and push Markdown file changes to the repository. |
| Taiga | Project task management website to track sprints, user stories, and tasks. |
| TWP - Translate Web Pages | Firefox extension to translate text in Spanish to English to quickly read user stories and tasks. |
| Windows-based PC (Windows 10 or Windows 11) | Computer to test Linear Reg, as it is available only on PC. |

*Table 1: List of software and equipment used in development*

## Agile Development Process with Linear Reg

Agile methodology was used throughout the development of Linear Reg.

### What is Agile Development?

[Agile development](https://www.atlassian.com/agile/project-management) is an iterative and flexible project management method that focuses on collaboration and feedback. A popular framework for agile development is scrum. Unlike more rigid processes, scrum deliverables are incremental improvements to the software, which are released in short cycles called “sprints.” Development and documentation teams work closely to prioritize tasks and can adjust quickly if/when requirements change.

Table 2 contains a shortlist of essential terms used in Agile development projects:

| Term      | Definition |
| :-------- | :--------- |
| [User stories](https://www.atlassian.com/agile/project-management/user-stories#:~:text=Summary:%20A%20user%20story%20is,the%20end%20user%20or%20customer.) | A key part of agile software development. They are used to help teams understand how to build a product from the user's perspective and its value. A collection of user stories is called an “epic,” which is managed by a product owner. |
| Product backlog | A list of priority features for the product. |
| Sprint Planning | A team planning meeting that decides what to complete in the coming sprint. |
| Sprint Demo | An opportunity for teams to show the work was completed in that sprint. |
| Standup | A brief meeting for the software team to share updates and align workflows. |
| Retrospective | A review of what did and didn't go well in the last sprint. Specific actions to improve the next sprint are confirmed. |
| Scrum master | Oversees the scrum framework by facilitating standups, consults with the team and internal stakeholders to ensure the project stays on course. |

*Table 2: List of essential Agile terms*

### Linear Reg Development Sprints

Linear Reg was developed within 9 sprints, with 8 sprints lasting 1 week and 2 sprints lasting 2 weeks. During the 9 sprints, we developed the stable release of Linear Reg and created documentation for new developers (GitHub documentation) and for new users (README).

At the end of each sprint, the development team met for a sprint retrospective to discuss what went well during the sprint and what could be improved in the following sprints. The team chose upcoming user stories and measured complexity by estimating how long and difficult the user stories would be to complete.

## Artificial Intelligence and Related Concepts

Linear Reg allows both inexperienced users and developers to gain experience working with artificial intelligence and its applications.

### What is Artificial Intelligence?

[Artificial Intelligence](https://www.coursera.org/articles/what-is-artificial-intelligence) (AI) is a field of science that aims to mimic the cognitive processes of the human brain, such as reasoning, decision making, recognizing speech, and problem solving. As AI is a broad field, how it works is different with each [AI technique](https://cloud.google.com/learn/what-is-artificial-intelligence). However, the core principle revolves around data. Using data, the AI systems can find patterns and relationships that humans cannot. AI can be used within many different disciplines to inform data analytics, make predictions and give recommendations to support data driven decision making.

### What is Machine Learning?

[Machine learning](https://cloud.google.com/learn/what-is-machine-learning) (ML) is a subset of AI. ML uses algorithms, like linear regression models, to “learn” and improve computer system performance over time. With ML, the computer can process large datasets, gather insights, recognize patterns, and make informed decisions, without being explicitly programmed. As large datasets are processed, the ML model becomes more efficient.

People tend to use the terms AI and ML [interchangeably](https://cloud.google.com/learn/artificial-intelligence-vs-machine-learning), but they are not the same thing. AI is the **concept** of enabling a machine to reason like a human, while ML is one of the **applications** of AI that allows machines to extract knowledge and learn from data.

![Image of an umbrella labeled 'Artificial Intelligence' above terms including 'Machine Learning'.](/docs/assets/images/ai-umbrella.png "Artificial intelligence umbrella")

*Figure 1: Artificial intelligence is a broad topic that covers many applications. Image taken from [Why Business Leaders Should Think of AI as an Umbrella Term](https://medium.com/opex-analytics/why-business-leaders-should-think-of-ai-as-an-umbrella-term-dba8badc55e4)*

There are [three categories](https://www.ibm.com/topics/machine-learning) of ML models:
* **Supervised learning**, which uses labeled datasets to train algorithms to classify data.
* **Unsupervised learning**, which uses algorithms to analyze and group unlabeled datasets and to find hidden patterns or groupings.
* **Semi-supervised learning**, which is a midpoint between supervised and unsupervised learning and uses smaller labeled datasets to help classify the larger unlabeled datasets.

### What is Linear Regression?

Linear regression is a [supervised machine learning algorithm](https://www.ibm.com/topics/supervised-learning) used to identify a linear relationship between a dependent variable and one or more independent variables by plotting a line of best fit. It's typically used to make predictions.

![Screenshot visualizing the line of regression](/docs/assets/images/regression-line.png "Line of regression")

*Figure 2: Visualization of the best fit line for a linear regression model. Image from [What is Linear Regression? Types, Equation, Examples, and Best Practices for 2022](https://www.spiceworks.com/tech/artificial-intelligence/articles/what-is-linear-regression/)*

[Linear regression](https://www.spiceworks.com/tech/artificial-intelligence/articles/what-is-linear-regression/) helps businesses evaluate trends, make estimates, and forecast outcomes before making decisions. Some [basic examples](https://datatab.net/tutorial/linear-regression) where linear regression models can be used for information analysis and predictions include:

* Does height have an influence on the weight of a person?
* What is the relationship between pollution levels and rising temperatures?
* How does the age of a home affect the purchase price?
* How does RAM capacity affect its cost?

The above are examples of simple linear regression as there is only 1 dependent and 1 independent variable. If there are multiple independent variables, then it would be called multiple linear regression.

The regression line is described by the equation **ŷ = bx + a**, where:

* **ŷ** is the estimated dependent variable
* **b** is the slope (the gradient of the straight line)
* **x** is the independent variable
* **a** is the y-intercept (the point of intersection with the y-axis)

## Linear Reg Project Team 

Linear Reg's development and accompanying documentation was completed by a team of 4 developers, 2 technical writers and 2 overseeing managers. 

### Team Members and Responsibilities 

The following stakeholders and cross-functional teams in Table 3 were involved in the development and documentation of Linear Reg:

| Department | Name | Responsibilities |
| :--------- | :--- | :--------------- |
| Development Manager/Product Owner | Alberto José Alvarellos González | Oversee developer milestones |
| Documentation Manager | Amy Briggs | Oversee documentation milestones |
| Technical Writers | <ul><li>Katie Wallace</li><li>Nina Sanchez</li></ul> | Write product documentation |
| Developers | <ul><li>Pedro Martinez Ferrer</li><li>Alberto Benito Gómez</li><li>Miguel Armesto Dapena</li><li>Pablo Fariña Clemente</li> | Research and develop product |

*Table 3: Names, roles, and responsibilities of the Linear Reg development team*

### Considerations for New Developers 

The following considerations should be kept in mind when developing future iterations of the Linear Reg application: 

* **Follow coding best practices**
    * Code includes clear naming conventions, modularization and uses appropriate comments with necessary. 
    * Code is well structured and follows the [PEP 8](https://peps.python.org/pep-0008/) style guide formatting standards (Python). 
    * All Github commits should have clear, descriptive messages. 

* **Consolidate UI elements** 
    * UI elements with similar functions/implementations, like the data visualizer and column selector, can be integrated into the same body of code for better organization and efficiency. 

* **Select versatile libraries** 
    * Choose libraries that are simple to implement but also include a wide range of features to enhance the user interface and provide a richer experience. 

* **Focus on continuous improvement**  
    * Look for ways to improve the application by adding new visual features and upgrade or remove code that is outdated or no longer needed or useful. 

### Considerations for New Technical Writers 

The following considerations should be kept in mind when expanding Linear Reg's documentation: 

* **Follow technical writing best practices**
    * Continuously analyse audience and purpose to determine best approach to meet user needs.
    * Help topics include concept, task and reference information types.
    * Use direct and purposeful language.
    * Formatting should promote scanability and readability.
    
 * **Refer to the [Microsoft Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)**
    * Identify proper terminology for software documentation. 
    
 * **Write in Markdown** 
    * If comfortable, write or append new documentation directly in Markdown, commit the changes, then make a pull request. 
    * If not, then you can write documentation on Microsoft Word and contact one of the documentation writers to convert it into Markdown. 

### Linear Reg Localization

Localization efforts were performed throughout the development and documentation of Linear Reg. To support translation, best practices in User Experience (UX) writing were followed. User Interface (UI) elements and associated microcopy is:

* **Concise:** efficient and focused.
* **Purposeful:** goal-oriented and valuable.
* **Clear:** simple and specific language, void of jargon.