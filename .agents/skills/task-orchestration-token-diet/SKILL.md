---
name: task-orchestration-token-diet
description: 멀티 에이전트 작업 분할, Strict Context Pruning(토큰 절약), 하이브리드 모델 라우팅 및 Subagent Thread Kill 정책 스킬.
---

# ⚡ Task Decomposition & Token Diet Policy Skill

## 1. 개요 (Overview)
본 스킬은 풀스택 개발 요청 시 오케스트레이터 에이전트가 복잡한 과제를 원자적(Atomic) 서브타스크로 분할하고, 최적의 하이브리드 LLM 모델에 동적으로 할당하며, 엄격한 토큰 절약(Token Diet) 및 스레드 수명주기(Thread Kill) 관리 정책을 집행합니다.

---

## 2. 세부 지침 (Detailed Rules)

### 🧩 1. 작업 분할 및 동적 라우팅 (Task Decomposition & Dynamic Routing)
* 대규모 요구사항 수신 시 오케스트레이터 에이전트는 즉시 **Frontend-Agent**, **Backend-Agent**, **QA-Agent** 등 전용 역할의 Subagent로 작업을 분할합니다.
* 서브에이전트 호출 시 명확하고 독립적인 한 가지 단일 과제(Atomic Sub-task)만 명시하여 전달합니다.

### ✂️ 2. 토큰 다이어트 및 컨텍스트 정리 (Context Pruning & Token Diet)
* **전체 코드베이스 전달 금지**: Subagent 생성 및 호출 시 프로젝트 전체 코드를 전달하지 않습니다.
* **스니펫 단위 전달**: 해당 작업 수행에 **직접적으로 필요한 코드 조각(최대 200줄 이내)** 및 관련 의존성 import 구문만 추출하여 전달합니다.
* **중복 로그 축소**: 터미널 실행 결과나 대용량 로그 전달 시 에러 핵심 지점(Stack Trace 상위 10줄 이내)만 요약하여 전달합니다.

### 💀 3. 스레드 강제 종료 정책 (Thread Kill Policy)
* Subagent가 전달받은 서브타스크를 완수하고 생성된 코드가 메인 코드베이스에 병합(Merge)되면, 오케스트레이터는 즉시 `manage_subagents` 툴을 사용하여 해당 Subagent의 대화 스레드를 종료(`kill`)합니다.
* 불필요하게 대화 스레드를 유지하여 발생되는 토큰 누적을 방지합니다.

### 🔀 4. 하이브리드 모델 라우팅 규정 (Hybrid Model Routing Rules)

| 모델 종류 | 역할 및 사용 비율 | 적용 대상 |
| :--- | :--- | :--- |
| **Gemini 3.5 Flash** | **Default Engine (90%)** | 코드 스캐폴딩, UI 컴포넌트 렌더링, CSS 스타일링, 기본 API 엔드포인트 작성, 단순 리팩토링 |
| **Gemini 3.1 Pro** | **Escalation Engine (10%)** | 1. 테스트 러너가 연속 3회 이상 실패할 경우 자가 치유 에스컬레이션<br>2. 최초 핵심 DB 스키마 및 아키텍처 수립 단계 |

> ⚠️ **주의**: `Gemini 3.1 Pro` 에이전트는 지정된 문제 해결(DB 수립 또는 3회 이상 실패 버그 디버깅) 완료 직후 즉시 스레드를 종료(`kill`)하여 메인 라우터인 `Gemini 3.5 Flash`로 복귀합니다.
