# Maintainability (CISQ / ISO/IEC 5055)

Source: CWE 5.0 (2026-10-28), view CWE-1305 "CISQ Quality Measures (2020)", grouping CWE-1307. © The MITRE Corporation, CWE Terms of Use. Cite as `CWE-<id>`.
These are the weaknesses the CISQ measures (published as ISO/IEC 5055:2021) count for Maintainability.
`(also …)` = the weakness is counted in another CISQ characteristic too.

- **CWE-407** Inefficient Algorithmic Complexity — An algorithm in a product has an inefficient worst-case computational complexity that may be detrimental to system performance and can be triggered by an attacker, typically using crafted manipulations that ensure that the worst case is being reached.
- **CWE-478** Missing Default Case in Multiple Condition Expression — The code does not have a default case in an expression with multiple conditions, such as a switch statement.
- **CWE-480** Use of Incorrect Operator — The product accidentally uses the wrong operator, which changes the logic in security-relevant ways. *(also Reliability, Security)*
- **CWE-484** Omitted Break Statement in Switch — The product omits a break statement within a switch or similar construct, causing code associated with multiple conditions to execute. This can cause problems when the programmer only intended to execute code associated with one condition. *(also Reliability)*
- **CWE-561** Dead Code — The product contains dead code, which can never be executed.
- **CWE-570** Expression is Always False — The product contains an expression that will always evaluate to false. *(also Security)*
- **CWE-571** Expression is Always True — The product contains an expression that will always evaluate to true. *(also Security)*
- **CWE-783** Operator Precedence Logic Error — The product uses an expression in which operator precedence causes incorrect logic to be used. *(also Security)*
- **CWE-1041** Use of Redundant Code — The product has multiple functions, methods, procedures, macros, etc. that contain the same code, i.e., the code has been copied or duplicated.
- **CWE-1045** Parent Class with a Virtual Destructor and a Child Class without a Virtual Destructor — A parent class has a virtual destructor method, but the parent has a child class that does not have a virtual destructor. *(also Reliability)*
- **CWE-1047** Modules with Circular Dependencies — The product contains modules in which one module has references that cycle back to itself, i.e., there are circular dependencies.
- **CWE-1048** Invokable Control Element with Large Number of Outward Calls — The code contains callable control elements that contain an excessively large number of references to other application objects external to the context of the callable, i.e. a Fan-Out value that is excessively large.
- **CWE-1051** Initialization with Hard-Coded Network Resource Configuration Data — The product initializes data using hard-coded values that act as network resource identifiers. *(also Reliability)*
- **CWE-1052** Excessive Use of Hard-Coded Literals in Initialization — The product initializes a data element using a hard-coded literal that is not a simple integer or static constant element.
- **CWE-1054** Invocation of a Control Element at an Unnecessarily Deep Horizontal Layer — The code at one architectural layer invokes code that resides at a deeper layer than the adjacent layer, i.e., the invocation skips at least one layer, and the invoked code is not part of a vertical utility layer that can be referenced from any horizontal layer.
- **CWE-1055** Multiple Inheritance from Concrete Classes — The product contains a class with inheritance from more than one concrete class.
- **CWE-1062** Parent Class with References to Child Class — The code has a parent class that contains references to a child class, its methods, or its members.
- **CWE-1064** Invokable Control Element with Signature Containing an Excessive Number of Parameters — The product contains a function, subroutine, or method whose signature has an unnecessarily large number of parameters/arguments.
- **CWE-1074** Class with Excessively Deep Inheritance — A class has an inheritance level that is too high, i.e., it has a large number of parent classes.
- **CWE-1075** Unconditional Control Flow Transfer outside of Switch Block — The product performs unconditional control transfer (such as a "goto") in code outside of a branching structure such as a switch block.
- **CWE-1079** Parent Class without Virtual Destructor Method — A parent class contains one or more child classes, but the parent class does not have a virtual destructor method. *(also Reliability)*
- **CWE-1080** Source Code File with Excessive Number of Lines of Code — A source code file has too many lines of code.
- **CWE-1084** Invokable Control Element with Excessive File or Data Access Operations — A function or method contains too many operations that utilize a data manager or file resource.
- **CWE-1085** Invokable Control Element with Excessive Volume of Commented-out Code — A function, method, procedure, etc. contains an excessive amount of code that has been commented out within its body.
- **CWE-1086** Class with Excessive Number of Child Classes — A class contains an unnecessarily large number of child classes.
- **CWE-1087** Class with Virtual Method without a Virtual Destructor — A class contains a virtual method, but the method does not have an associated virtual destructor. *(also Reliability)*
- **CWE-1090** Method Containing Access of a Member Element from Another Class — A method for a class performs an operation that directly accesses a member element from another class.
- **CWE-1095** Loop Condition Value Update within the Loop — The product uses a loop with a control flow condition based on a value that is updated within the body of the loop.
