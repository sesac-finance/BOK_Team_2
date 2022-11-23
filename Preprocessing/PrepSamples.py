import os
# os.environ['JAVA_HOME'] = 'D:\99.Dev\JDK'

# from konlpy.tag import Mecab
#
# mecab = Mecab(dicpath='C:/mecab/mecab-ko-dic')
# print(mecab.morphs('아 더빙 진짜 짜증 나네요 목소리'))
text= '금통위는 따라서 물가안정과 병행, 경기상황에 유의하는 금리정책을 펼쳐나가기로 했다고 밝혔다.'
from ekonlpy.tag import Mecab
import kss
mecab = Mecab()

print("pos", mecab.pos(text))
print()
print("morphs", mecab.morphs(text))
print()
print("nouns0pos", mecab.pos(' '.join(mecab.nouns(text))))
print()
print("lemmatize", mecab.lemmatize(text))
print()
print('sent_word' , mecab.sent_words(text))
print()
print(kss.split_sentences(text))

# sorted(vocab.items(), key=lambda x: x[1], reverse=True)

# from collections import Counter
# Counter.most_common('number')