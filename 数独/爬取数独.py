import requests, re

def getSudoku(id:int) -> dict[str]:
    '''从TheSudoku.com获取题目'''
    url = f'https://www.thesudoku.com/easy-{id}-free-sudoku'
    try:
        requ = requests.get(url)
        html = requ.text
        txt = re.findall(f'"GridID":{id}'+r',"Difficulty".*?};', html)
        return '{'+txt[0][:-1]
    except:
        pass


if __name__ == '__main__':
    file=open('数独.txt', mode='w',encoding='utf-8')
    for i in range(200):
        sudo = getSudoku(i)
        if sudo:
            file.write(sudo+'\n')
    file.close()