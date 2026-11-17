# Efficiency (CISQ / ISO/IEC 5055)

Source: CWE 5.0 (2026-10-28), view CWE-1305 "CISQ Quality Measures (2020)", grouping CWE-1309. © The MITRE Corporation, CWE Terms of Use. Cite as `CWE-<id>`.
These are the weaknesses the CISQ measures (published as ISO/IEC 5055:2021) count for Efficiency.
`(also …)` = the weakness is counted in another CISQ characteristic too.

- **CWE-404** Improper Resource Shutdown or Release — The product does not release or incorrectly releases a resource before it is made available for re-use. *(also Reliability, Security)*
- **CWE-424** Improper Protection of Alternate Path — The product does not sufficiently protect all possible paths that a user can take to access restricted functionality or resources. *(also Reliability, Security)*
- **CWE-1042** Static Member Data Element outside of a Singleton Class Element — The code contains a member element that is declared as static (but not final), in which its parent class element is not a singleton class - that is, a class element that can be used only once in the 'to' association of a Create action.
- **CWE-1043** Data Element Aggregating an Excessively Large Number of Non-Primitive Elements — The product uses a data element that has an excessively large number of sub-elements with non-primitive data types such as structures or aggregated objects.
- **CWE-1046** Creation of Immutable Text Using String Concatenation — The product creates an immutable text string using string concatenation operations.
- **CWE-1049** Excessive Data Query Operations in a Large Data Table — The product performs a data query with a large number of joins and sub-queries on a large data table.
- **CWE-1050** Excessive Platform Resource Consumption within a Loop — The product has a loop body or loop condition that contains a control element that directly or indirectly consumes platform resources, e.g. messaging, sessions, locks, or file descriptors.
- **CWE-1057** Data Access Operations Outside of Expected Data Manager Component — The product uses a dedicated, central data manager component as required by design, but it contains code that performs data-access operations that do not use this data manager.
- **CWE-1060** Excessive Number of Inefficient Server-Side Data Accesses — The product performs too many data queries without using efficient data processing functionality such as stored procedures.
- **CWE-1067** Excessive Execution of Sequential Searches of Data Resource — The product contains a data query against an SQL table or view that is configured in a way that does not utilize an index and may cause sequential searches to be performed.
- **CWE-1072** Data Resource Access without Use of Connection Pooling — The product accesses a data resource through a database without using a connection pooling capability.
- **CWE-1073** Non-SQL Invokable Control Element with Excessive Number of Data Resource Accesses — The product contains a client with a function or method that contains a large number of data accesses/queries that are sent through a data manager, i.e., does not use efficient database capabilities.
- **CWE-1089** Large Data Table with Excessive Number of Indices — The product uses a large data table that contains an excessively large number of indices.
- **CWE-1091** Use of Object without Invoking Destructor Method — The product contains a method that accesses an object but does not later invoke the element's associated finalize/destructor method.
- **CWE-1094** Excessive Index Range Scan for a Data Resource — The product contains an index range scan for a large data table, but the scan can cover a large number of rows.
