"use strict";
(self["webpackChunk_datalayer_jupyter_viewer"] = self["webpackChunk_datalayer_jupyter_viewer"] || []).push([[7674],{

/***/ 73469:
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "KERNEL_SETTINGS_SCHEMA": () => (/* reexport */ kernel_v0_schema_namespaceObject2),
  "default": () => (/* binding */ pyodide_kernel_extension_lib)
});

// EXTERNAL MODULE: ./node_modules/@jupyterlab/coreutils/lib/index.js
var lib = __webpack_require__(48425);
// EXTERNAL MODULE: ./node_modules/@jupyterlite/server/lib/tokens.js + 1 modules
var tokens = __webpack_require__(51237);
// EXTERNAL MODULE: ./node_modules/@jupyterlite/kernel/lib/tokens.js
var lib_tokens = __webpack_require__(52416);
// EXTERNAL MODULE: ./node_modules/@jupyterlite/contents/lib/tokens.js
var contents_lib_tokens = __webpack_require__(49703);
;// CONCATENATED MODULE: ./node_modules/@jupyterlite/pyodide-kernel-extension/schema/kernel.v0.schema.json
const kernel_v0_schema_namespaceObject = __webpack_require__.p + "schema/kernel.v0.schema.json";
var kernel_v0_schema_namespaceObject2 = /*#__PURE__*/__webpack_require__.t(kernel_v0_schema_namespaceObject);
;// CONCATENATED MODULE: ./node_modules/@jupyterlite/pyodide-kernel-extension/style/img/pyodide.svg
/* harmony default export */ const pyodide = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<svg width=\"182\" height=\"182\" data-name=\"Layer 1\" version=\"1.1\" viewBox=\"0 0 182 182\" xmlns=\"http://www.w3.org/2000/svg\">\n <defs>\n  <style>.cls-1 {\n        fill: #fff;\n      }\n\n      .cls-2 {\n        fill: #654ff0;\n      }</style>\n </defs>\n <rect width=\"182\" height=\"182\" fill=\"#fff\" stop-color=\"#000000\" style=\"paint-order:stroke fill markers\"/>\n <rect class=\"cls-1\" x=\"107\" y=\"125\" width=\"50\" height=\"32\"/>\n <path class=\"cls-2\" d=\"m135.18 97c0-0.13-0.01-7.24-0.02-7.37h27.51v71.33h-71.34v-71.33h27.51c0 0.13-0.02 7.24-0.02 7.37m32.59 56.33h4.9l-7.43-25.25h-7.45l-6.12 25.25h4.75l1.24-5.62h8.49l1.61 5.62zm-26.03 0h4.69l6.02-25.25h-4.63l-3.69 17.4h-0.06l-3.5-17.4h-4.42l-3.9 17.19h-0.06l-3.23-17.19h-4.72l5.44 25.25h4.78l3.75-17.19h0.06zm18.89-19.03h1.99l2.37 9.27h-6.42z\"/>\n <path d=\"m89 49.66c0 10.6-8.8 20-20 20h-40v20h-10v-70h50c10.7 0 19.7 8.9 20 20zm-10-10c0-5.5-4.5-10-10-10h-40v30h40c5.5 0 10-4.5 10-10z\"/>\n <path d=\"m132 67.66v22h-10v-22l-30-33v-15h10v10.9l25 27.5 25-27.5v-10.9h10v15z\"/>\n</svg>\n");
;// CONCATENATED MODULE: ./node_modules/@jupyterlite/pyodide-kernel-extension/lib/index.js
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







const KERNEL_ICON_URL = `data:image/svg+xml;base64,${btoa(pyodide)}`;
/**
 * The default CDN fallback for Pyodide
 */
const PYODIDE_CDN_URL = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js';
/**
 * The id for the extension, and key in the litePlugins.
 */
const PLUGIN_ID = '@jupyterlite/pyodide-kernel-extension:kernel';
/**
 * A plugin to register the Pyodide kernel.
 */
const kernel = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [lib_tokens/* IKernelSpecs */.qP],
  optional: [tokens/* IServiceWorkerManager */.f, contents_lib_tokens/* IBroadcastChannelWrapper */.dC],
  activate: (app, kernelspecs, serviceWorker, broadcastChannel) => {
    const config = JSON.parse(lib.PageConfig.getOption('litePluginSettings') || '{}')[PLUGIN_ID] || {};
    const url = config.pyodideUrl || PYODIDE_CDN_URL;
    const pyodideUrl = lib.URLExt.parse(url).href;
    const pipliteWheelUrl = config.pipliteWheelUrl ? lib.URLExt.parse(config.pipliteWheelUrl).href : undefined;
    const rawPipUrls = config.pipliteUrls || [];
    const pipliteUrls = rawPipUrls.map(pipUrl => lib.URLExt.parse(pipUrl).href);
    const disablePyPIFallback = !!config.disablePyPIFallback;
    kernelspecs.register({
      spec: {
        name: 'python',
        display_name: 'Python (Pyodide)',
        language: 'python',
        argv: [],
        resources: {
          'logo-32x32': KERNEL_ICON_URL,
          'logo-64x64': KERNEL_ICON_URL
        }
      },
      create: async options => {
        const {
          PyodideKernel
        } = await Promise.all(/* import() */[__webpack_require__.e(7179), __webpack_require__.e(758)]).then(__webpack_require__.bind(__webpack_require__, 38865));
        const mountDrive = !!((serviceWorker === null || serviceWorker === void 0 ? void 0 : serviceWorker.enabled) && (broadcastChannel === null || broadcastChannel === void 0 ? void 0 : broadcastChannel.enabled));
        if (mountDrive) {
          console.info('Pyodide contents will be synced with Jupyter Contents');
        } else {
          console.warn('Pyodide contents will NOT be synced with Jupyter Contents');
        }
        return new PyodideKernel({
          ...options,
          pyodideUrl,
          pipliteWheelUrl,
          pipliteUrls,
          disablePyPIFallback,
          mountDrive
        });
      }
    });
  }
};
const plugins = [kernel];
/* harmony default export */ const pyodide_kernel_extension_lib = (plugins);

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiNzY3NC5qdXB5dGVyLXZpZXdlci5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7QUNBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AZGF0YWxheWVyL2p1cHl0ZXItdmlld2VyLy4vbm9kZV9tb2R1bGVzL0BqdXB5dGVybGl0ZS9weW9kaWRlLWtlcm5lbC1leHRlbnNpb24vc3R5bGUvaW1nL3B5b2RpZGUuc3ZnIiwid2VicGFjazovL0BkYXRhbGF5ZXIvanVweXRlci12aWV3ZXIvLi9ub2RlX21vZHVsZXMvQGp1cHl0ZXJsaXRlL3B5b2RpZGUta2VybmVsLWV4dGVuc2lvbi9saWIvaW5kZXguanMiXSwic291cmNlc0NvbnRlbnQiOlsiZXhwb3J0IGRlZmF1bHQgXCI8P3htbCB2ZXJzaW9uPVxcXCIxLjBcXFwiIGVuY29kaW5nPVxcXCJVVEYtOFxcXCI/Plxcbjxzdmcgd2lkdGg9XFxcIjE4MlxcXCIgaGVpZ2h0PVxcXCIxODJcXFwiIGRhdGEtbmFtZT1cXFwiTGF5ZXIgMVxcXCIgdmVyc2lvbj1cXFwiMS4xXFxcIiB2aWV3Qm94PVxcXCIwIDAgMTgyIDE4MlxcXCIgeG1sbnM9XFxcImh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnXFxcIj5cXG4gPGRlZnM+XFxuICA8c3R5bGU+LmNscy0xIHtcXG4gICAgICAgIGZpbGw6ICNmZmY7XFxuICAgICAgfVxcblxcbiAgICAgIC5jbHMtMiB7XFxuICAgICAgICBmaWxsOiAjNjU0ZmYwO1xcbiAgICAgIH08L3N0eWxlPlxcbiA8L2RlZnM+XFxuIDxyZWN0IHdpZHRoPVxcXCIxODJcXFwiIGhlaWdodD1cXFwiMTgyXFxcIiBmaWxsPVxcXCIjZmZmXFxcIiBzdG9wLWNvbG9yPVxcXCIjMDAwMDAwXFxcIiBzdHlsZT1cXFwicGFpbnQtb3JkZXI6c3Ryb2tlIGZpbGwgbWFya2Vyc1xcXCIvPlxcbiA8cmVjdCBjbGFzcz1cXFwiY2xzLTFcXFwiIHg9XFxcIjEwN1xcXCIgeT1cXFwiMTI1XFxcIiB3aWR0aD1cXFwiNTBcXFwiIGhlaWdodD1cXFwiMzJcXFwiLz5cXG4gPHBhdGggY2xhc3M9XFxcImNscy0yXFxcIiBkPVxcXCJtMTM1LjE4IDk3YzAtMC4xMy0wLjAxLTcuMjQtMC4wMi03LjM3aDI3LjUxdjcxLjMzaC03MS4zNHYtNzEuMzNoMjcuNTFjMCAwLjEzLTAuMDIgNy4yNC0wLjAyIDcuMzdtMzIuNTkgNTYuMzNoNC45bC03LjQzLTI1LjI1aC03LjQ1bC02LjEyIDI1LjI1aDQuNzVsMS4yNC01LjYyaDguNDlsMS42MSA1LjYyem0tMjYuMDMgMGg0LjY5bDYuMDItMjUuMjVoLTQuNjNsLTMuNjkgMTcuNGgtMC4wNmwtMy41LTE3LjRoLTQuNDJsLTMuOSAxNy4xOWgtMC4wNmwtMy4yMy0xNy4xOWgtNC43Mmw1LjQ0IDI1LjI1aDQuNzhsMy43NS0xNy4xOWgwLjA2em0xOC44OS0xOS4wM2gxLjk5bDIuMzcgOS4yN2gtNi40MnpcXFwiLz5cXG4gPHBhdGggZD1cXFwibTg5IDQ5LjY2YzAgMTAuNi04LjggMjAtMjAgMjBoLTQwdjIwaC0xMHYtNzBoNTBjMTAuNyAwIDE5LjcgOC45IDIwIDIwem0tMTAtMTBjMC01LjUtNC41LTEwLTEwLTEwaC00MHYzMGg0MGM1LjUgMCAxMC00LjUgMTAtMTB6XFxcIi8+XFxuIDxwYXRoIGQ9XFxcIm0xMzIgNjcuNjZ2MjJoLTEwdi0yMmwtMzAtMzN2LTE1aDEwdjEwLjlsMjUgMjcuNSAyNS0yNy41di0xMC45aDEwdjE1elxcXCIvPlxcbjwvc3ZnPlxcblwiOyIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbmltcG9ydCB7IFBhZ2VDb25maWcsIFVSTEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJU2VydmljZVdvcmtlck1hbmFnZXIgfSBmcm9tICdAanVweXRlcmxpdGUvc2VydmVyJztcbmltcG9ydCB7IElLZXJuZWxTcGVjcyB9IGZyb20gJ0BqdXB5dGVybGl0ZS9rZXJuZWwnO1xuaW1wb3J0IHsgSUJyb2FkY2FzdENoYW5uZWxXcmFwcGVyIH0gZnJvbSAnQGp1cHl0ZXJsaXRlL2NvbnRlbnRzJztcbmltcG9ydCAqIGFzIF9LRVJORUxfU0VUVElOR1NfU0NIRU1BIGZyb20gJy4uL3NjaGVtYS9rZXJuZWwudjAuc2NoZW1hLmpzb24nO1xuZXhwb3J0IHsgX0tFUk5FTF9TRVRUSU5HU19TQ0hFTUEgYXMgS0VSTkVMX1NFVFRJTkdTX1NDSEVNQSB9O1xuaW1wb3J0IEtFUk5FTF9JQ09OX1NWR19TVFIgZnJvbSAnLi4vc3R5bGUvaW1nL3B5b2RpZGUuc3ZnJztcbmNvbnN0IEtFUk5FTF9JQ09OX1VSTCA9IGBkYXRhOmltYWdlL3N2Zyt4bWw7YmFzZTY0LCR7YnRvYShLRVJORUxfSUNPTl9TVkdfU1RSKX1gO1xuLyoqXG4gKiBUaGUgZGVmYXVsdCBDRE4gZmFsbGJhY2sgZm9yIFB5b2RpZGVcbiAqL1xuY29uc3QgUFlPRElERV9DRE5fVVJMID0gJ2h0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9weW9kaWRlL3YwLjI1LjAvZnVsbC9weW9kaWRlLmpzJztcbi8qKlxuICogVGhlIGlkIGZvciB0aGUgZXh0ZW5zaW9uLCBhbmQga2V5IGluIHRoZSBsaXRlUGx1Z2lucy5cbiAqL1xuY29uc3QgUExVR0lOX0lEID0gJ0BqdXB5dGVybGl0ZS9weW9kaWRlLWtlcm5lbC1leHRlbnNpb246a2VybmVsJztcbi8qKlxuICogQSBwbHVnaW4gdG8gcmVnaXN0ZXIgdGhlIFB5b2RpZGUga2VybmVsLlxuICovXG5jb25zdCBrZXJuZWwgPSB7XG4gIGlkOiBQTFVHSU5fSUQsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJS2VybmVsU3BlY3NdLFxuICBvcHRpb25hbDogW0lTZXJ2aWNlV29ya2VyTWFuYWdlciwgSUJyb2FkY2FzdENoYW5uZWxXcmFwcGVyXSxcbiAgYWN0aXZhdGU6IChhcHAsIGtlcm5lbHNwZWNzLCBzZXJ2aWNlV29ya2VyLCBicm9hZGNhc3RDaGFubmVsKSA9PiB7XG4gICAgY29uc3QgY29uZmlnID0gSlNPTi5wYXJzZShQYWdlQ29uZmlnLmdldE9wdGlvbignbGl0ZVBsdWdpblNldHRpbmdzJykgfHwgJ3t9JylbUExVR0lOX0lEXSB8fCB7fTtcbiAgICBjb25zdCB1cmwgPSBjb25maWcucHlvZGlkZVVybCB8fCBQWU9ESURFX0NETl9VUkw7XG4gICAgY29uc3QgcHlvZGlkZVVybCA9IFVSTEV4dC5wYXJzZSh1cmwpLmhyZWY7XG4gICAgY29uc3QgcGlwbGl0ZVdoZWVsVXJsID0gY29uZmlnLnBpcGxpdGVXaGVlbFVybCA/IFVSTEV4dC5wYXJzZShjb25maWcucGlwbGl0ZVdoZWVsVXJsKS5ocmVmIDogdW5kZWZpbmVkO1xuICAgIGNvbnN0IHJhd1BpcFVybHMgPSBjb25maWcucGlwbGl0ZVVybHMgfHwgW107XG4gICAgY29uc3QgcGlwbGl0ZVVybHMgPSByYXdQaXBVcmxzLm1hcChwaXBVcmwgPT4gVVJMRXh0LnBhcnNlKHBpcFVybCkuaHJlZik7XG4gICAgY29uc3QgZGlzYWJsZVB5UElGYWxsYmFjayA9ICEhY29uZmlnLmRpc2FibGVQeVBJRmFsbGJhY2s7XG4gICAga2VybmVsc3BlY3MucmVnaXN0ZXIoe1xuICAgICAgc3BlYzoge1xuICAgICAgICBuYW1lOiAncHl0aG9uJyxcbiAgICAgICAgZGlzcGxheV9uYW1lOiAnUHl0aG9uIChQeW9kaWRlKScsXG4gICAgICAgIGxhbmd1YWdlOiAncHl0aG9uJyxcbiAgICAgICAgYXJndjogW10sXG4gICAgICAgIHJlc291cmNlczoge1xuICAgICAgICAgICdsb2dvLTMyeDMyJzogS0VSTkVMX0lDT05fVVJMLFxuICAgICAgICAgICdsb2dvLTY0eDY0JzogS0VSTkVMX0lDT05fVVJMXG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBjcmVhdGU6IGFzeW5jIG9wdGlvbnMgPT4ge1xuICAgICAgICBjb25zdCB7XG4gICAgICAgICAgUHlvZGlkZUtlcm5lbFxuICAgICAgICB9ID0gYXdhaXQgaW1wb3J0KCdAanVweXRlcmxpdGUvcHlvZGlkZS1rZXJuZWwnKTtcbiAgICAgICAgY29uc3QgbW91bnREcml2ZSA9ICEhKChzZXJ2aWNlV29ya2VyID09PSBudWxsIHx8IHNlcnZpY2VXb3JrZXIgPT09IHZvaWQgMCA/IHZvaWQgMCA6IHNlcnZpY2VXb3JrZXIuZW5hYmxlZCkgJiYgKGJyb2FkY2FzdENoYW5uZWwgPT09IG51bGwgfHwgYnJvYWRjYXN0Q2hhbm5lbCA9PT0gdm9pZCAwID8gdm9pZCAwIDogYnJvYWRjYXN0Q2hhbm5lbC5lbmFibGVkKSk7XG4gICAgICAgIGlmIChtb3VudERyaXZlKSB7XG4gICAgICAgICAgY29uc29sZS5pbmZvKCdQeW9kaWRlIGNvbnRlbnRzIHdpbGwgYmUgc3luY2VkIHdpdGggSnVweXRlciBDb250ZW50cycpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGNvbnNvbGUud2FybignUHlvZGlkZSBjb250ZW50cyB3aWxsIE5PVCBiZSBzeW5jZWQgd2l0aCBKdXB5dGVyIENvbnRlbnRzJyk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIG5ldyBQeW9kaWRlS2VybmVsKHtcbiAgICAgICAgICAuLi5vcHRpb25zLFxuICAgICAgICAgIHB5b2RpZGVVcmwsXG4gICAgICAgICAgcGlwbGl0ZVdoZWVsVXJsLFxuICAgICAgICAgIHBpcGxpdGVVcmxzLFxuICAgICAgICAgIGRpc2FibGVQeVBJRmFsbGJhY2ssXG4gICAgICAgICAgbW91bnREcml2ZVxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxufTtcbmNvbnN0IHBsdWdpbnMgPSBba2VybmVsXTtcbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9