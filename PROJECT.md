# CNC-FC350 — Fixed-Column Box-Frame Mill

## 프로젝트 개요
- **프로젝트명**: CNC-FC350
- **타입**: Fixed-Column 박스프레임 CNC 밀링머신
- **가공영역**: 350×300×150mm (X×Y×Z)
- **외형**: ~750×650×600mm
- **프레임**: 6061-T6 알루미늄, CNC 외주 가공 후 자가 조립
- **정밀도**: ±0.01mm (외주 가공 기준)

## 핵심 콘셉트
> SolidWorks/Fusion360/Rhino로 설계 → 중국 CNC 가공업체에 도면 전송 → 정밀 가공 부품 수령 → 자가 조립

## 용도
- PCB 드릴링/밀링
- BOXCO 인클로저 패널 가공
- 플라네터리 기어 가공
- 정밀 기어 제작
- 기어축 가공 (4축 로터리)
- 알루미늄/황동 소형 부품

## 스펙 요약
| 항목 | 스펙 |
|------|------|
| 구조 | Fixed-Column 박스형 (최강 강성) |
| 가공영역 | 350×300×150mm |
| 프레임 재질 | 6061-T6, 20~25mm 두께, 아노다이징 |
| 리니어 레일 | HGR20 전축 (6레일, 12블록) |
| 볼스크류 | SFU1605 C7 XYZ |
| 스핀들 | 1.5kW 수냉 ER16, ∅65mm |
| 모터 | NEMA23 3.0Nm ×4 (XYZ+A) |
| 드라이버 | DM556 ×4 |
| 컨트롤러 | grblHAL STM32F446 |
| 4축 | K11-80 로터리 + 심압대 MT2 |
| 전원 | Mean Well RSP-750-48 + MDR-60-24 |
| 프레임 무게 | ~55kg |

## 파일 구조
```
~/Desktop/CNC-FC350/
├── PROJECT.md          ← 이 파일
├── cnc-fc350-3d.html   ← Phase 1: Three.js 3D 외관 뷰어
├── (Phase 2: Rhino Python 스크립트 — 각 플레이트별)
├── (Phase 3: Fusion 360 어셈블리 + 2D 도면)
└── (Phase 4: STEP + PDF → 공장 발주)
```

## GitHub
- **URL**: https://github.com/ebaek200/CNC-FC350-Fixed-Column-Mill

## sy-baek.shop
- **URL**: https://sy-baek.shop/cnc-fc350.html

## 외주 가공 업체 후보
- Shenzhen Huarui Century Technology (Made-in-China, Diamond Member)
- 정밀도: ±0.01mm, MOQ: 1개, ISO9001

## 진행 상태
- [x] Phase 1: Three.js 3D 외관 뷰 (2026-04-22)
- [ ] Phase 1: 형님 컨펌
- [ ] Phase 2: Rhino Python 상세 설계 (플레이트별)
- [ ] Phase 3: Fusion 360 어셈블리 + 간섭 체크 + 2D 도면
- [ ] Phase 4: STEP + PDF → 공장 발주

## 비용 추정
| 카테고리 | 예상 비용 |
|----------|----------|
| A. 프레임 외주 가공 (가공비+재료비+배송) | ₩550,000~1,030,000 |
| B. HGR20 레일+블록 (6레일, 12블록) | ₩300,000~400,000 |
| C. 스핀들 시스템 (1.5kW+VFD+펌프) | ₩350,000 |
| D. 모터+드라이버+전원 | ₩355,000 |
| E. 4축 로터리 | ₩375,000 |
| F. 볼스크류+베어링 (SFU1605×3) | ₩150,000 |
| G. 컨트롤러+전자부품 | ₩300,000 |
| H. 공구+액세서리 | ₩400,000 |
| **총합** | **₩2,780,000~3,360,000** |
