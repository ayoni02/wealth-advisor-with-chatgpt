import openai 
import re
#from pprint import pprint as ppt
from uuid import uuid4
from time import time, sleep

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

openai.api_key = open_file('openaikey.txt')

sexs = [
    'male',
    'female'
]

salaries = range(10_000, 100_000, 10_000) # 9

returns = range(0, 10_000, 1_000) # 10

rents = range(0, 10_000, 1000) # 10

expenses = range(500, 1_000, 500) # 2

savings = range(0, 10_000, 1_000) # 10

goals = [
    'debts',
    'retirement',
    'education',
    'home',
    'business',
    'car',
    'vacation',
    'emergency',
    'other'
]


def gpt3_completion(prompt, engine='text-davinci-002', temp=1.0, top_p=1.0, 
                    token=1000, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdfasdf']):
    max_retries = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII', errors='ignore').decode()
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=token,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop
            )
            text = response['choices'][0]['text'].strip()
            # text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            save_file('gpt3_logs/%s' % filename, prompt + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry > max_retries:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)
    
if __name__ == '__main__':
    count = 0
    for saving in savings:
        for retur in returns:
            for salary in salaries:
                for goal in goals:
                    for rent in rents:
                        for expense in expenses:
                            for sex in sexs:
                                count += 1
                                prompt = open_file('prompt.txt').replace('<<SEX>>', sex).replace('<<SALARY>>', str(salary)).replace('<<RETURNS>>', str(retur)).replace('<<RENT>>', str(rent)).replace('<<EXPENSES>>', str(expense)).replace('<<SAVINGS>>', str(saving)).replace('<<GOALS>>', goal).replace('<<UUID>>', str(uuid4()))
                                print('\n\n', prompt)
                                completion = gpt3_completion(prompt)
                                outprompt = 'Sex: %s\nSalary: %s\nReturns for investment: %s\nRent/month: %s\nMonthly expenses: %s\nSavings: %s\nFinancial goals: %s\n\nAdvice: ' % (sex, salary, retur, rent, expense, saving, goal)
                                filename = (str(saving) + str(retur) + str(salary) + goal + str(rent) + str(expense) + sex).replace(' ', '').replace('&', '') + '%s.txt' % time()
                                save_file('prompts/%s' % filename, outprompt)
                                save_file('completions/%s' % filename, completion)
                                print('\n\n', outprompt)
                                print('\n\n', completion)
                                if count > 100_000:
                                    exit()
                #print(count)