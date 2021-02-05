#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PyQt5.QtCore import QTime
# start 시간 측정
time = QTime.currentTime()
'''
사용자 머무르는 시간
'''
# 버튼이 클릭 되었을 때 -> def btnRun_cliked(self)함수 안에 들어가야함
# 사용자가 피드를 넘겼을 때
after = QTime.currentTime()

# 시간을 문자열로 변환하여 출력
start = time.toString()
end = after.toString()

# 시간을 시, 분, 초로 분해하여 정수로 변환
start_hour = int(start[:2])
end_hour = int(end[:2])
start_min = int(start[3:5])
end_min = int(end[3:5])
start_sec = int(start[6:])
end_sec = int(end[6:])

# "total == 머무른 시간" 을 계산 
total = 0
if start_sec > end_sec:
    end_min -= 1 
    end_sec+= 60
total += (end_sec - start_sec)
if start_min > end_min:
    end_hour -= 1
    end_min += 60
total += (end_min - start_min)* 60
total += (end_hour - start_hour) * 3600

print(total)


# In[ ]:


# 시간을 json 파일의 해당 이미지에다가 갱신
import json

# filename = 이미지 파일 이름 
json_data[filename]['time'] = total
# if 좋아요 버튼을 눌렀을때
if (json_data[filename]['likes']== 1):
    # 이미 한번 누른경우, 초기화 (0)
    json_data[filename]['likes'] = 0
else: # 좋아요가 처음인 경우에 좋아요 수 갱신
    json_data[filename]['likes']=1
    tag_name = json_data[filename]['tag']
    tag_json[tag_name]['likes'] += 1
    

