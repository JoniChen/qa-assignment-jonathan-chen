# Design choices 

## Language and Framework 

I have chosen to use python and playwright for this task. After years of using java and selenium , the last few years i have switched entirely to python and playwright.

I love python for its simplicity , the syntax is much more readable , and it is typeless and forgiving as opposed to java which is not. 

Selenium is a very popular framework to this day , but it is old and slow and takes many code lines sometimes to acheive simple tasks. 
That is why i like playwright and the direction they are taking , it has many usefull features out of the box like autowaits and parallel , it is very fast and lightweight.

The only time i can see why using selenium would be better is only if legacy tests are already written with selenium and the job is to increase test number. 
The same for java if a comapny needs to write tests in the same project as the product code and that code is java then i will write the tests in java. 

Since i am using python the natural choice for test runner is pytest and for api the requests library

## Anti flakiness strategy
What i believe is a good startegy - 
1. Stable selectors like data-test-id instead of brittle xpath / css - i have no problem to own this end to end including changing the client repo source code myself in order to have better locators where not available instead of waiting for client team
2. No hard sleeps - i avoid time.sleep unless there is no alternative , instead i use playwright auto wait or explicit conditions
3. Retry policy
4. Detailed logs and traces

## What is important when scaling tests number
At scale , anti flakiness is less about adding waits and more about discipline : stable selectors , isolated tests , reliable environment and fast feedback

## Reporting and triage 
If a test fails at night , we will see a clear text error message , a screenshot or video showing how it got there , and a log trace of what went on with the dom or network



