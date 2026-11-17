# Reliability (CISQ / ISO/IEC 5055)

Source: CWE 5.0 (2026-10-28), view CWE-1305 "CISQ Quality Measures (2020)", grouping CWE-1306. © The MITRE Corporation, CWE Terms of Use. Cite as `CWE-<id>`.
These are the weaknesses the CISQ measures (published as ISO/IEC 5055:2021) count for Reliability.
`(also …)` = the weakness is counted in another CISQ characteristic too.

- **CWE-119** Improper Restriction of Operations within the Bounds of a Memory Buffer — The product performs operations on a memory buffer, but it reads from or writes to a memory location outside the buffer's intended boundary. *(also Security)*
- **CWE-170** Improper Null Termination — The product does not terminate or incorrectly terminates a string or array with a null character or equivalent terminator.
- **CWE-252** Unchecked Return Value — The product does not check the return value from a method or function. *(also Security)*
- **CWE-390** Detection of Error Condition Without Action — The product detects a specific error, but takes no actions to handle the error.
- **CWE-394** Unexpected Status Code or Return Value — The product does not properly check when a function or operation returns a value that is legitimate for the function, but is not expected by the product.
- **CWE-404** Improper Resource Shutdown or Release — The product does not release or incorrectly releases a resource before it is made available for re-use. *(also Efficiency, Security)*
- **CWE-424** Improper Protection of Alternate Path — The product does not sufficiently protect all possible paths that a user can take to access restricted functionality or resources. *(also Efficiency, Security)*
- **CWE-459** Incomplete Cleanup — The product does not properly "clean up" and remove temporary or supporting resources after they have been used.
- **CWE-476** NULL Pointer Dereference — The product dereferences a pointer that it expects to be valid but is NULL.
- **CWE-480** Use of Incorrect Operator — The product accidentally uses the wrong operator, which changes the logic in security-relevant ways. *(also Maintainability, Security)*
- **CWE-484** Omitted Break Statement in Switch — The product omits a break statement within a switch or similar construct, causing code associated with multiple conditions to execute. This can cause problems when the programmer only intended to execute code associated with one condition. *(also Maintainability)*
- **CWE-562** Return of Stack Variable Address — A function returns the address of a stack variable.
- **CWE-595** Comparison of Object References Instead of Object Contents — The product compares object references instead of the contents of the objects themselves, preventing it from detecting equivalent objects.
- **CWE-662** Improper Synchronization — The product utilizes multiple threads, processes, components, or systems to allow temporary access to a shared resource that can only be exclusive to one process at a time, but it does not properly synchronize these actions, which might cause simultaneous accesses of this resource by multiple threads or processes. *(also Security)*
- **CWE-665** Improper Initialization — The product does not initialize or incorrectly initializes a resource. *(also Security)*
- **CWE-672** Operation on a Resource after Expiration or Release — The product uses, accesses, or otherwise operates on a resource after that resource has been expired, released, or revoked. *(also Security)*
- **CWE-681** Incorrect Conversion between Numeric Types — When converting from one data type to another, such as long to integer, data can be omitted or translated in a way that produces unexpected values. If the resulting values are used in a sensitive context, then dangerous behaviors may occur. *(also Security)*
- **CWE-682** Incorrect Calculation — The product performs a calculation that generates incorrect or unintended results that are later used in security-critical decisions or resource management. *(also Security)*
- **CWE-703** Improper Check or Handling of Exceptional Conditions — The product does not properly anticipate or handle exceptional conditions that rarely occur during normal operation of the product.
- **CWE-704** Incorrect Type Conversion or Cast — The product does not correctly convert an object, resource, or structure from one type to a different type.
- **CWE-758** Reliance on Undefined, Unspecified, or Implementation-Defined Behavior — The product uses an API function, data structure, or other entity in a way that relies on properties that are not always guaranteed to hold for that entity.
- **CWE-835** Loop with Unreachable Exit Condition — The product contains an iteration or loop with an exit condition that cannot be reached, i.e., an infinite loop. *(also Security)*
- **CWE-908** Use of Uninitialized Resource — The product uses or accesses a resource that has not been initialized.
- **CWE-1045** Parent Class with a Virtual Destructor and a Child Class without a Virtual Destructor — A parent class has a virtual destructor method, but the parent has a child class that does not have a virtual destructor. *(also Maintainability)*
- **CWE-1051** Initialization with Hard-Coded Network Resource Configuration Data — The product initializes data using hard-coded values that act as network resource identifiers. *(also Maintainability)*
- **CWE-1066** Missing Serialization Control Element — The product contains a serializable data element that does not have an associated serialization method.
- **CWE-1070** Serializable Data Element Containing non-Serializable Item Elements — The product contains a serializable, storable data element such as a field or member, but the data element contains member elements that are not serializable.
- **CWE-1077** Floating Point Comparison with Incorrect Operator — The code performs a comparison such as an equality test between two float (floating point) values, but it uses comparison operators that do not account for the possibility of loss of precision.
- **CWE-1079** Parent Class without Virtual Destructor Method — A parent class contains one or more child classes, but the parent class does not have a virtual destructor method. *(also Maintainability)*
- **CWE-1082** Class Instance Self Destruction Control Element — The code contains a class instance that calls the method or function to delete or destroy itself, e.g., use of "delete this" in C++.
- **CWE-1083** Data Access from Outside Expected Data Manager Component — The product is intended to manage data access through a particular data manager component such as a relational or non-SQL database, but it contains code that performs data access operations without using that component.
- **CWE-1087** Class with Virtual Method without a Virtual Destructor — A class contains a virtual method, but the method does not have an associated virtual destructor. *(also Maintainability)*
- **CWE-1088** Synchronous Access of Remote Resource without Timeout — The code has a synchronous call to a remote resource, but there is no timeout for the call, or the timeout is set to infinite.
- **CWE-1098** Data Element containing Pointer Item without Proper Copy Control Element — The code contains a data element with a pointer that does not have an associated copy or constructor method.
