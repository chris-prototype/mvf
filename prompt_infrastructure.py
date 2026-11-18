from textwrap import dedent

GITHUB_ORG = "palceholder"


def build_infra_prompt(repo_name, repo_full, title, ticket_id):
    return dedent(f"""\
        Set up the infrastructure for a new app. Do these steps in order:

        ## 1. Create GitHub repo

        Use the GitHub MCP to create a new repository:
        - Owner: `{GITHUB_ORG}`
        - Name: `{repo_name}`
        - Description: `{title} (built by software factory from {ticket_id})`
        - Private: false
        - Auto-init: true (so it has a default branch)

        Then clone it: `git clone https://github.com/{repo_full}.git .`

        If the repo already exists, just clone it.

        ## 2. Create Vercel project

        Use the Vercel MCP to create a new project:
        - Name: `{repo_name}`
        - Link it to the GitHub repo `{repo_full}`
        - Framework preset: Next.js

        If the project already exists, skip this step.

        ## 3. Provision Supabase via Vercel Marketplace

        Use the Vercel MCP or run: `vercel integration add supabase`
        This creates a Supabase project and auto-injects database env vars
        (POSTGRES_URL, SUPABASE_URL, SUPABASE_ANON_KEY, etc.) into the Vercel project.

        If Supabase is already provisioned (check `vercel integration list`), skip this step.

        ## 4. Pull env vars

        Run `vercel env pull .env.local` to pull the auto-injected Supabase env vars
        into the workspace so agents can use them during development.

        ## 5. Scaffold the Next.js app

        If there is no `package.json` in the repo yet, scaffold a Next.js app in place
        (create-next-app permits an existing `.git`/`README.md`):

        ```
        npx --yes create-next-app@latest . --ts --tailwind --app --src-dir --eslint --use-npm --import-alias "@/*" --yes
        ```

        Then add the test toolchain and a Jest config that uses `next/jest`:

        ```
        npm install -D jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom @types/jest ts-node
        ```

        Create `jest.config.ts` (via `next/jest`, testEnvironment `jsdom`,
        setupFilesAfterEnv `./jest.setup.ts`) and `jest.setup.ts`
        (`import '@testing-library/jest-dom'`). Add these scripts to `package.json`:
        `"test": "jest"` and `"test:coverage": "jest --coverage"`.

        Convention: all source lives under `src/` — pages/routes in `src/app/`,
        components in `src/components/`, using the `@/` import alias.

        Commit the scaffold to the default branch and push:

        ```
        git add -A && git commit -m "{ticket_id}: scaffold Next.js app (TS, Tailwind, Jest)" && git push origin HEAD
        ```

        If `package.json` already exists, skip this step.

        Confirm everything is ready with `git status` and `npm run build`.
    """)