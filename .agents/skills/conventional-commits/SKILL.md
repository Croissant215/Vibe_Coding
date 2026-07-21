---
name: conventional-commits
description: 빌드/테스트 성공 후 Git Diff 자동 분석 및 Conventional Commits 명세 준수 커밋 메시지 자동 생성 스킬.
---

# 📝 Conventional Commits Skill

## 1. 개요 (Overview)
본 스킬은 코드 작성 및 검증(빌드/테스트) 완료 후 `git diff` 분석을 자동으로 수행하고, 변경 내역에 따라 **Conventional Commits** 표준 태그를 적용한 커밋 메시지를 생성 및 커밋을 자동화합니다.

---

## 2. 커밋 메시지 구조 (Format Specification)

```text
<type>(<scope>): <short summary>

[optional body describing details and rationale]
```

### 🏷️ 타입(Type) 분류 규정
* `feat`: 새로운 기능 추가 (예: `feat(auth): add secure login with prepared statement`)
* `fix`: 버그 수정 (예: `fix(sql): prevent SQL injection in vulnerable login endpoint`)
* `docs`: 문서 수정 (예: `docs(readme): update API setup guide`)
* `style`: 코드 의미에 영향을 주지 않는 스타일/포맷 변경 (예: `style(ui): apply tailwind glassmorphism styles`)
* `refactor`: 버그 수정이나 기능 추가가 아닌 코드 구조 개선 (예: `refactor(db): extract helper function for hashing`)
* `test`: 테스트 코드 추가 또는 수정 (예: `test(auth): add unit tests for user registration`)
* `chore`: 빌드 업무 수정, 패키지 매니저 설정 등 (예: `chore(deps): add mcp python dependency`)

---

## 3. 자동화 작업 순서 (Automated Process)
1. **차이점 분석**: `git diff --staged` 또는 `git diff`를 실행하여 변경 파일과 코드 라인을 파악합니다.
2. **타입 자동 판별**: 변경 내용의 성격(기능, 버그, 문서, 리팩토링 등)을 분석하여 알맞은 Prefix 태그를 선택합니다.
3. **요약문 생성**: 명령조(Imperative mood, Korean/English)로 명확하고 간결한 Headline 작성.
4. **Git Commit 실행**: 규격에 맞추어 Git Commit을 자동 완료합니다.
