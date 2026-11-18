from scanner import scan

# Test 1: Correct program
code1 = """analysis Grades
load students from "students.csv" with (name text, score number)
show students
end
"""

# Test 2: Correct program
code2 = """analysis Results
let total = 60
let average = 78.4
show average
end
"""

# Test 3: Correct program
code3 = """analysis Scores
let score = 85
if score >= 60 then
show "Passed"
otherwise
show "Failed"
done
end
"""

# Test 4: Lexical errors
code4 = """analysis Errors
let total = 12abc
show "Hello
end
"""

# Test 5: Lexical errors
code5 = """analysis Errors
let abcdefghijklmnopq = 10
show $5
end
"""

programs = [code1, code2, code3, code4, code5]

for i in range(len(programs)):
    tokens, errors = scan(programs[i])

    print("\nTEST", i + 1)

    print("TOKENS:")
    for token in tokens:
        print(token)

    print("TOTAL TOKENS:", len(tokens))

    print("ERRORS:")
    for error in errors:
        print(error)
