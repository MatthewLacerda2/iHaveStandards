import { createTester } from "./tester";
import { noFetchOutsideSdk } from "./no-fetch-outside-sdk";

const tester = createTester();

tester.run("no-fetch-outside-sdk", noFetchOutsideSdk, {
  valid: [
    // The SDK client is the one place fetch is allowed.
    {
      code: `const r = fetch("/api/v1/items");`,
      filename: "src/lib/api/client.ts",
    },
    // A page going through the SDK is fine.
    {
      code: `import { listItems } from "@/lib/api/items";`,
      filename: "src/routes/index.tsx",
    },
  ],
  invalid: [
    {
      code: `const r = fetch("/api/v1/items");`,
      filename: "src/routes/index.tsx",
      errors: [{ messageId: "network" }],
    },
  ],
});
