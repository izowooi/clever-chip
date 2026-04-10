---
name: aliexpress-price-tracker
description: 특정 상품의 가격을 조회합니다.
---

클로드에 연결된 chrome 을 이용하여 아래의 url 에 접속하여 가격을 기록합니다.
기록된 가격은하나의 텍스트 파일에 한 줄씩 날짜와, 가격, 상품명을 기록하여 추후 DB 에사용되도록 구조화를 해서 진행합니다.


1. 브라우저로 https://ko.aliexpress.com/item/1005011667770571.html 에 접속
2. 해당 페이지에서 상품과, 가격 등의 정보를 취득합니다.
3. ~/claude/aliexpress-price 에 타임스탬프와 함께 필요한 정보들을 저장합니다. (기존 데이터에 append)
4. 이전 데이터에 이어서 ~/claude/aliexpress-price/price.md 에 기록
5. 작업을 마친후에는 탭그룹을 닫아주세요.

빈도: Every 6 hours
모델: Claude Sonnet (토큰 절약)
Working folder: ~/claude/aliexpress-price/
