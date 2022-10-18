\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}
\title{Blockbuster 2}

\date{\today} 

\author{Mvie Lovers \\
        bpl9915: Brett Lubberts\\
        cjs5232: Connor Stange\\
        jae9307: Jose Estevez\\
        afh9608: Adam Harnish\\
        prj7465: Patrick Johnson\\
        }

\begin{document}

\maketitle

\section{Introduction}
Design a command line interface that queries, modifies, etc. to db using Python as a language. Command line interface will support commands with options to execute necessary "business" operations. Will use GitHub to manage front-end file concurrency. SQL will be used as the primary language for the database. Database will store all required fields and have interrelated tables. Database will be able to be accessed by the front-end in order to supply command line outputs.\\
\\
Choices:\\
1. Tools\\
2. Recipes\\
3. Movies\\

\section{Design}
\subsection{Conceptual Model}
While implementing our EER diagram, we tried to keep our diagram specific yet complex. Each section of our diagram had unique ID's to keep from overlap, which is a lot easier to manage than using several specific keys. We also designed our diagram to be split up into different corners, which led to the diagram being much more visually aiding and organized.\\
Required attributes stated in design specification were added to corresponding entities (Users need email/password, tools need name)\\
IDs were created for all entities, and pre-existing attributes were used where possible (Barcode)\\
Additional attributes such as Expected{\_}Return{\_}Date and Last{\_}Status{\_}Change were added in order to allow functionality later needed in the front end
\begin{figure}[htb]
\begin{center}
\includegraphics[width=5in]{images/Mvie Lovers EER.png}
\caption{Mvie Lovers EER.pdf}
\label{SAMPLE FIGURE}
\end{center}
\end{figure}

\subsection{Reduction to tables}
Entities were listed and all attributes were added\\
IDs were underlined and foreign keys italicized\\
The one-to-many relationships Category $<->$ User and Tool $<->$ User were converted by adding a foreign key UID to Category and a foreign key UID to Tool\\
The other two many to many relationships were made into separate entities of corresponding names to hold all relationships\\\\
users(\underline{username}, password, first{\_}name, last{\_}name, email, creation{\_}date, last{\_}access{\_}date)\\
tools(\underline{barcode}, name, description, purchase{\_}date, purchase{\_}price, shareable, \textit{username})\\
categories(\underline{cid}, name, \textit{username})\\
tool{\_}reqs(\textit{\underline{username}}, \textit{\underline{barcode}}, \underline{date{\_}required}, duration, status, last{\_}status{\_}change, expected{\_}return{\_}date)\\
tool{\_}categs(\textit{\underline{barcode}}, \textit{\underline{cid}})\\

\subsection{Data Requirements/Constraints}
\textbf{Domains:}\\\\
users:\\
username varchar PRIMARY KEY\\
password varchar NOT NULL\\
first{\_}name varchar NOT NULL\\
last{\_}name varchar NOT NULL\\
email varchar NOT NULL\\
creation{\_}date timestamp NOT NULL\\
last{\_}access{\_}date timestamp NOT NULL\\\\
tools:\\
barcode char(12) PRIMARY KEY\\
name varchar NOT NULL\\
description varchar\\
purchase{\_}date date\\
purchase{\_}price decimal(8, 2) ($\ge$ 0)\\
shareable boolean\\
username varchar REFERENCES Users\\\\
categories:\\
cid serial PRIMARY KEY\\
name varchar NOT NULL\\
username varchar NOT NULL REFERENCES Users\\\\
tool{\_}reqs:\\
username varchar PRIMARY KEY REFERENCES users\\
barcode char(12) PRIMARY KEY REFERENCES tools\\
date{\_}required date PRIMARY KEY\\
duration interval ($>$ 0) NOT NULL\\
borrow{\_}status status (enum) $\in$ \{'Pending', 'Accepted', 'Denied'\} NOT NULL\\
last{\_}status{\_}change timestamp\\
expected{\_}return{\_}date date\\\\
tool{\_}categs:\\
barcode char(12) PRIMARY KEY REFERENCES tools\\
cid serial PRIMARY KEY REFERENCES categories\\\\
\subsection{Sample instance data}
users:\\
users('bpl9915', '1234', 'Brett', 'Lubberts', 'bpl9915@rit.edu', '2022-09-22 04:05:06', '2022-09-22 04:05:06')\\
users('Atom', 'password87', 'Adam', 'Harnish', 'afh9608@rit.edu', '2022-09-23 02:02:26', '2022-09-23 02:02:26')\\
users('The Woo', 'I<3Mvies', 'Jose', 'Estevez', 'jae9307@rit.edu', '2022-09-24 01:02:48', '2022-09-25 11:02:48')\\
users('8con', 'tools10', 'Connor', 'Stange', 'cjs5232@rit.edu', '2022-09-22 04:07:06', '2022-09-22 04:07:06')\\
users('rypat1', 'sfihdg', 'Patrick', 'Johnson', 'prj7465@rit.edu', '2022-10-02 11:05:06', '2022-10-03 11:05:06')\\\\
tools:\\
tools('927583055274', 'Dewalt Drill', 'Drill for drilling', '8/30/20', 99.99, true, 'bpl9915')\\
tools('839673820582', 'Sawzall', 'Portable saw that saws all things', '9/10/22', 87.99, true, 'bpl9915')\\
tools('384736491758', 'Screwdriver', 'Medium size phillips head', '4/30/20', 3.00, true, 'Atom')\\
tools('726540949172', 'Claw Hammer', 'Hammer with claw for removing nails', '2/4/16', 15.00, false, 'The Woo')\\
tools('819493857199', 'Mallet', 'Rubber mallet that can be used to hammer without causing damage', '8/16/21', 49.99, true, 'rypat1')\\\\
categories:\\
categories(1, 'Hammer', 'The Woo')\\
categories(2, 'Drill', 'bpl9915')\\
categories(3, 'Saw', '8con')\\
categories(4, 'Screwdriver', 'rypat1')\\
categories(5, 'Impact Driver', 'Atom')\\\\
tool requests:\\
tool{\_}reqs('bpl9915', '927583055274', '9/30/22', 10, 'Pending', NULL, NULL)\\
tool{\_}reqs('rypat1', '384736491758', '9/23/22', 1, 'Accepted', '9/23/22 12:00', '9/30/22')\\ 
tool{\_}reqs('bpl9915', '384736491758', '10/1/22', 7, 'Pending', NULL, NULL)\\
tool{\_}reqs('8con', '927583055274', '10/3/22', 3, 'Pending', NULL, NULL)\\
tool{\_}reqs('rypat1', '726540949172', '10/3/22', 8, 'Pending', NULL, NULL)\\\\
tool categories:\\
tool{\_}categs('819493857199', 4)\\
tool{\_}categs('927583055274', 2)\\
tool{\_}categs('927583055274', 3)\\
tool{\_}categs('839673820582', 1)\\
tool{\_}categs('819493857199', 1)\\
\section{Implementation}
Use this section to describe the overall implementation of your database. Include samples of SQL statements to create the tables (DDL statements) and a description of the ETL process, including examples of the SQL insert statements used to populate each table initially.

Include also sample of the SQL insert statements used in your application program to insert new data in the database. Finally, add an appendix of all the SQL statements created in your application during Phase 4 and a description of the indexes created to boost the performance of your application.\\\\
create table users\\
(\\
    username    varchar\\
        primary key,\\
    password    varchar   not null,\\
    first\_name  varchar   not null,\\
    last\_name   varchar   not null,\\
    email       varchar   not null,\\
    creation    timestamp not null,\\
    last\_access timestamp not null\\
);\\\\
create table tools\\
(\\
    barcode        char(12)\\
        primary key,\\
    name           varchar not null,\\
    description    varchar,\\
    purchase\_date  date,\\
    purchase\_price decimal(8, 2),\\
    shareable      bool,\\
    username       varchar not null\\
        references users (username),\\
    check (purchase\_price > 0)\\
);\\\\
create table categories\\
(\\
    cid      serial\\
        primary key,\\
    name     varchar not null,\\
    username varchar not null\\
        references users (username)\\
);\\\\
\section{Data Analysis}
\subsection{Hypothesis}
Use this section to state the objectives of your data analysis; what are the observations you are expecting to find. Note that your final
observations may end up differing from your proposal, that is also a valid result.
\subsection{Data Preprocessing}
Use this section to describe the preprocessing steps you have performed to prepare the data for the analytics. Preprocessing steps may include: data cleaning (e.g., filling missing values, fixing outliers), formatting the data (e.g., resolving issues like inconsistent abbreviations, multiples date format in the data), combining or splitting fields, add new information (data enrichness).

Explain how the data was extracted from the database for the analysis; if you used complex queries or views, or both.
\subsection{Data Analytics \& Visualization}
Use this section to explain the process/techniques used to analyze the data, use data visualization to present the results, and explain them.
\subsection{Conclusions}
Use this section to explain the conclusions drawn from your data analysis.\\
\section{Lessons Learned}
Use this section to describe the issues you faced during the project and how you overcame them. Also, describe what you learned during this effort; this section, like the others, plays a critical component in determining your final grade.\\

{\bf The next subsection is meant to provide you with some help in
  dealing with figures, tables and references, as these are sometimes
  hard for folks new to \LaTeX. Your figures and tables
  may be distributed all over your paper (not just here), as appropriate for your paper.

  Please delete the following subsection before you make any submissions!}

\subsection{Tables, Figures, and Citations/References}

Tables, figures, and references in technical
documents need to be presented correctly. As many students
are not familiar with using these objects, here is a quick
guide extracted from the ACM style guide.

\begin{table}
\centering
\caption{Feelings about Issues}
\label{SAMPLE TABLE}
\begin{tabular}{|l|r|l|} \hline
Flavor&Percentage&Comments\\ \hline
Issue 1 &  10\% & Loved it a lot\\ \hline
Issue 2 &  20\% & Disliked it immensely\\ \hline
Issue 3 &  30\% & Didn't care one bit\\ \hline
Issue 4 &  40\% & Duh?\\ \hline
\end{tabular}
\end{table}


First, note that figures in the report must be original, that is,
created by the student: please do not cut-and-paste figures from any
other paper or report you have read or website. Second, if you do need to include figures,
they should be handled as demonstrated here. State that
Figure~\ref{SAMPLE FIGURE} is a simple illustration used in the ACM
Style sample document. Never refer to the figure below (or above)
because figures may be placed by \LaTeX{} at any appropriate location
that can change when you recompile your source $.tex$
file. Incidentally, in proper technical writing (for reasons beyond
the scope of this discussion), table captions are above the table and
figure captions are below the figure. So the truly junk information
about flavors is shown in Table~\ref{SAMPLE TABLE}.

\begin{figure}[htb]
\begin{center}
\includegraphics[width=1.5in]{images/fly.jpg}
\caption{A sample black \& white graphic (JPG).}
\label{SAMPLE FIGURE}
\end{center}
\end{figure}

\section{Resources}
Include in this section the resources you have used in your project beyond the normal code development such as data sets or data analytic tools (i.e. Weka, R).
\end{document}
