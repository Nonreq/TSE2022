# BiAn(狴犴)
![logo](BiAnLogo.png)

**BiAn** is a source code level code obfuscation tool developed for Solidity smart contracts. We will obfuscate the Solidity smart contract from the following three aspects:
+ **Layout obfuscation**. 
+ **Data flow obfuscation**. 
+ **Control flow obfuscation**. 

**BiAn**'s output: The contract after code obfuscation(.sol).

Limited by our technical level, the number of currently available tools and test cases, **BiAn** still has the following limitations:
1. **BiAn** cannot handle the solFile that contains multiple contracts.
2. **BiAn** cannot handle contracts that generate warnings at compile time. We use the local compiler (*solc*) to compile a contract. If a warning is generated when compiling the contract, the local compiler (*solc*) does not output the compilation result, which leads to errors in the following obfuscation steps.
3. **BiAn** may run abnormally when it confuses a contract. We welcome users to submit *bug* issues.

In addition, in the uploaded Bian file contains the source code of Bian、test dataset and the real dataset.

## Open source code used in **BiAn**
In the *Convert Integer Literals to Arithmetic Expressions* and *Split boolean variables* function, I use the code from project *Auto-Generate-Expression* (contributed by @threeworld et al). Since our requirements do not exactly match the project *Auto-Generate-Expression*'s function, I rewrite some code.

## License
This program is issued, reproduced or used under the permission of **MIT**. Please indicate the source when using.
