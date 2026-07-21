---
name: tailwind-shadcn-factory
description: Tailwind CSS 및 Shadcn UI 기반 모듈식 웹 UI 컴포넌트 설계 및 제작 스킬. 현대적 프론트엔드 UI 컴포넌트 라이브러리 패턴과 반응형 디자인 시스템을 준수합니다.
---

# 🎨 Tailwind CSS & Shadcn UI Component Factory Skill

## 1. 개요 (Overview)
본 스킬은 현대적이고 세련된 프론트엔드 UI/UX 구축을 위하여 **Tailwind CSS** 및 **Shadcn UI**의 모듈식 컴포넌트 패턴을 적용합니다. 날(raw) HTML/CSS 작성을 지양하고, 재사용 가능한 모듈형 컴포넌트 시스템을 구축합니다.

---

## 2. 디자인 가이드라인 & 원칙 (Design Principles)

### 🎨 Visual & Aesthetic Excellence
* **컬러 팔레트**: 원색(Plain Red/Blue) 사용 금지. HSL 기반의 테마 컬러스킴(Slate, Indigo, Emerald, Zinc 등) 및 Sleek Dark Mode 지원.
* **타이포그래피**: 시스템 기본 폰트 대신 Google Fonts (Inter, Outfit, Roboto 등) 적용.
* **디자인 기법**: Glassmorphism, Subtle Gradients, Smooth Box Shadows, Micro-interactions.
* **컴포넌트 모듈화**: Atomic Design (Primitives -> Components -> Organisms -> Pages) 구조 적용.

---

## 3. 구현 명세 (Implementation Specs)

### 🧩 Tailwind CSS 클래스 토큰 예시
```html
<!-- Glassmorphism Card Element Example -->
<div class="relative overflow-hidden rounded-2xl border border-white/10 bg-slate-900/80 p-6 backdrop-blur-xl shadow-2xl transition-all hover:border-indigo-500/50 hover:shadow-indigo-500/10">
  <div class="flex items-center justify-between gap-4">
    <h3 class="text-lg font-semibold text-slate-100">Component Title</h3>
    <span class="inline-flex items-center rounded-full bg-indigo-500/10 px-3 py-1 text-xs font-medium text-indigo-400 ring-1 ring-inset ring-indigo-500/20">Active</span>
  </div>
  <p class="mt-2 text-sm text-slate-400">Description text goes here with clean typography and proper contrast.</p>
</div>
```

---

## 4. 컴포넌트 라이브러리 연동 규칙
1. **Shadcn UI 패턴 적용**: Button, Dialog, Card, Input, Tabs, Badge 등 핵심 원자 컴포넌트는 Shadcn UI 디자인 계약을 기본으로 구현합니다.
2. **반응형 디자인 (Responsive)**: Mobile-First 접근 방식 (`sm:`, `md:`, `lg:`, `xl:`)을 모든 레이아웃에 필수로 포함합니다.
3. **접근성 (Accessibility)**: ARIA 속성 (`aria-expanded`, `aria-label`, `role`) 및 키보드 네비게이션을 기본 탑재합니다.
