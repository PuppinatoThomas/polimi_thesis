from experiments.model.prompt import QuestionPrompt
from experiments.model.task import Task

tasks = [
    Task(
        name="data_cleaning",
        prompts=[
            QuestionPrompt(
                prompt_id=1,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it?",
            ),
            QuestionPrompt(
                prompt_id=2,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it?", #mi serve per avere la versione aggiornata al nuovo modello senza perdere le vesrioni precedenti
            ),
            QuestionPrompt( #CoT
                prompt_id=3,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it?",
                system_message="The next task requires the following actions: 1) perform data standardization/data normalization; 2) error detection and correction; deuplicate detection",
            ),
            QuestionPrompt(
                prompt_id=4,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it? Let's think step by step.",
                system_message="You are a data quality expert. For this reason, you help users by providing detailed answers that stick to the task and dataset you are given. Be the most accurate and complete you can.",
            ),
            QuestionPrompt(
                prompt_id=5,
                user_message="Question: Consider this dataset:\n{{pharmacy_csv_text}}\nCan you do data cleaning on it?\n"
                             "Answer: 1) Data wrangling\n"
                             "\tDate: different formats (year-month-day and month/day/year). Transform them into the first format.\n"
                             "\tSales Person: since it contains bot name and surname, split it in two new columns ('Sales Person Name' and 'Sales Person Surname').\n"
                             "\tAmount ($): different currencies present (dollar and euro), since dollar is the common currency than remove the euro's sign and convert them to dollars.\n\n"
                             
                             "2) Missing data identification and correction\n"
                             "\tIdentification: looking at the dataset, clearly ["", nan, Missing] are missing values. Since there is absolutely no means in having 0 or '-' in any columns and they are recurrent values, they are other missing values.\n"
                             "\tCorrection (column by column):\n"
                             "\t\tDate: date type with high variability; Missing values: '-', 'Missing', "" ; impute with a standard value ('Date not available').\n"
                             "\t\tProduct:categorical column with high variability; Missing values: '-', 'Missing', "" ; impute with a standard value ('Product not specified').\n"
                             "\t\tSales Person Name: categorical column; Missing values: '-', 'Missing', "" ; if the surname is not a missing value impute the mode of that column, otherwise with a standard value ('Name not specified').\n"
                             "\t\tSales Person Surname: categorical column; Missing values: '-', 'Missing', "" ; if the name is not a missing value impute the mode of that column, otherwise with a standard value ('Surname not specified').\n"
                             "\t\tBoxes Shipped: numerical column; Missing values: 0, 'nan', "" ; use a regressor to impute values (some possible features to use are Product and Amount($)).\n"
                             "\t\tAmount ($): numerical column; Missing values: 0, 'nan', "" ; use a regressor to impute values (some possible features to use are Product and Boxes Shipped).\n"
                             "\t\tCountry: categorical value; Missing values: '-', 'Missing', "" ; since this dataset has a very limited number of different values then impute with the mode.\n\n"
                             
                             "3) Outlier detection and correction\n"
                             "\tDetection (consider columns with numerical values after imputation):\n"
                             "\t\tBoxes Shipped: since it is a numerical value, apply Median Absolute Deviation defined as: Z-Score = |x – median(x)| / mad(x). Considering a threshold of 2.5, the outliers are 24, 28, 28 and 29. Also values <6 are reported as outliers, but based on the context it is clear that with high probability they are correct values (it is common to buy small number of medicines)\n"
                             "\t\tAmount($): apply interquartile range method, no outlier is found.\n"
                             "\tCorrection: remove the real outliers and impute with the previous method.\n\n"
                             
                             "4) Duplicate detection and correction\n"
                             "\tDetection:\n"
                             "\t\tExact duplicate: since there is only one pair of rows that have the same values column by column, the pair (7,23), there is only one exact duplicate.\n"
                             "\t\tNon-exact duplicate detection: adopt a recordLinkage approach: select a blocking key (in this case Sales Person Name may be a good choice); group all the tuples with the same Sales Person Name and compare the values in each fields, pairwise. For each fields define a similarity measure (i.e.soundex for Sales Person Surname since they are surnames, or jaro-winkler for Product field, since it is a textual one). For the thresholds, we may want the same exact date, an high accuracy for textual fields (0.85), an offset of maximum 2 for Boxes Shipped; for the Amount ($) column, since the values are on a large scale, use abs(p1 - p2) / max(p1, p2) < 0.1. Finally, if, for each pair of tuples, the number of values that have a positive comparison is grater than 5, than consider them as duplicates.\n"
                             "\tCorrection: we have no criteria to choose between a tuple or another, drop one of the two randomly.\n\n"
                             
                             "Question: Consider this dataset:\n{{airline_csv_text}}\nCan you do data cleaning on it?\n"
                             "Answer: 1) Data wrangling\n"
                             "\tdeparture_time: some values are clearly inverted: Morning_Early should be replaced with Early_Morning, Afternoon_Late should be replaced with Late_Afternoon.\n"
                             "\tstops: since it consists of numerical values (excluding missing values) written in words, convert each string value in the numerical counterpart.\n"
                             "\tclass: there are different representations for the same concept: Business and bus are equivalent, Economic and eco are equivalent. Since Business and Economic are the more frequent and complete values, transform bus and eco in Business and Economic\n\n"
                             
                             "2) Missing data identification and correction\n"
                             "\tIdentification: looking at the dataset, clearly ["", nan, Missing] are missing values. Since there is absolutely no means in having  '-' in any columns and it is a recurrent value, it is another representation of missing value. Moreover, 999999999 is clearly a value inputted as a placeholder, it must be considered as a missing values and replaced.\n"
                             "\tCorrection (column by column):\n"
                             "\t\tairline: categorical column with low number of distinct values; Missing values: '-', 'Missing', "" ; impute with a standard value ('airline not available') or with the mode.\n"
                             "\t\tsource_city: categorical column; Missing values: '-', 'Missing', "" ; impute with a standard value ('City not specified').\n"
                             "\t\tdeparture_time: no missing value detected, no action required.\n"
                             "\t\tstops: numerical column; Missing values: '-', 'Missing', 999999999 ; since there are only 3 possible values (zero, one , two) impute with the mode.\n"
                             "\t\tclass: categorical column with only 2 possible values; Missing values: '-', 'Missing', "" ; impute with a standard value ('class not available') or with the mode.\n"
                             "\t\tduration: numerical column with high variability; Missing values: '-', 'nan', 999999999 ; impute with the median.\n"
                             "\t\tprice: numerical column with high variability; Missing values: '-', 'Missing', 999999999 ; impute with the median.\n\n"
                             
                             "3) Outlier detection and correction\n"
                             "\tDetection (consider columns with numerical values after imputation):\n"
                             "\t\tduration: since it is a numerical value, apply Median Absolute Deviation defined as: Z-Score = |x – median(x)| / mad(x). Considering a threshold of 3, the outliers found are 20.17 and 23.08 but based on the context it is clear that with high probability they are correct values (it is possible that some flight, consisting in more than one stop, lasts 24 hours)\n"
                             "\t\tprice: apply interquartile range method and MAD method: both find the higher outlier, 168000, but both fail to recognize small outliers.\n"
                             "\tCorrection: remove the real outliers and impute with the previous method.\n\n"
                              
                             "4) Duplicate detection and correction\n"
                             "\tDetection:\n"
                             "\t\tExact duplicate: since there is only one pair of rows that have the same values column by column, the pair (7,23), there is only one exact duplicate.\n"
                             "\t\tNon-exact duplicate detection: adopt a recordLinkage approach: select a blocking key (in this case airline may be a good choice since it divides the tuples in group with, approximately, the same number of tuples); group all the tuples with the same airline's value and compare the values in each fields, pairwise. For each fields define a similarity measure (i.e.soundex source_city since they are city names, or jaro-winkler for departure_time field, since it is a textual one). For the thresholds, we want the same class' value (since it's a binary field), an high accuracy for textual fields (0.85); for the price column, since the values are on a large scale, use abs(p1 - p2) / max(p1, p2) < 0.1; for the stops field, since the number of values acceptable is only 3, we want the same exact value; for the duration field, accept values if the have a maximum difference of +/- 2 (hours). Finally, if, for each pair of tuples, the number of values that have a positive comparison is grater than 5, than consider them as duplicates.\n"
                             "\tCorrection: we have no criteria to choose between a tuple or another, drop one of the two randomly.\n\n"
                             
                             "Question: Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it?\n"
                             "Answer: "


            ),
            QuestionPrompt(
                prompt_id=6,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it?\nTo complete this task, you need to follow these steps:\n1) Data transformation, that is, data type conversion (if necessary), mapping to a common format, and domain-specific transformations;\n2) Error localization and correction, that is, identifying and correcting inconsistencies, incomplete data, and outliers;\n3) Duplicate detection, that is, identifying exact and non-exact duplicates.",
            ),
            QuestionPrompt(
                prompt_id=7,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it?\nTo complete this task, you need to follow these steps:\n1) Mapping data into common formats, units of measurement and types.\n2) Detecting different representations of missing values in each column and infer or predict values to impute.\n3) Detecting  and handling outliers.\n4) Detecting and handling exact duplicates.\n5) Detecting and handling non-exact duplicates.",
            ),
            QuestionPrompt(
                prompt_id=8,
                user_message="Given a dataset, list all the operations required to perform data cleaning on it.",
            ),
            QuestionPrompt(
                prompt_id=9,
                user_message="Consider this dataset:\n{{csv_text}}\nPerform the following operations on it:\n{{answer_text}}"
            ),
            QuestionPrompt(
                prompt_id=10,
                user_message="Question: Consider this dataset:\n{{pharmacy_csv_text}}\nCan you do data cleaning on it?"
                             "Answer: Let's do it step by step. Firstly, there is the data wrangling phase. By looking at the data, we can notice that the dates have two different formats: month/day/year and year-month-day. In order to solve the problem, it is necessary to stick to a convention and change all dates to the chosen format (we can choose year-month-day). Moreover, the column 'Amount ($)' contains values that have a different currency (euros): to correct this error it is necessary to remove the euro sign and to convert the values from euros to dollars, applying the change. Finally, the column 'Sales Person' contains the name and the surname of the sales person: it is better to split it in two columns, 'Sales Person Name' and 'Sales Person Surname'.\n"
                             "As a second step, there is error detection and correction. Firstly, we identify different representations of missing values: some of them are obvious ( empty string, nan, Missing) others are more tricky. There is no reason to have a 0 in the 'Amount($)' or in the 'Boxes Shipped' columns, so also this is a missing value representation, same for '-'. Now, in order to impute the correct values, let's take a look to the data columns: 'Date', 'Product', 'Sales Person Name' and 'Sales Person Surname' have a really high variability, the best option is to use a placeholder like 'unknown' or 'not available'; for 'Boxes Shipped', a numerical column, a good option is to use the median; for 'Amount($)' the best option would be to use some machine learning technique or, if there are too many missing values in the other columns, to use again the median; for 'Country', since it is a categorical column with a restricted number of possible values, the best solution is to use the mode.\n"
                             "After that, for outliers detection, identify the columns that may have some outliers: since 'Amount ($)' and 'Boxes Shipped' are numerical columns, apply the Interquartile Range (IQR) method or the Z-score method. After the identification, one possible correction is to remove the incorrect value and to impute it using the previous rules.\n"
                             "As a last step, there is duplicate detection and correction. Firstly, identify exact duplicates (if they are present), then search for non-exact duplicates.\n"
                             "Question: Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it?\n"
                             "Answer: ",

            ),
            QuestionPrompt(
                prompt_id=11,
                user_message="Question: Consider this dataset:\n{{pharmacy_csv_text}}\nCan you do data cleaning on it?\n"
                             "Answer: 1) Data wrangling\n"
                             "\tDate: different formats (year-month-day and month/day/year). Transform them into the first format.\n"
                             "\tSales Person: since it contains bot name and surname, split it in two new columns ('Sales Person Name' and 'Sales Person Surname').\n"
                             "\tAmount ($): different currencies present (dollar and euro), since dollar is the common currency than remove the euro's sign and convert them to dollars.\n"
                             "2) Missing data identification and correction\n"
                             "\tIdentification: looking at the dataset, clearly ["", nan, Missing] are missing values. Since there is absolutely no means in having 0 or '-' in any columns and they are recurrent values, they are other missing values.\n"
                             "\tCorrection (column by column):\n"
                             "\t\tDate: date type with high variability; Missing values: '-', 'Missing', "" ; impute with a standard value ('Date not available').\n"
                             "\t\tProduct:categorical column with high variability; Missing values: '-', 'Missing', "" ; impute with a standard value ('Product not specified').\n"
                             "\t\tSales Person Name: categorical column; Missing values: '-', 'Missing', "" ; if the surname is not a missing value impute the mode of that column, otherwise with a standard value ('Name not specified').\n"
                             "\t\tSales Person Surname: categorical column; Missing values: '-', 'Missing', "" ; if the name is not a missing value impute the mode of that column, otherwise with a standard value ('Surname not specified').\n"
                             "\t\tBoxes Shipped: numerical column; Missing values: 0, 'nan', "" ; use a regressor to impute values (some possible features to use are Product and Amount($)).\n"
                             "\t\tAmount ($): numerical column; Missing values: 0, 'nan', "" ; use a regressor to impute values (some possible features to use are Product and Boxes Shipped).\n"
                             "\t\tCountry: categorical value; Missing values: '-', 'Missing', "" ; since this dataset has a very limited number of different values then impute with the mode.\n"
                             "3) Outlier detection and correction\n"
                             "\tDetection (consider columns with numerical values after imputation):\n"
                             "\t\tBoxes Shipped: since it is a numerical value, apply Median Absolute Deviation defined as: Z-Score = |x – median(x)| / mad(x). Considering a threshold of 2.5, the outliers are 24, 28, 28 and 29. Also values <6 are reported as outliers, but based on the context it is clear that with high probability they are correct values (it is common to buy small number of medicines)\n"
                             "\t\tAmount($): apply interquartile range method, no outlier is found.\n"
                             "\tCorrection: remove the real outliers and impute with the previous method.\n"
                             "4) Duplicate detection and correction\n"
                             "\tDetection:\n"
                             "\t\tExact duplicate: since there is only one pair of rows that have the same values column by column, the pair (7,23), there is only one exact duplicate.\n"
                             "\t\tNon-exact duplicate detection: define similarity measures for comparisons (i.e. Jaro-Winkler for Sales Person Name and Surname, Country and Product; Levenshtein for Date, Boxes Shipped and Amount($)) and define a threshold. If the combination of the values obtained by the comparison in pair is greater than the threshold, the tuples can be considered as duplicates."
                             "Question: Consider this dataset:\n{{csv_text}}\nCan you do data cleaning on it?\n"
                             "Answer: "
            ),
            QuestionPrompt(
                prompt_id=20,
                user_message="Consider this dataset:\n"
                             "flight_code, stops, departure_time, duration\n"
                             "001, one, Early_Morning, 1.30\n"
                             "002, two, Early_Afternoon, 360\n"
                             "022, two, Night, 4.50\n"
                             "019, zero, Afternoon_Early, 50\n"
                             "291, zero, Early_Morning, 1.30\n"
                             "After performing data standardization:\n"
                             "flight_code, stops, departure_time, duration(h)\n"
                             "001, 1, Early_Morning, 1.30\n"
                             "002, 2, Early_Afternoon, 6.00\n"
                             "022, 2, Night, 4.50\n"
                             "019, 0, Early_Afternoon, 0.50\n"
                             "291, 0, Early_Morning, 1.30\n\n"
                             
                             "Consider this dataset:\n"
                             "car_company_code, car_model_code, price, fuel_type\n"
                             "POR, CAYB, $72.200, Petrol\n"
                             "POR, GT3R, $241.300, Pet\n"
                             "VOL, PSAT, $40.000 - $45.000, Diesel\n"
                             "MAZ, BIAN, $22.000 - $26.000, Petrol\n"
                             "VOL, GTDI, $30.000 - $35.000, Diesel\n"
                             "After performing data standardization:\n"
                             "car_name_code, min_price($), max_price($), fuel_type\n"
                             "PORCAYB, $72.200, $72.200, Petrol\n"
                             "PORGT3R, $241.300, $241.300, Petrol\n"
                             "VOLPSAT, $40.000, $45.000, Diesel\n"
                             "MAZBIAN, $22.000, $26.000, Petrol\n"
                             "VOLGTDI, $30.000, $35.000, Diesel\n\n"
                             "Consider this dataset, called Master:\n{{csv_text}}\nPerform only data standardization on it."
            ),
            QuestionPrompt(
                prompt_id=21,
                user_message="Consider this dataset:\n"
                             "user_id, year, height(cm), gender\n"
                             "U431, 1987, 190, f\n"
                             "U855, 1945, 173, f\n"
                             "U732, 1062, 186, f\n" 
                             "U362, 1984, 130, m\n"
                             "U825, 1999, 167, f\n"
                             "U894, 2012, 174, m\n"
                             "U143, 2412, 181, f\n"
                             "U087, 1970, 244, f\n"
                             "U253, 1501, 87, m\n"
                             "U845, 1993, 159, m\n"
                             "After performing outlier detection, the following outliers are detected:\n"
                             "For year, with IQR method: 1062, 2412, 1501; with MAD method: 1062, 2412, 1501;\n"
                             "For height(cm), with IQR method: 130, 244, 87; With MAD method: 244, 87.\n\n"
                             "Consider this dataset:\n"
                             "patient,age,blood_pressure"
                             "B998, 25, 112\n"
                             "A221, 30, 115\n"
                             "V761, 35, 118\n"
                             "C091, 40, 122\n"
                             "F009, 45, 180\n"
                             "J081, 50, 129\n"
                             "Q112, 55, 132\n"
                             "R543, 60, 136\n"
                             "T948, 65, 210\n"
                             "L827, 70, 95\n"
                             "After performing outlier detection, the following outliers are detected:\n"
                             "For blood_pressure, with linear regression and MAD methods: 180, 210, 95; with IQR method: 180, 210.\n\n"
                             "Consider now the Master dataset after data standardization: perform only outlier detection on it."

            ),
            QuestionPrompt(
                prompt_id=22,
                user_message="Consider this dataset:\n"
                             "name, age, gender, occupation, city, weight(kg), height(cm), BMI\n"
                             ", 28, Male,, New York, 75, 180, 23.15\n"
                             "Jane Smith, 34, Female, Doctor, Los Angeles, 62, 99999, 22.77\n"
                             "missing, Johnson, 45, null, -, Chicago, 85, 175, -1\n"
                             "Emily Davis, -1, Female, Student,,nan, 160, 21.09\n"
                             "David Wilson, 0, Male, Artist,San Francisco, 78, 178, 24.61\n"
                             "The missing values are: '', 99999, missing, null, -, -1, 0,"
                             "After imputation (using median for age, mode for gender, deterministic relationships for weight(kg), height(cm), BMI, placeholder for the rest), the dataset becomes:\n"
                             "name, age, gender, occupation, city, weight(kg), height(cm), BMI\n"                             
                             "Unknown, 28, Male, Not specified, New York, 75, 180, 23.15\n"
                             "Jane Smith, 34, Female, Doctor, Los Angeles, 62, 165, 22.77\n"
                             "Unknown, 45, Male, Teacher, Chicago, 85, 175, 27.76\n"
                             "Emily Davis, 34, Female, Student, Not specified, 54, 160, 21.09\n"
                             "David Wilson, 34, Male, Artist, San Francisco, 78, 178, 24.61\n\n"
                             "Consider this dataset:\n"
                             "species,average_length(cm),average_weight(g),habitat,diet\n"
                             "Neon Tetra, 4, 0.5, Flakes\n"
                             "Betta splendens, 6, 2, Insects\n"
                             "Angelfish, 15,, Omnivore\n"
                             "null, 5, 0.6, Algae\n"
                             "Ghost Shrimp, 4, 0.3, missing\n"
                             "Goldfish, 25, 300, Insects\n"
                             "Corydoras panda, 5, 3, Detritus\n"
                             "Discus, 20, 200, Protein\n"
                             "Gourami, -, 5, Omnivore\n"
                             "Pleco, 30, 500, Algae\n"
                             "The missing values are: '', missing, null, -\n"
                             "After imputation (using random forest regressor for average_length(cm) and average_weight(g), mode for diet, placeholder for species), the dataset becomes:\n"
                             "species,average_length(cm),average_weight(g),habitat,diet\n"                             
                             "Neon Tetra, 4, 0.5, Flakes\n"
                             "Betta splendens, 6, 2, Insects\n"
                             "Angelfish, 15, 80, Omnivore\n"
                             "Unknown, 5, 0.6, Algae\n"
                             "Ghost Shrimp, 4, 0.3, Algae\n"
                             "Goldfish, 25, 300, Insects\n"
                             "Corydoras panda, 5, 3, Detritus\n"
                             "Discus, 20, 200, Protein\n"
                             "Gourami, 9.91, 5, Omnivore\n"
                             "Pleco, 30, 500, Algae\n\n"
                             "Consider the Master dataset after data standardization and outlier detection: perform data imputation on it."
            ),
            QuestionPrompt(
                prompt_id=23,
                user_message="Consider this dataset:\n"
                             "title, author, genre, pages, year\n"
                             "The Catcher in the Rye, J.D. Salinger, Classic, 277, 1951\n"
                             "1984 ,George Orwell, Dystopian, 328, 1949\n"
                             "To Kill a Mockingbird, Harper Lee, Classic, 281, 1960\n"
                             "Brave New World, Aldous Huxley, Dystopian, 268,1932\n"
                             "The Hobbit, J.R.R. Tolkien, Fantasy, 310, 1937\n"
                             "The Catcher in the Rye, J.D. Salinger, Classic, 277, 1951\n"
                             "The Catcher in the Rye, J.D. Salingher, Classic, 278, 1951\n"
                             "Pride and Prejudice, Jane Austen, Romance, 279, 1813\n"
                             "Fahrenheit 451, Ray Bradbury, Dystopian, 194, 1953\n"
                             "The Great Gatsby, F. Scott Fitzgerald, Classic, 180, 1925\n"

                             "The exact duplicates are lines 1 and 6. Using a record linkage approach, the non-exact duplicates are lines 1 and 7 and lines 6 and 7.\n"
                             "Consider this dataset:\n"
                             "course, track, semester, #students\n"
                             "Mathematical Analysis I, Mathematical Engineering, 1, 300\n"
                             "Mathematical Analysis I, Computer Science, 2, 200\n"
                             "Mathematical Analysis II, Mathematical Engineering, 1, 200\n"
                             "Mathematical Analysis II, Mathematical Engineering, 1, 500\n"
                             "Data and Information Quality, Computer Science, 1, 150\n"
                             "There are no exact duplicates. The non_exact duplicate are lines 3 and 4.\n"
                             "Consider the Master dataset after data standardization, outlier detection and data imputation: perform data deduplication on it."

            ),
        ]
    ),
    Task(
        name="data_profiling",
        prompts=[
            QuestionPrompt(
                prompt_id=1,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data profiling on it?"
            ),
            QuestionPrompt(
                prompt_id=2,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data profiling on it?", #mi serve per avere la versione aggiornata al nuovo modello senza perdere le vesrioni precedenti
            ),
            QuestionPrompt(
                prompt_id=3,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data profiling on it?",
                system_message="The next task requires the following actions: 1) Infer the context of the dataset; 2) calculate and present useful statistics about the dataset; 3) calculate and present useful statistics about each column",
            ),
            QuestionPrompt(
                prompt_id=4,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data profiling on it?",
                system_message="Knowledge: Data profiling is the process of examining and analyzing data to understand its structure, content, and quality. It consists of 3 subtasks: cardinalities, value distribution and (Data types, patterns and domains)",
            ),
            QuestionPrompt(
                prompt_id=5,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data profiling on it?",
            ),
            QuestionPrompt(
                prompt_id=6,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data profiling on it? \nTo complete this task, you need to follow these steps:\n1) Providing information and statistics about the entire dataset and any correlation between columns.\n2) Single column analysis, that is, providing statistical measurements associated with the frequency distribution of data values (and patterns) within a single column (or data attribute), for each column. Numerical answers are preferable whenever they are possible",
            ),
            QuestionPrompt(
                prompt_id=7,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data profiling on it?\nTo complete this task, you need to follow these steps:\n1) Providing statistics about the entire dataset, like domain classification, number of rows and columns, total number of missing values, number of exact duplicate, candidate UCC and correlation between columns.\n2) Providing statistic about each single columns, like data type, number of missing values, number of distinct values, domain classification, frequency of each values. If the column is numerical, provide numerically also mathematical statistics like mean, median, range, minimum, maximum, variance, quartiles.\n3) Providing functional and relaxed dependencies.",
            ),
            QuestionPrompt(
                prompt_id=8,
                user_message="Given a dataset, list all the operations required to perform data profiling on it.",
            ),
            QuestionPrompt(
                prompt_id=9,
                user_message="Consider this dataset:\n{{csv_text}}\nPerform the following operations on it:\n{{answer_text}}"
            ),
            QuestionPrompt(
                prompt_id=20,
                user_message="Consider this dataset:\n"
                             "code, artist, name, year, museum, city\n"
                             "25987, Leonardo da Vinci, Mona Lisa, 1503, Louvre Museum, Paris\n"
                             "63524, Vincent van Gogh, The Starry Night,1889 ,Museum of Modern Art, New York\n"
                             "38245, Michelangelo ,David, 1504, Galleria dell'Accademia, Florence\n"
                             "57392, Pablo Picasso, Les Demoiselles d'Avignon, 1907, Museum of Modern Art, New York\n"
                             "11123, Johannes Vermeer, Girl with a Pearl Earring, 1665, Mauritshuis, The Hague\n"
                             "25987, Leonardo da Vinci, Mona Lisa, 1503, Louvre Museum, Paris\n"
                             "66543, Michelangelo, The Creation of Adam, 1512, Sistine Chapel, Vatican City\n"
                             ""
                             "After performing data profiling at high level, we get the following information:\n"
                             "Domain classification: the dataset contains information about individual art objects\n"
                             "Number of columns: 6\n"
                             "Number of rows: 7\n"
                             "Number of exact duplicates: 1\n"
                             "Number of missing values: 0\n"
                             "Consider this dataset:\n"
                             "user_id, first_name,last_name,birth_year,height_cm,weight_kg,hours_exercise_per_week\n"
                             "U001,,Rossi,1985,null,75,3\n"
                             "U002,Laura,Bianchi,1990,165,60,5\n"
                             "U003,Laura,,-,170,68,2\n"
                             "U004,Andrea,Neri,1995,182,80,4\n"
                             "U005,Matteo,missing,1982,175,77,6\n"
                             "U006,Matteo,Ferri,1993,160,55,-\n"
                             "U007,Luca,Conti,1993,180,78,1\n"
                             "U008,nan,Moretti,1980,168,missing,999999\n"
                             "U009,Davide,Conti,1980,nan,85,3\n"
                             "U010,Davide,Conti,1980,162,58,5\n"
                             "After performing data profiling at high level, we get the following information:\n"
                             "Domain classification: the dataset contains information about individual art objects\n"
                             "Number of columns: 7\n"
                             "Number of rows: 10\n"
                             "Number of exact duplicates: 0\n"
                             "Number of missing values: 10\n"
                             "Possible UUC: user_id, [first_name,last_name,birth_year,height_cm,weight_kg]\n"
                             "Correlation analysis:\n"
                             "                        | birth_year | height_cm | weight_kg | hours_exercise_per_week |\n"
                             "-----------------------------------------------------------------------------------------\n"
                             "birth_year              |   1.000000 |   0.663266 |   0.505884 |            -0.642944    |\n"
                             "height_cm               |   0.663266 |   1.000000 |   0.978098 |            -0.521186    |\n"
                             "weight_kg               |   0.505884 |   0.978098 |   1.000000 |            -0.397178    |\n"
                             "hours_exercise_per_week |  -0.642944 |  -0.521186 |  -0.397178 |             1.000000    |\n\n"
                           
                             "Consider this dataset, called Master:\n{{csv_text}}\nCan you do data profiling, only at high level, on it?"

            ),
            QuestionPrompt(
                prompt_id=21,
                user_message="Consider this dataset:\n"
                             "code, artist, name, year, museum, city\n"
                             "25987, Leonardo da Vinci, Mona Lisa, 1503, Louvre Museum, Paris\n"
                             "63524, Vincent van Gogh, The Starry Night, 1889, Museum of Modern Art, New York\n"
                             "38245, Michelangelo, David, 1504, Galleria dell'Accademia, Florence\n"
                             "57392, Pablo Picasso, Les Demoiselles d'Avignon, 1907, Museum of Modern Art, New York\n"
                             "11123, Johannes Vermeer, Girl with a Pearl Earring, 1665, Mauritshuis, The Hague\n"
                             "66543, Michelangelo, The Creation of Adam, 1512, Sistine Chapel, Vatican City\n"
                             "After performing single column analysis, we get the following information:\n"
                             "code:\n"
                             "Domain classification: Code that identify the object of art\n"
                             "Datatype: String\n"
                             "Number of missing values: 0\n"
                             "Number of distinct values: 6\n"
                             "Histogram: 25987 1, 63524 1, 38245 1, 57392 1, 11123 1, 66543 1\n"
                             "artist:\n"
                             "Domain classification: Name of the artist\n"
                             "Datatype: String\n"
                             "Number of missing values: 0\n"
                             "Number of distinct values: 6\n"
                             "Histogram: Michelangelo 2, Leonardo da Vinci 1, Vincent van Gogh 1, Pablo Picasso 1, Johannes Vermeer 1\n"
                             "name:\n"
                             "Domain classification: Name of the object of art\n"
                             "Datatype: String\n"
                             "Number of missing values: 0\n"
                             "Number of distinct values: 6\n"
                             "Histogram: Mona Lisa 1, The Starry Night 1, David 1, Les Demoiselles d'Avignon 1, Girl with a Pearl Earring 1, The Creation of Adam 1\n"
                             "year:\n"
                             "Domain classification: Year of creation of the object of art\n"
                             "Datatype: Integer\n"
                             "Number of missing values: 0\n"
                             "Number of distinct values: 6\n"
                             "Minimum: 1503\n"
                             "Maximum: 1907\n"
                             "Mean: 1663.333\n"
                             "Variance: 30716.222\n"
                             "Median: 1588.5\n"
                             "Q1: 1506 - Q2: 1588.5  - Q3: 1833\n"
                             "museum:\n"
                             "Domain classification: Name of the museum where the object of art is located\n"
                             "Datatype: String\n"
                             "Number of missing values: 0\n"
                             "Number of distinct values: 5\n"
                             "Histogram: Museum of Modern Art 2, Louvre Museum 1, Galleria dell'Accademia 1, Mauritshuis 1, Sistine Chapel 1\n"
                             "city:\n"
                             "Domain classification: Location of the museum where the object of art is located\n"
                             "Datatype: String\n"
                             "Number of missing values: 0\n"
                             "Number of distinct values: 5\n"
                             "Histogram: New York 2, Paris , Florence 1, The Hague 1, Vatican City 1\n\n"
                             
                             "Consider this dataset:\n"                         
                             "user_id,first_name,last_name,birth_year,height_cm,weight_kg,hours_exercise_per_week\n"
                             "U001,,Rossi,1985,null,75,3\n"
                             "U002,Laura,Bianchi,1990,165,60,5\n"
                             "U003,Laura,,-,170,68,2\n"
                             "U004,Andrea,Neri,1995,183,80,4\n"
                             "U005,Matteo,missing,1982,175,78,-\n"
                             "U006,Matteo,Ferri,1993,160,55,-\n"
                             "U007,Luca,Conti,1993,180,78,1\n"
                             "U008,nan,Moretti,1980,168,missing,999999\n"
                             "U009,Davide,Conti,1980,nan,85,3\n"
                             "U010,Davide,Conti,1980,162,58,5\n"
                             "After performing single column analysis, we get the following information:\n"                        
                             "user_id:\n"
                             "Domain classification: Code that identify the person\n"
                             "Datatype: String\n"
                             "Number of missing values: 0\n"
                             "Number of distinct values: 10\n"
                             "Histogram: U001 1,  U002 1, U003 1, U004 1, U005 1, U006 1, U007 1, U008 1, U009 1, U010 1,\n"
                             "first_name:\n"
                             "Domain classification: Name of the artist\n"
                             "Datatype: String\n"
                             "Number of missing values: 2\n"
                             "Number of distinct values: 7\n"
                             "Histogram: Laura 2, Matteo 2, Davide 2, nan 1, Andrea 1, Luca 1, '' 1\n" 
                             "last_name:\n"
                             "Domain classification: Surname of the artist\n"
                             "Datatype: String\n"
                             "Number of missing values: 2\n"
                             "Number of distinct values: 8\n"
                             "Histogram: Conti 3, Rossi 1, Bianchi 1, Neri 1, missing 1, Ferri 1, Moretti 1, '' 1\n"                        
                             "birth_year:\n"
                             "Domain classification: year of birth of the person\n"
                             "Datatype: Integer\n"
                             "Number of missing values: 1\n"
                             "Number of distinct values: 6\n"
                             "Minimum: 1980\n"
                             "Maximum: 1995\n"
                             "Mean: 1986.444\n"
                             "Variance: 35.358\n"
                             "Median: 1985\n"
                             "Q1: 1980 - Q2: 1985  - Q3: 1993\n"                             
                             "height_cm:\n"
                             "Domain classification: height of the person in centimeters\n"
                             "Datatype: Integer\n"
                             "Number of missing values: 2\n"
                             "Number of distinct values: 10\n"
                             "Minimum: 160\n"
                             "Maximum: 183\n"
                             "Mean: 170.375\n"
                             "Variance: 60.734\n"
                             "Median: 169\n"
                             "Q1: 164.25 - Q2: 169  - Q3: 176.25\n"                             
                             "weight_kg:\n"
                             "Domain classification: weight of the person in kilograms\n"
                             "Datatype: Integer\n"
                             "Number of missing values: 1\n"
                             "Number of distinct values: 9\n"
                             "Minimum: 55\n"
                             "Maximum: 85\n"
                             "Mean: 70.778\n"
                             "Variance: 105.061\n"
                             "Median: 75\n"
                             "Q1: 60 - Q2: 75  - Q3: 78\n"                             
                             "hours_exercise_per_week:\n"
                             "Domain classification: Number of hours of exercise per week\n"
                             "Datatype: Integer\n"
                             "Number of missing values: 3\n"
                             "Number of distinct values: 7\n"
                             "Minimum: 1\n"
                             "Maximum: 5\n"
                             "Mean: 3.285\n"
                             "Variance: 1.918\n"
                             "Median: 3\n"
                             "Q1: 2.5 - Q2: 3  - Q3: 4.5\n\n"
                             
                             "Consider the Master dataset, perform the single column analysis on it."

            ),
        ]
    ),
    Task(
        name="data_imputation",
        prompts=[
            QuestionPrompt(
                prompt_id=1,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data imputation on it?"
            ),
            QuestionPrompt(
                prompt_id=2,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data imputation on it? Let's think step by step."
            ),
            QuestionPrompt( #CoT
                prompt_id=3,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data imputation on it?",
                system_message="The next task requires the following actions: 1) identify which are the missing values, also in different formats; 2) understand if the value can be imputed or it is better to impute a placeholder; 3) suggest the best imputation technique for imputing.",
            ),
            QuestionPrompt(
                prompt_id=4,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data imputation on it?",
                system_message="Knowledge: Data imputation is the process of replacing missing data values in a dataset with estimated or substituted values. Some techniques for data imputation are: Next or Previous; Value K Nearest Neighbors; Maximum or Minimum Value; Missing Value Prediction; Most Frequent Value; Average or Linear Interpolation; Median Value; Placeholder",
            )
        ]
    ),
    Task(
        name="data_deduplication",
        prompts=[
            QuestionPrompt(
                prompt_id=1,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it?"
            ),
            QuestionPrompt(
                prompt_id=2,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it? Describe step by step your reasoning."  #One-shot CoT
            ),
            QuestionPrompt(
                prompt_id=3,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it?",
                system_message="Given these rows:"
                               "1) Luca, Moore, 25, Como;"
                               "2) Sara, Anderson, 25, Como;"
                               "3) Luca, Moore, 25, Como;"
                               "4) Lucas, Moore, 26, Como;"
                               "The duplicates are 1 and 3; the non-exact duplicates are 1 and 4, 3 and 4; the others are not duplicates at all", #"One-shot"

            ),
            QuestionPrompt(
                prompt_id=4,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it? Let's think step by step.",
                system_message="Given these rows:"
                               "1) Luca, Moore, 25, Como;"
                               "2) Sara, Anderson, 25, Como;"
                               "3) Luca, Moore, 25, Como;"
                               "4) Lucas, Moore, 26, Como;"
                               "The duplicates are 1 and 3; the non-exact duplicates are 1 and 4, 3 and 4; the others are not duplicates at all"
                               "Given these rows:"
                               "1) Rome, Italy, 00042;"
                               "2) Rome, Italy, 00042;"
                               "3) Rmoe, italy, 00042;"
                               "4) Como, Italy, 22100;"
                               "The duplicates are 1 and 2; the non-exact duplicates are 1 and 3, 2 and 3; the others are not duplicates at all", #Two-shot

            ),
            QuestionPrompt(
                prompt_id=5,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it?",
                system_message="Q: Consider this dataset:"
                               "1) Luca, Moore, 25, Como;"
                               "2) Sara, Anderson, 25, Como;"
                               "3) Luca, Moore, 25, Como;"
                               "4) Lucas, Moore, 26, Como;"
                               "A: The duplicates are 1 and 3 because all fields are equal; the non-exact duplicates are 1 and 4, 3 and 4 because the names are really similar and also the age, while others fields are equal; the others are not duplicates at all because names and surnames are substantially different", #"One-shot"

            ),
            QuestionPrompt(
                prompt_id=6,
                user_message="Generate 4 facts about data deduplication, considering exact matching and non-exact matching techniques. Now consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it applying the facts you stated before?",
            ),
            QuestionPrompt(
                prompt_id=7,
                user_message="Generate 4 facts about data deduplication, considering exact matching and non-exact matching techniques. Now consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it applying the facts you stated before?",
                system_message="You are a data expert, specialized in data cleaning. You will respond in the most accurate way, giving specific answers and providing complex answers if needed"
            ),
            QuestionPrompt(
                prompt_id=8,
                user_message="Generate 4 facts about data deduplication, considering exact matching and non-exact matching techniques. Now consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it applying the facts you stated before?",
                system_message="Imagine three different experts are answering this question. All experts will write down 1 step of their thinking,then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they leave. The question is.."
            ),
            QuestionPrompt(
                prompt_id=9,
                user_message="Consider exact matching and non-exact matching techniques. Now consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it?",
                system_message="Imagine three different experts are answering this question. All experts will write down 1 step of their thinking,then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they leave. The question is.."
            ),
            QuestionPrompt(
                prompt_id=10,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it?",
                system_message="The next task requires the following actions: 1) identify all duplicates based on exact matching; 2) identify all duplicates based on non-exact matching"
            ),
            QuestionPrompt(
                prompt_id=11,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data deduplication on it?",
                system_message="Knowledge: Duplicate detection is the process of identifying and potentially eliminating redundant or similar records within a dataset. In order to perform it, it is necessary to search both exact duplicates and non-exact duplicates"
            ),
        ]
    ),
    Task(
        name="outlier_detection",
        prompts=[
            QuestionPrompt(
                prompt_id=1,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do outlier detection on it?"
            ),
            QuestionPrompt(
                prompt_id=2,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data outlier detection on it? Describe step by step your reasoning."  #One-shot CoT
            ),

            QuestionPrompt(
                prompt_id=3,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do outlier detection on it?",
                system_message="Given this dataset:"
                               "1) 10, 29, 50, 90, 1110, 0.1, 0.01, 30, 20, 34, 82;"
                               "The outliers are 90, 1110, 0.01, 0.1, 82",
                # "One-shot"

            ),
            QuestionPrompt(
                prompt_id=4,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do outlier detection on it?",
                system_message="Given this dataset: 10, 29, 50, 90, 1110, 0.1, 0.01, 30, 20, 34, 82; The outliers are 90, 1110, 0.01, 0.1, 82\nGiven this dataset:3,2,3,1,4,1,1,2,3,4,7,5,7,1,3,2,2,7,8,9,10,2,1,2,1,1,11,12; the outliers are: 7,8,9,10,11,12",

            ),
            QuestionPrompt(
                prompt_id=5,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do outlier detection on it?"
            ),
            QuestionPrompt(
                prompt_id=6,
                user_message="Generate 4 facts about outlier detection. Now consider this dataset:\n{{csv_text}}\nCan you do outlier detection on it applying the facts you stated before?",
            ),
            QuestionPrompt(
                prompt_id=7,
                user_message="Generate 4 facts about outlier detection. Now consider this dataset:\n{{csv_text}}\nCan you do outlier detection on it applying the facts you stated before?",
                system_message="You are a data expert, specialized in data cleaning. You will respond in the most accurate way, giving specific answers and providing complex answers if needed"
            ),
            QuestionPrompt(
                prompt_id=8,
                user_message="Generate 4 facts about outlier detection. Now consider this dataset:\n{{csv_text}}\nCan you do outlier detection on it applying the facts you stated before?",
                system_message="Imagine three different experts are answering this question. All experts will write down 1 step of their thinking,then share it with the group. Then all experts will go on to the next step, etc. If any expert realises they're wrong at any point then they leave. The question is.."
            ),
        ]
    ),
    Task(
        name="data_wrangling",
        prompts=[
            QuestionPrompt(
                prompt_id=1,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data wrangling on it?"
            ),
            QuestionPrompt(
                prompt_id=2,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data wrangling on it?"
            ),
            QuestionPrompt(
                prompt_id=3,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data wrangling on it? Reason step by step and be the most accurate and detailed as possible"
            ),
            QuestionPrompt(
                prompt_id=4,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data wrangling on it?"
            ),
            QuestionPrompt(
                prompt_id=5,
                user_message=" Consider this dataset:\n{{csv_text}}\nCan you do data wrangling on it?"
            ),
            QuestionPrompt(
                prompt_id=7,
                user_message=":Consider this dataset:\n{{csv_text}}\nCan you do data wrangling on it? \nTo complete this task, you need to follow these steps:\n1) Merging columns.\n2) Splitting columns.\n3) Formatting and converting columns.\n4)Renaming columns, only if needed.\n5)Dropping columns.",
            ),
            QuestionPrompt(
                prompt_id=8,
                user_message="Given a dataset, list all the operations required to perform data wrangling on it.",
            ),
            QuestionPrompt(
                prompt_id=9,
                user_message="Consider this dataset:\n{{csv_text}}\nPerform the following operations on it:\n{{answer_text}}"
            ),
            QuestionPrompt(
                prompt_id=20,
                user_message="Consider this dataset:\n"
                             "user_id, age, mail_name, @, domain\n"
                             "A900, 20, arossi, @, gmail.com\n"
                             "D912, 21, mbianchi, @, gmail.com\n"
                             "P213, 24, save, @, outlook.com\n"
                             "G182, 42, omarro, @, outlook.com\n"
                             "S127, 58, lugi, @, gmail.com\n\n"
                             "After performing column merging and dropping pre-merging columns:\n"
                             "Consider this dataset:\n"
                             "user_id, age, mail\n"
                             "A900, 20, arossi@gmail.com\n"
                             "D912, 21, mbianchi@gmail.com\n"
                             "P213, 24, save@outlook.com\n"
                             "G182, 42, omarro@outlook.com\n"
                             "S127, 58, lugi@gmail.com\n\n"
                             
                             "Consider this dataset:\n"
                             "product_code, expiration_year, expiration_month\n"
                             "PKM123, 2026, 12\n"
                             "MON453, 2030, 08\n"
                             "APP843, 2029, 09\n"
                             "TAR456, 2028, 01\n"
                             "GXT196, 2034, 10\n"
                             "After performing column merging and dropping pre-merging columns:\n"
                             "product_code, expiration_date\n"
                             "PKM123, 2016/12\n"
                             "MON453, 2030/08\n"
                             "APP843, 2029/09\n"
                             "TAR456, 2028/01\n"
                             "GXT196, 2034/10\n\n"
                            
                             
                             "Consider this dataset, called Master:\n{{csv_text}}\nPerform only column merging on it, only for the columns where needed"
            ),
            QuestionPrompt(
                prompt_id=21,
                user_message="Consider this dataset:\n"
                             "client_id, height, weight, birthday\n"
                             "GOL492, 170.1cm, 70kg, 21-12-2000\n" 
                             "ASL921, 165cm, 67.2kg, 31-02-1999\n"
                             "MOK371, 6ft, 147.71lb, 04-07-1998\n"              
                             "IDN982, 1.762m, 87kg, 29-09-1999\n" 
                             "KOA339, 1.873m, 79kg, 11-03-2002\n"
                             "After performing column splitting and dropping pre-splitting columns:\n"
                             "client_id, height, height_unit, weight, weight_unit, birthday\n"
                             "GOL492, 1.701, cm, 70, kg, 21-12-2000\n"   
                             "ASL921, 1.65, cm, 67.2, kg, 31-02-1999\n"
                             "MOK371, 6, ft, 147.71, lb, 04-07-1998\n"
                             "IDN982, 1.762, m, 87, kg, 29-09-1999\n"
                             "KOA339, 1.873, m, 79, kg, 11-03-2002\n\n"
                             
                             "Consider this dataset:\n"
                             "person, subscription  \n"
                             "Mario Brambilla, basic, 30\n"
                             "John Smith, premium, 10 \n"
                             "Dalila Linda, premium, 8\n"
                             "Franco Volturi, basic, 21\n"
                             "Andrea Sani, basic, 3\n\n"
                             "After performing column splitting and dropping pre-splitting columns:\n"
                             "person_name, person_surname, subscription, remaining months\n"
                             "Mario, Brambilla, basic, 30\n"
                             "John, Smith, premium, 10\n"
                             "Dalila, Linda, premium, 8\n"
                             "Franco, Volturi, basic, 21\n"
                             "Andrea, Sani, basic, 3\n\n"
                             
                             "Consider Master dataset after column merging: perform only column splitting on it, only for the columns where needed."
            ),
            QuestionPrompt(
                prompt_id=22,
                user_message="Consider this dataset:\n"
                             "height, height_unit, weight, weight_unit\n"
                             " 170.1, cm, 70, kg\n"
                             " 165, cm, 67.2, kg\n"
                             " 6, ft, 147.71, lb\n"
                             " 1.762, m, 87, kg\n"
                             " 1.873, m, 79, kg\n\n"
                             "After performing conversion and formatting:\n"
                             "height, height_unit, weight, weight_unit\n"
                             " 1.70, m, 70.0, kg\n"
                             " 1.65, m, 67.2, kg\n"
                             " 1.83, m, 67.0, kg\n"
                             " 1.76, m, 87.0, kg\n"
                             " 1.87, m, 79.0, kg\n\n"
                             
                             "Consider this dataset:\n"
                             "product, cost, currency, shipping_date\n"
                             "123, 10, $, 19-09-2025\n"
                             "342, 21, $, 21-03-2025\n"
                             "234, 63, €, '18 September 2025'\n"
                             "754, 111.80, €, '28 July 2025'\n"
                             "862, 57.8, $, 30-05-2025\n"
                             "After performing conversion and formatting:\n"
                             "product, cost, monetary_unit, shipping_date\n"
                             "123, 10.00, $, 19-09-2025\n"
                             "342, 21.00, $, 21-09-2025\n"
                             "234, 73.81, $, 18-09-2025\n"
                             "754, 129.82, $, 28-07-2025\n"
                             "862, 57.80, $, 30-05-2025\n\n"
                             
                             "Consider Master dataset after column splitting and column merging: perform only conversion and formatting on it, only for the columns where needed."
            ),
            QuestionPrompt(
                prompt_id=23,
                user_message="Consider this dataset:\n"
                             "movie_title, director_firstname, director_lastName, RY\n"
                             "Inception, Christopher, Nolan, 2010\n"
                             "Pulp Fiction, Quentin, Tarantino, 1994\n"
                             "The Great Beauty, Paolo, Sorrentino, 2013\n"
                             "Parasite, Bong, Joon-ho, 2019\n"
                             "Amélie, Jean-Pierre, Jeunet, 2001\n"
                             "After performing column renaming:\n"
                             "movie, director_firstname, director_lastname, release_year\n"
                             "Inception, Christopher, Nolan, 2010\n"
                             "Pulp Fiction, Quentin, Tarantino, 1994\n"
                             "The Great Beauty, Paolo, Sorrentino, 2013\n"
                             "Parasite, Bong ,Joon-ho, 2019\n"
                             "Amélie, Jean-Pierre, Jeunet, 2001\n\n"
                             
                             "Consider this dataset:\n"
                             "height, height_unit, weight, weight_unit\n"
                             " 1.70, m, 70.0, kg\n"
                             " 1.65, m, 67.2, kg\n"
                             " 1.83, m, 67.0, kg\n"
                             " 1.76, m, 87.0, kg\n"
                             " 1.87, m, 79.0, kg\n"
                             "After performing column renaming:\n"
                             "height (m), height_unit, weight (kg), weight_unit\n"
                             " 1.70, m, 70.0, kg\n"
                             " 1.65, m, 67.2, kg\n"
                             " 1.83, m, 67.0, kg\n"
                             " 1.76, m, 87.0, kg\n"
                             " 1.87, m, 79.0, kg\n\n"

                             "Consider Master dataset after column splitting, column merging, conversion and formatting: perform only column renaming on it, only for the columns where needed."
            ),
            QuestionPrompt(
                prompt_id=24,
                user_message="Consider this dataset:\n"
                             "breed, type_of_coat, color, number_of_legs, owner_name, owner_surname\n"
                             "Labrador, short, yellow, 4, Sara, Don\n"
                             "Poodle, curly, white, 4, Paolo, Andretti\n"
                             "German Shepherd, medium, black and tan, 4, Samuele, Severini\n"
                             "Dachshund, short, brown, 4, Clara, Rignanese\n"
                             "Samoyed, long, white, 4, Rita, Gialli\n"
                             "After performing column dropping:\n"
                             "breed, type_of_coat, color, owner_name, owner_surname\n"
                             "Labrador, short, yellow, Sara, Don\n"
                             "Poodle, curly, white, Paolo, Andretti\n"
                             "German Shepherd, medium, black and tan, Samuele, Severini\n"
                             "Dachshund, short, brown, Clara, Rignanese\n"
                             "Samoyed, long, white, Rita, Gialli\n\n"        

                             "Consider this dataset:\n"
                             "height (m), height_unit, weight (kg), weight_unit\n"
                             " 1.70, m, 70.0, kg\n"
                             " 1.65, m, 67.2, kg\n"
                             " 1.83, m, 67.0, kg\n"
                             " 1.76, m, 87.0, kg\n"
                             " 1.87, m, 79.0, kg\n\n"
                             "After performing column dropping:\n"
                             "height (m), weight (kg)\n"
                             " 1.70, 70.0\n"
                             " 1.65, 67.2\n"
                             " 1.83, 67.0\n"
                             " 1.76, 87.0\n"
                             " 1.87, 79.0\n\n"

                             "Consider Master dataset after column splitting, column merging, conversion, formatting and renaming: perform only column dropping on it, only for the columns where needed."
            ),
        ]
    ),
    Task(
        name="data_standardization",
        prompts=[
            QuestionPrompt(
                prompt_id=1,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data standardization on it?"
            ),
        ]
    ),
    Task(
        name="dependency_discovery",
        prompts=[
            QuestionPrompt(
                prompt_id=1,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do dependency discovery on it?"
            ),
            QuestionPrompt(
                prompt_id=2,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do data dependency discovery on it?"
            ),
            QuestionPrompt(
                prompt_id=3,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do dependency discovery on it?",
                system_message="The next task requires the following actions: 1) search and find the functional dependencies; 2) search and find the relaxed dependencies. Don't make assumptions based on domain knowledge, infer the dependencies only from data"

            ),
            QuestionPrompt(
                prompt_id=4,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do dependency discovery on it? Describe step by step your reasoning.",  #One-shot CoT
                system_message="You are a data expert, specialized in data cleaning. You will respond in the most accurate way, giving specific answers and providing complex answers if needed. Focus your reasoning on finding exact functional dependencies and relaxed dependencies, applying definitions"

            ),
            QuestionPrompt(
                prompt_id=5,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do dependency discovery on it?"
            ),
            QuestionPrompt(
                prompt_id=6,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do dependency discovery on it? \nTo complete this task, you need to follow these steps:\n1) Identifying and providing minimal functional dependencies.\n2) Identifying and providing relaxed functional dependencies."
            ),
            QuestionPrompt(
                prompt_id=7,
                user_message="Consider this dataset:\n{{csv_text}}\nCan you do dependency discovery on it? \nTo complete this task, you need to follow these steps:\n1) Minimal functional dependencies discovery, that is, searching and providing relationships that hold for all the dataset.\n2) Minimal relaxed dependencies discovery, that is: searching and providing relationships that hold for a high percentage of the dataset; searching and providing relationships that hold if small value differences within the same column are accepted."
            ),
            QuestionPrompt(
                prompt_id=8,
                user_message="Given a dataset, list all the operations required to perform dependency discovery on it.",
            ),
            QuestionPrompt(
                prompt_id=9,
                user_message="Consider this dataset:\n{{csv_text}}\nPerform the following operations on it:\n{{answer_text}}"
            ),
            QuestionPrompt(
                prompt_id=20,
                user_message="Consider this dataset:\n"
                             "A, B, C\n"  
                             "1, 0, 4\n" 
                             "1, 2, 3\n" 
                             "1, 3, 4\n" 
                             "1, 0, 4\n" 
                             "4, 2, 1\n" 
                             "The minimal functional dependencies are: C->A, (A, B)->C.\n"
                             "Consider this dataset:\n"
                             "floor, room, activity, #seats\n"  
                             "1, 1A, sculpture, 20\n" 
                             "2, 3B, drawing, 50\n" 
                             "2, 2C, cooking, 30\n" 
                             "1, 1A, modeling, 30\n" 
                             "3, 1B, cooking, 20\n" 
                             "The minimal functional dependency is: room->floor.\n"
                             "Consider this dataset, called Master:\n{{csv_text}}\nCan you detect minimal functional dependencies?"
            ),
            QuestionPrompt(
                prompt_id=21,
                user_message="Consider this dataset:\n"
                             "col1, col2\n"
                             "1, Cat\n"
                             "1, Cat\n"
                             "2, Cat\n"
                             "2, Cat\n"
                             "2, Cat\n"
                             "3, Dog\n"
                             "3, Dog\n"
                             "3, Cat\n"
                             "3, Dog\n"
                             "3, Dog\n"
                             "There are no strict minimal functional dependencies.\n"
                             "Allowing at most a number of errors equal to 10% of the rows, the minimal relaxed dependency is col1->col2.\n\n"
                             "Consider this dataset:\n"
                             "A, B, C\n"  
                             "1, 2, 1\n" 
                             "2, 3, 3\n" 
                             "2, 3, 3\n" 
                             "2, 2, 3\n" 
                             "4, 2, 1\n"
                             "The minimal functional dependency is A->C.\n"
                             "Allowing at most a number of errors equal to 20% of the rows, the minimal relaxed dependencies are A->B, B->C, C->A, C->B .\n\n" 
                             "Consider the Master dataset, detect the minimal relaxed dependencies."
            ),
        ]
    ),
]

def get_prompt(task_name, prompt_id):
    for task in tasks:
        if task.name == task_name:
            for prompt in task.prompts:
                if str(prompt.id) == str(prompt_id):
                    return prompt

    raise ValueError("Prompt " + str(prompt_id) + " not found for task " + str(task_name))