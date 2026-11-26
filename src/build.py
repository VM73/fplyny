src=open('app.html',encoding='utf-8').read()
src=src.replace('/*QUESTIONS*/',open('questions.js',encoding='utf-8').read()).replace('/*OKRUHY*/',open('okruhy.js',encoding='utf-8').read()).replace('/*CONTENT*/',open('content.js',encoding='utf-8').read()).replace('/*PREZ*/',open('prez.js',encoding='utf-8').read()).replace('/*PH*/',open('ph.js',encoding='utf-8').read()).replace('/*SAT*/',open('sat.json',encoding='utf-8').read())
open('fplyny.html','w',encoding='utf-8').write(src)
