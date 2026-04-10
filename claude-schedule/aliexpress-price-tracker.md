---
name: aliexpress-price-tracker
description: AliExpress 상품 가격을 주기적으로 조회하여 CSV에 기록합니다.
---

## Task

Chrome으로 아래 URL에 접속하여 상품 가격 정보를 수집하고 CSV 파일에 append 합니다.

- URL: https://ko.aliexpress.com/item/1005011667770571.html

## Steps

1. 브라우저로 URL 접속
2. 페이지에서 상품명, 현재 가격, 원래 가격, 할인율, 통화 정보 추출
3. 아래 CSV 형식으로 `~/claude/aliexpress-price/price_history.csv`에 append
4. 파일이 없으면 헤더 포함하여 새로 생성
5. 완료 후 탭 닫기

## CSV Schema

timestamp,product_name,price,original_price,discount_pct,currency,url,status

- `timestamp`: ISO 8601 (예: `2026-04-10T19:34:22+09:00`)
- `price`, `original_price`: 숫자만 (콤마 제거)
- `discount_pct`: 소수점 (예: `20.1`)
- `status`: `OK` 또는 에러 시 `ERROR:<reason>`

## Error Handling

- 페이지 로딩 실패 또는 가격 미노출 시: status를 `ERROR:page_load_failed` 등으로 기록하고 price는 빈 값
- 기존 파일 손상 시: `.bak` 백업 후 새로 기록

## Settings

- 빈도: Every 6 hours
- 모델: Claude Sonnet
- Working folder: ~/claude/aliexpress-price/