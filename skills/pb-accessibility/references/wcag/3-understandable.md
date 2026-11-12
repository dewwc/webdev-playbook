# 3. Understandable

Source: W3C WCAG 2.2 (W3C Document License). Cite as `WCAG <num> (<level>)`, e.g. `WCAG 1.1.1 (A)`.
Level: A = minimum, AA = usual target (includes A), AAA = enhanced.
Each criterion links to its W3C *Understanding* page, which explains intent and sufficient techniques.

## 3.1 Readable

- **3.1.1 Language of Page** (A) — The default human language of each web page can be programmatically determined . [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html)
- **3.1.2 Language of Parts** (AA) — The human language of each passage or phrase in the content can be programmatically determined except for proper names, technical terms, words of indeterminate language, and words or phrases that have become part of the vernacular of the immediately surrounding text . [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts.html)
- **3.1.3 Unusual Words** (AAA) — A mechanism is available for identifying specific definitions of words or phrases used in an unusual or restricted way , including idioms and jargon . [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/unusual-words.html)
- **3.1.4 Abbreviations** (AAA) — A mechanism for identifying the expanded form or meaning of abbreviations is available. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/abbreviations.html)
- **3.1.5 Reading Level** (AAA) — When text requires reading ability more advanced than the lower secondary education level after removal of proper names and titles, supplemental content , or a version that does not require reading ability more advanced than the lower secondary education level, is available. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html)
- **3.1.6 Pronunciation** (AAA) — A mechanism is available for identifying specific pronunciation of words where meaning of the words, in context, is ambiguous without knowing the pronunciation. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/pronunciation.html)

## 3.2 Predictable

- **3.2.1 On Focus** (A) — When any user interface component receives focus, it does not initiate a change of context . [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/on-focus.html)
- **3.2.2 On Input** (A) — Changing the setting of any user interface component does not automatically cause a change of context unless the user has been advised of the behavior before using the component. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/on-input.html)
- **3.2.3 Consistent Navigation** (AA) — Navigational mechanisms that are repeated on multiple web pages within a set of web pages occur in the same relative order each time they are repeated, unless a change is initiated by the user. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/consistent-navigation.html)
- **3.2.4 Consistent Identification** (AA) — Components that have the same functionality within a set of web pages are identified consistently. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html)
- **3.2.5 Change on Request** (AAA) — Changes of context are initiated only by user request or a mechanism is available to turn off such changes. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/change-on-request.html)
- **3.2.6 Consistent Help** (A) *(new in 2.2)* — If a web page contains any of the following help mechanisms , and those mechanisms are repeated on multiple web pages within a set of web pages , they occur in the same order relative to other page content, unless a change is initiated by the user:
  - Human contact details;
  - Human contact mechanism;
  - Self-help option;
  - A fully automated contact mechanism. Note 1 Help mechanisms may be provided directly on the page, or may be provided via a direct link to a different page containing the information. Note 2 For this success criterion, "the same order relative to other page content" can be thought of as how the content is ordered when the page is serialized. The visual position of a help mechanism is likely to be consistent across pages for the same page variation (e.g., CSS break-point). The user can initiate a change, such as changing the page's zoom or orientation, which may trigger a different page variation. This criterion is concerned with relative order across pages displayed in the same page variation (e.g., same zoom level and orientation). [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/consistent-help.html)

## 3.3 Input Assistance

- **3.3.1 Error Identification** (A) — If an input error is automatically detected, the item that is in error is identified and the error is described to the user in text. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html)
- **3.3.2 Labels or Instructions** (A) — Labels or instructions are provided when content requires user input. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html)
- **3.3.3 Error Suggestion** (AA) — If an input error is automatically detected and suggestions for correction are known, then the suggestions are provided to the user, unless it would jeopardize the security or purpose of the content. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html)
- **3.3.4 Error Prevention (Legal, Financial, Data)** (AA) — For web pages that cause legal commitments or financial transactions for the user to occur, that modify or delete user-controllable data in data storage systems, or that submit user test responses, at least one of the following is true:
  - **Reversible**: Submissions are reversible.
  - **Checked**: Data entered by the user is checked for input errors and the user is provided an opportunity to correct them.
  - **Confirmed**: A mechanism is available for reviewing, confirming, and correcting information before finalizing the submission. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html)
- **3.3.5 Help** (AAA) — Context-sensitive help is available. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/help.html)
- **3.3.6 Error Prevention (All)** (AAA) — For web pages that require the user to submit information, at least one of the following is true:
  - **Reversible**: Submissions are reversible.
  - **Checked**: Data entered by the user is checked for input errors and the user is provided an opportunity to correct them.
  - **Confirmed**: A mechanism is available for reviewing, confirming, and correcting information before finalizing the submission. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-all.html)
- **3.3.7 Redundant Entry** (A) *(new in 2.2)* — Information previously entered by or provided to the user that is required to be entered again in the same process is either:
  - auto-populated, or
  - available for the user to select. Except when:
  - re-entering the information is essential ,
  - the information is required to ensure the security of the content, or
  - previously entered information is no longer valid. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)
- **3.3.8 Accessible Authentication (Minimum)** (AA) *(new in 2.2)* — A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless that step provides at least one of the following:
  - **Alternative**: Another authentication method that does not rely on a cognitive function test.
  - **Mechanism**: A mechanism is available to assist the user in completing the cognitive function test.
  - **Object Recognition**: The cognitive function test is to recognize objects.
  - **Personal Content**: The cognitive function test is to identify non-text content the user provided to the website. Note 1 "Object recognition" and "Personal content" may be represented by images, video, or audio. Note 2 Examples of mechanisms that satisfy this criterion include:
  - support for password entry by password managers to reduce memory need, and
  - copy and paste to reduce the cognitive burden of re-typing. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html)
- **3.3.9 Accessible Authentication (Enhanced)** (AAA) *(new in 2.2)* — A cognitive function test (such as remembering a password or solving a puzzle) is not required for any step in an authentication process unless that step provides at least one of the following:
  - **Alternative**: Another authentication method that does not rely on a cognitive function test.
  - **Mechanism**: A mechanism is available to assist the user in completing the cognitive function test. [Understanding](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-enhanced.html)
