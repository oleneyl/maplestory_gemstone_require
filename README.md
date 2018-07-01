# maplestroy_gemstone_require

Jemstone upgrade simulator.

------
Usage
------
1. open calc.py
2. Modify __main__'s User information : jobname & slot
3. python3 calc.py


----
Description
----

- core_jemstone.json
  
  This JSON file includes information about key : "Job Name" 's 
  - Total Enhancing core Types ( in "core_total")
  - main Enhance skill name ( in "main" list)
  - sub Enhance skill name (in "sub" list)
  - skill requirement that need to upgrade(in "vskill")
  - 1Lv cores that need to fresh game environment (Such as Spider in mirror, ...) (in useless_skill)


- calc.py

  This Python File simulates how much Jemstone will be required for achieve our core goal.
  
  - Important global variables
    
    - AIM_MAIN : main skill enhancement level goal.
    - AIM_SUB : sub skill enhancement level goal.
    - AIM_SKILL : V skill enhancement level goal.

  - Usage Tips
    
    class <User> generate user with given jobname & character level. You must generate User first, and then run User.simulate(). This function will return used jemstone for achieve goal use'd been setted in AIM_* global variable.
    In calc.py's code, it iterates 10 time ( = iter_num) & calculate average & standard deviation, print in STDOUT.
    

# 메이플스토리 젬스톤 계산기

젬스톤 코어강화 시뮬레이터 입니다.

------
사용법
------
1. calc.py 를 엽니다.
2. __main__ 으로 구분된 루틴 내의 User information 을 변경하세요 :  jobname & slot 을 원하는 직엄명과 slot 수로 변경합니다.
3. Jobname은 core_jemstone.json 내부의 keyy들을 참조하세요.
4. python3 calc.py 를 터미널에 입력합니다.


----
설명
----

- core_jemstone.json
  
  이 JSON 파일은 직업의 이름과, 각 직업에 대한 다음 정보를 담고 있습니다:
  - 총 강화 코어 개수 ("core_total"에 명시됨)
  - 주 강화 스킬명 ("main" 리스트 내부에 명시됨)
  - 부 강화 스킬명("sub" 리스트 내부에 명시됨)
  - 강화가 필요한 스킬의 개수("vskill"에 명시됨)
  - 원활한 플레이를 위해서 1Lv이지만 필요한 코어들(스파이더 인 미러와 같은) ("useless_skill" 에 명시됨)

- calc.py

  이 Python3 파일은 당신이 특정 직업&SLOT을 가지고 있을 때 소모해야 하는 평균 젬스톤 수를 계산해 줍니다.
  
  - 주요 전역 변수
    - AIM_MAIN : 주 코어들을 강화할 목표 레벨입니다.
    - AIM_SUB : 부 코어들을 강화할 목표 레벨입니다.
    - AIM_SKILL : V 스킬을 강화할 목표 레벨입니다.

  - 사용 팁
    
    class <User> 는 시뮬레이션에 적합한 가상의 유저를 주어진 직업명과 level을 받아서 생성합니다. 해당 프로그램의 실행을 위해서는 먼저 User를 생성합니다. 그리고, User.simulate() 함수를 실행합니다. 해당 함수는 AIM_* 전역변수에 설정된
    목표치를 달성하기 위해 소모한 젬스톤의 개수를 출력할 것입니다.
    calc.py 코드는 기본적으로 20회 ( = iter_num)의 시뮬레이션을 반복하고, 평균과 표준편차를 계산하여 당신의 STDOUT에 출력할 것입니다.