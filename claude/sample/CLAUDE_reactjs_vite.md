## 🛠️ Development Environment

- **Language**: TypeScript (`^5.0.0`)
- **Framework**: Vite + React Router
- **Styling**: Tailwind CSS
- **Component Library**: shadcn/ui
- **Data Fetching**: React Query (TanStack)
- **Testing**: Jest + React Testing Library
- **Linting**: ESLint with `@typescript-eslint`
- **Formatting**: Prettier
- **Package Manager**: `pnpm` (preferred)

## 📂 Recommended Project Structure

```warp-runnable-command
.
├── src/                     # Source code
│   ├── main.tsx             # Application entry point
│   ├── App.tsx              # Main application component with routing
│   ├── api/                 # Axios & http api
│   ├── components/          # UI components (shadcn or custom)
│   ├── hooks/               # Custom React hooks
│   ├── pages/               # Page components
│   ├── styles/              # Gloabl and Tailwind customizations
│   ├── router/              # Router
│   ├── lib/                 # Client helpers, API wrappers, etc.
│   ├── i18n/                # i18n
│   ├── tests/               # Unit and integration tests
├── public/
├── .eslintrc.js
├── tailwind.config.ts
├── tsconfig.json
├── vite.config.ts
├── package.json
└── README.md
```

## 📦 Installation Notes

- Vite setup with React and TypeScript
- shadcn/ui installed with `npx shadcn-ui@latest init`
- React Query initialized with `<QueryClientProvider>`

## ⚙️ Dev Commands

- **Dev server**: `pnpm dev`
- **Build**: `pnpm build`
- **Start**: `pnpm start`
- **Lint**: `pnpm lint`
- **Format**: `pnpm format`
- **Test**: `pnpm test`

## 🧠 Claude Code Usage

- Use `claude /init` to create this file
- Run `claude` in the root of the repo
- Prompt with: `think hard`, `ultrathink` for deep plans
- Compact with `claude /compact`
- Use `claude /permissions` to whitelist safe tools

## 📌 Prompt Examples

```warp-runnable-command
Claude, refactor `useUser.ts` to use React Query.
Claude, scaffold a new `Button.tsx` using shadcn/ui and Tailwind.
Claude, generate the Tailwind styles for this mockup screenshot.
Claude, build an API route handler for POST /api/user.
Claude, create a test for `ProfileCard.tsx` using RTL.
```

## 🧪 Testing Practices

- **Testing Library**: `@testing-library/react`
- **Mocking**: `msw`, `vi.mock()`
- **Test command**: `pnpm test`
- Organize tests in `/tests` or co-located with components

## 🧱 Component Guidelines

- Use `shadcn/ui` components by default for form elements, cards, dialogs, etc.
- Style components with Tailwind utility classes
- Co-locate CSS modules or component-specific styling in the same directory

## ⚛️ React Query Patterns

- Set up `QueryClient` in `src/main.tsx`
- Use `useQuery`, `useMutation`, `useInfiniteQuery` from `@tanstack/react-query`
- Place API logic in `/lib/api/` and call via hooks
- Use query keys prefixed by domain: `['user', id]`

## Routing

- React Router v6 with BrowserRouter
- Routes defined in `src/App.tsx`
- Use `useNavigate` for programmatic navigation
- Use `Link` component for navigation links

## 📝 Code Style Standards

- Prefer arrow functions
- Annotate return types
- Always destructure props
- Avoid `any` type, use `unknown` or strict generics
- Group imports: react → react-router → libraries → local

## 🔍 Documentation & Onboarding

- Each component and hook should include a short comment on usage
- Document top-level files (like `src/App.tsx`) and configs
- Keep `README.md` up to date with getting started, design tokens, and component usage notes

## 🔐 Security

- Validate all server-side inputs (API routes)
- Use HTTPS-only cookies and CSRF tokens when applicable
- Protect sensitive routes with middleware or session logic

## 🧩 Custom Slash Commands

Stored in `.claude/commands/`:

- `/generate-hook`: Scaffold a React hook with proper types and test
- `/wrap-client-component`: Convert server to client-side with hydration-safe boundary
- `/update-tailwind-theme`: Modify Tailwind config and regenerate tokens
- `/mock-react-query`: Set up MSW mocking for all useQuery keys