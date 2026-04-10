---
name: diablo-4-world-boss-schedule-scraper
description: 디아블로4 월드보스 시간표 사이트에서 데이터 수집
---

1. 브라우저로 https://helltides.com/schedule 에 접속
2. 해당 페이지에는 World Boss, Helltide, Legion 이렇게 3개의 탭이 있습니다.
3. World Boss, Helltide 만 활성화 되어있어요.
4. Helltide 를 한 번 클릭하면 World Boss ( 월드보스 ) 만 남기 때문에 기록하기 쉽습니다.
5. 이렇게 표시된 월드보스의 시간을 기록합니다.
6. 다음 정보를 추출: 보스 이름, 출현 시간
7. ~/diablo4/worldboss_data.json 에 타임스탬프와 함께 저장 (기존 데이터에 append)
8. 이전 데이터와 비교해서 변경사항이 있으면 ~/diablo4/changes.md 에 기록
9. 작업을 마친후에는 탭그룹을 닫아주세요.

빈도: Every 6 hours