import lexer
lexer.lex_test("main(){ int i = 10;}");
print(lexer.wordlist)
