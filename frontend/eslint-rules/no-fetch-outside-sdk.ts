import { type TSESTree } from "@typescript-eslint/utils";
import { createRule, isApiSdkFile } from "./utils";

export const noFetchOutsideSdk = createRule({
  name: "no-fetch-outside-sdk",
  meta: {
    type: "problem",
    docs: {
      description:
        "Forbid direct fetch() outside lib/api — pages call the typed SDK, not the network.",
    },
    messages: {
      network:
        "Direct fetch() is only allowed in lib/api. Go through the typed SDK (lib/api/<domain>.ts).",
    },
    schema: [],
  },
  defaultOptions: [],
  create(context) {
    // The SDK itself (lib/api/client.ts) is the one place fetch lives.
    if (isApiSdkFile(context.filename)) return {};
    return {
      CallExpression(node: TSESTree.CallExpression) {
        const callee = node.callee;
        if (callee.type === "Identifier" && callee.name === "fetch") {
          context.report({ node, messageId: "network" });
        }
      },
    };
  },
});
